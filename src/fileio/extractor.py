'''
Created on 12 apr 2016

@author: peppone
'''
import re

from graph.network import network
import sys


class extractor(object):

    def vmgraphextractor(self,filename, defaultCpu = 10,defaultBw=1e6):

        fhandle = open (filename, 'r')
        graph = dict();
        vmDict = {}
        for line in fhandle:
            previous = None
            successive = None
            if line.isspace():
                continue
            res = re.findall('\s*([0-9]+|<->|<-|->|\[[^\]]*\])\s*', line)
            if res is None:
                continue
            elem = res.pop(0)
            previous = self.parsedigit(elem, line)
            elem = res.pop(0)
            popnewelement = False
            if self.isproperty(elem):
                popnewelement = True
                prop = self.parseproperty(elem, line)
                cpu = int(prop.get('cpu', None))
                if cpu == None:
                    print("Warning: cpu for VM# {} set to default value".format(previous),file=sys.stderr)
                    cpu = int(defaultCpu)
                self.addtodictionary(previous,cpu, vmDict,line)
            else:
                if vmDict.get(previous,None)==None:
                    print("Warning: cpu for VM# {} set to default value".format(previous),file=sys.stderr)
                    cpu=defaultCpu
                    self.addtodictionary(previous, cpu, vmDict,line)
            while len(res) > 0:
                if popnewelement:
                    elem = res.pop(0)
                popnewelement = False
                direction = self.parseconnector(elem, line)
                connector=elem
                elem = res.pop(0)
                successive = self.parsedigit(elem, line)
                if(successive == previous):
                    raise Exception("Source and destination must be different")
                if len(res) > 0:
                    elem = res.pop(0)
                else:
                    if vmDict.get(successive,None)==None:
                        print("Warning: cpu for VM# {} set to default value".format(successive),file=sys.stderr)
                    #vmDict[successive] = defaultCpu
                        self.addtodictionary(successive, defaultCpu, vmDict, line)
                prop = self.parseproperty(elem, line)
                bw = prop.get('bw', None)
                if bw ==None:
                    print("Warning: bw for link {}{}{} set to default value".format(previous,connector,successive),file=sys.stderr)
                    bw =defaultBw
                bw = float(bw)
                cpu = prop.get('cpu', None)
                if cpu == None:
                    if vmDict.get(successive,None)==None:
                        print("Warning: cpu for VM# {} set to default value".format(successive),file=sys.stderr)
                        cpu =int(defaultCpu)
                else:
                    cpu=int(cpu)
                self.addtodictionary(successive, cpu, vmDict,line)
                if len(prop) > 0:
                    popnewelement = True;
                if direction[0]:
                    adjlist = graph.get(successive, {})
                    adjlist[previous] = bw
                    graph[successive] = adjlist
                if direction[1]:
                    adjlist = graph.get(previous, {})
                    adjlist[successive] = bw;
                    graph[previous] = adjlist
                previous = successive
                successive = None
        net = network()
        net.addConnections(graph)
        net.addNodeList(vmDict)
        return net
        
    def adjextractor(self, filename,defaultBw=10e6):
        fhandle = open (filename, 'r')
        graph = dict();
        typeDict = {}
        for line in fhandle:
            previous = None
            successive = None
            res = re.findall('\s*([0-9]+|<->|<-|->|\[[^\]]*\])\s*', line)
            if res is None:
                continue
            elem = res.pop(0)
            previous = self.parsedigit(elem, line)
            elem = res.pop(0)
            popnewelement = False
            if self.isproperty(elem):
                popnewelement = True
                prop = self.parseproperty(elem, line)
                enType = prop.get('type', "server")
                self.addtodictionary(previous, enType, typeDict,line)
            else:
                if typeDict.get(previous,None)==None:
                    enType = 'switch'
                    self.addtodictionary(previous, enType, typeDict,line)
            while len(res) > 0:
                if popnewelement:
                    elem = res.pop(0)
                popnewelement = False
                direction = self.parseconnector(elem, line)
                connector = elem
                elem = res.pop(0)
                successive = self.parsedigit(elem, line)
                if(successive == previous):
                    raise Exception("Source and destination must be different")
                if len(res) > 0:
                    elem = res.pop(0)
                else:
                    typeDict[successive] = "switch"
                prop = self.parseproperty(elem, line)
                bw = prop.get('bw', None)
                if bw ==None:
                    print("Warning: bw for link {}{}{} set to default value".format(previous,connector,successive),file=sys.stderr)
                    bw =defaultBw
                bw = float(bw)
                enType = prop.get('type', None)
                if(enType!=None):
                    enType = enType.lower()
                    self.addtodictionary(successive, enType, typeDict,line)
                if len(prop) > 0:
                    popnewelement = True;
                if direction[0]:
                    adjlist = graph.get(successive, {})
                    adjlist[previous] = bw
                    graph[successive] = adjlist
                if direction[1]:
                    adjlist = graph.get(previous, {})
                    adjlist[successive] = bw;
                    graph[previous] = adjlist
                previous = successive
                successive = None
        net = network()
        net.addConnections(graph)
        net.addNodeList(typeDict)
        return net
    
    def demandgeneration(self,vmdict, allocation):
        ''' Result: list of
         ((vmsrc,serversrc),(vmdest,serverdest),bw)'''
        demandlist=[]
        for srcvm in vmdict:
            adjlist = vmdict[srcvm]
            for destvm in adjlist:
                bw = adjlist[destvm]
                demandlist.append(((srcvm,allocation[srcvm][0]),(destvm,allocation[destvm][0]),bw))
        print(demandlist)
        return demandlist
    def removesameserverdemands(self,demandlist):
        newdemandlist = demandlist
        for demand in demandlist:
            srcsrv=demand[0][1]
            dstsrv=demand[1][1]
            if srcsrv == dstsrv:
                newdemandlist.remove(demand)
        return newdemandlist
                
    def addtodictionary(self,elem,eType,dType,line):
        if eType == None:
            return
        currentType = dType.get(elem, None)
        if  currentType !=None and currentType !=eType:
            raise Exception("Mismatching property for "+str(elem)+" in line:\n\t"+line + "previous was " +str(currentType)+"\nactual is " + str(eType))
        else:
            dType[elem] = eType
            
    def parsedigit(self, arg, line):
        if not self.isdigit(arg):
            raise Exception("In line:\n\t" + line + "expected digit, found instead:\n\t" + arg)
        else:
            return int(arg)
    
    def parseconnector(self, arg, line):
        if not self.isconnector(arg):
            raise Exception("In line:\n\t" + line + "expected connector, found instead:\n\t" + arg)
        result = (False, False)
        if arg == '<->':
            result = (True, True)
        elif arg == '<-':
            result = (True, False)
        elif arg == '->':
            result = (False, True)     
        return result
    
    def parseproperty(self, arg, line):
        if not self.isproperty(arg):
            return {}
        return self.propertyextractor(arg)
    
    def isproperty(self, arg):
        if arg.startswith("[") and arg.endswith("]"):
            return True
        else:
            return False
        
    def isdigit(self, arg):
        try:
            int(arg)
        except:
            return False
        return True


    def isconnector(self, arg):
        if (arg == '<->')or (arg == '<-') or (arg == '->'):
            return True
        else:
            return False
        
    def propertyextractor(self, arg):
        arg = arg[1:len(arg) - 1]
        res = re.findall("\s*[a-zA-z][a-zA-z0-9]*\s*=\s*\"*[a-zA-z0-9\.]*\"*\s*", arg)
        resultDict = {}
        for tup in res:
            tup = re.findall("(.*)=(.*)", tup)
            for elem in tup:
                rst = elem[0].strip()
                name = self.parsename(rst)
                # self.parseassignment(rst)
                rst = elem[1].strip()
                value = self.parsevalue(rst)
                resultDict[name] = value
        return resultDict;
            

    def parsename(self, arg):
        if re.match("[a-zA-z][a-zA-z0-9]", arg) != None:
            return arg
        else:
            return None;
    
    def parseassignment(self, arg):
        if re.match("=", arg) == None:
            raise Exception("Assigment required")
    
    def parsevalue(self, arg):
        if arg.startswith("\""):
            if not arg.endswith("\""):
                raise Exception("Needed final quote")
            arg = arg[1:-1]
        elif (not arg.startswith("\"") and arg.endswith("\"")):
            raise Exception("Needed initial quote")
        if len(arg) == 0:
            arg = None
        return arg
        pass
