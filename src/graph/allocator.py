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
        vmlist= sorted(vmdict.items(), key = operator.itemgetter(1));
        print (vmlist)
        allocation = {}
        serverstatus={}
        server = sorted((elem[0] for elem in topology.items() if elem[1]=='server'))
        for s in server:
            serverstatus[s]=0
        serverlst = serverlist()
        for vm in vmlist:
            server = sorted(((elem[0],elem[1]) for elem in serverstatus.items()),key=(operator.itemgetter(1)))
            allocation[vm] = server[0][0]
            serverstatus[server[0][0]]=serverstatus[server[0][0]]+vm[1]
        for s in server:
            print ([(elem) for elem in allocation if allocation[elem]==int(s[0])])
        print (allocation)
        
    
    def bestfitallocation(self,vmdict,serverlist):
        pass
        