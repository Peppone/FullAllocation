
class network(object):

    def __init__(self):
        self.node = {};
        self.adjList = {}
        
    def addNodeList(self,nlist):
        if type(nlist) is not dict:
            raise Exception(dict,"is not a dictionary")
        for node in nlist:
                self.node[node]=nlist[node];
                    
    def addConnections(self,clist):
        #if clist is not dict:
        #    raise NotListException(clist)
        for elem in clist:
            self.adjList[elem]=clist[elem]
            
    def getConnectionList(self):
        return self.adjList
    
    def getNodeList(self):
        return self.node
    
    
class NotListException(Exception):
    def __init__(self,obj):
        print(obj,"is not a list")