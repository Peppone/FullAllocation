'''
Created on 11 apr 2016

@author: peppone
'''

class vm(object):
    '''
    classdocs
    '''


    def __init__(self, idNum, cpu):
        self.idNum = int (idNum);
        self.cpu = float(cpu);
    
    def getId(self):
        return self.idNum;
    
    def setId(self,idNum):
        self.idNum = int (idNum);
        
    def getCpu(self):
        return self.cpu;
    
    def setCpu (self,cpu):
        self.cpu = float (cpu);
        