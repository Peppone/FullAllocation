'''
Created on 14 apr 2016

@author: peppone
'''
import operator

from entity.server import serverlist


class allocator(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def firstallocation(self,vmdict,topology,policy="wf"):
        gateway = list((elem[0] for elem in topology.items() if elem[1]=="gateway" ))
        if len(gateway)!=1:
            raise Exception("Exactly one gateway should be present")
        gwvm= vmdict.get(0,None)
        vmdict.pop(0,None)
        vmlist= sorted(vmdict.items(), key = operator.itemgetter(1),reverse=True);
        serverstatus={}
        server = sorted((elem[0] for elem in topology.items() if elem[1]=='server'))
        for s in server:
            serverstatus[s]=0
        serverlst = serverlist()
        allocation={}
        if policy == 'wf':
            allocation = self.worstfitallocation(vmlist,serverstatus)
        if policy == 'bf':
            allocation = self.bestfitallocation(vmlist, serverstatus)
#         for s in server:
#             print ([(elem) for elem in allocation if allocation[elem]==int(s)])
        if gwvm != None:
            allocation[0]=(gateway[0],gwvm)
            vmdict[0]=gwvm
        return allocation
        
    def bestfitallocation(self,vmlist,serverstatus):
        allocation={}
        for vm in vmlist:
            server = sorted(((elem[0],elem[1]) for elem in serverstatus.items()),key=(operator.itemgetter(1)),reverse=True)
            allocationIndex = 0
            vmcpu = vm[1]
            while allocationIndex < len(server)-1:
                occupancy=server[allocationIndex][1]
                if occupancy + vm[1] > 100:
                    allocationIndex = allocationIndex +1
                else:
                    break
            allocation[vm[0]] = (server[allocationIndex][0],vmcpu)
            serverstatus[server[allocationIndex][0]]=serverstatus[server[allocationIndex][0]]+vm[1]
        return allocation
    
    def worstfitallocation(self,vmlist,serverstatus):
        allocation = {}
        for vm in vmlist:
            server = sorted(((elem[0],elem[1]) for elem in serverstatus.items()),key=(operator.itemgetter(1)))
            allocation[vm[0]] = (server[0][0],vm[1])
            serverstatus[server[0][0]]=serverstatus[server[0][0]]+vm[1]
        return allocation
        