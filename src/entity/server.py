'''
Created on 11 apr 2016

@author: peppone
'''

class serverlist(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.vmList = {};
        self.cpu = {}
    
    def setvmlist(self,vmlist):
        self.vmList=vmlist
        
    def getvmlist(self):
        return self.vmList        
    
    def setcpu(self,cpu):
        self.cpu=cpu
        
    def getcpu(self):
        return self.cpu
    
    def addVM(self,vm,server,cpu):
        if vm in self.vmList:
            raise Exception("VM {} already allocated".format(vm))
        self.vmList[vm]=server;
        currentcpu = self.cpu.get(server,0)
        self.cpu[server]= currentcpu + cpu
    
    def setServerOccupancy(self,server,occupancy=0):
        self.cpu[server]=occupancy
        
    def removeVM(self,vm,cpu):
        if vm not in self.vmList:
            raise Exception("VM {} not present".format(vm))
        server = self.vmList.get(vm)
        self.vmList[vm]=None
        self.cpu[server] = self.cpu - cpu;
            
    def getAvailableCpu(self,server):
        return 100-self.cpu[server]
    
    def getVMList(self):
        return self.vmList;
    
    def getCpu(self):
        return self.cpu
        