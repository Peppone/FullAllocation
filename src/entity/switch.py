'''
Created on 11 apr 2016

@author: peppone
'''

class switch(object):


    def __init__(self, idNum):
        '''
        Constructor
        '''
        self.idNum = int(idNum)
        self.links={}
        
    def getId(self):
        return self.idNum;
    
    def addConnection(self,idSrc,idDst,bw):
            self.links[(idSrc,idDst)]=float(bw);
            self.links[(idDst,idSrc)]=float(bw);
    def getConnections(self):
        return self.links
        
    
    
    