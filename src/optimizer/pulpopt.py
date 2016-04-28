'''
Created on 21 apr 2016

@author: peppone
'''
from pulp import *

class pulpopt(object):




    def __init__(self):
        '''
        Constructor
        '''
    def creatematrices(self,topology):
        amatrix={}
        bmatrix={}
        for src in topology:
            currentvertex = topology[src]
            for dest in currentvertex:
                    amatrix[(src,dest)]=1
                    bmatrix[(dest,src)]=1
        return [amatrix,bmatrix]
    
    def getlink(self,topology):
        link={}
        for src in topology:
            currentvertex = topology[src]
            for dest in currentvertex:
                link[src,dest]=currentvertex[dest]
        return link
            
    def initproblem(self,demandlist,topology):
        print(topology)
        prob = LpProblem("Multicommodity",LpMinimize)
        variables={}
        temp={}
        aggregatedemands={}
        
        for elem in demandlist:
            srcserver= elem[0][1]
            dstserver = elem[1][1]
            bw = elem[2]
            currentbw = aggregatedemands.get((srcserver,dstserver),0)
            currentbw += bw
            aggregatedemands[(srcserver,dstserver)]=currentbw
        links = self.getlink(topology)    
        flowvariable={}
        temp={}
        for i in aggregatedemands:
            temp = LpVariable.dicts("f",[(i,u,v) for (u,v) in links],0,aggregatedemands[i])
            flowvariable.update(temp)
        for i in aggregatedemands:
            src = i[0]
            dst = i[1]
            for v in topology:
                h=0
                if v == src:
                    h =  aggregatedemands[(src,dst)]
                elif v ==dst:
                    h = - aggregatedemands[(src,dst)]
                prob += (lpSum (flowvariable[i,u,k] for (u,k) in links if u == v) -\
                lpSum (flowvariable[i,u,k] for (u,k) in links if k == v))== h
        overprovisioning = LpVariable("e",0)
        '''capacity constraints'''
        for (u,v) in links:
            prob += lpSum (flowvariable[i,u,v] for i in aggregatedemands)<=links[(u,v)]+overprovisioning
        
        '''objective'''
        prob+= lpSum(flowvariable[(i,u,v)] for i in aggregatedemands for (u,v) in links)+overprovisioning
        res=prob.solve()   
        print("Result {}".format(res))      
        print (list((i,flowvariable[i].varValue) for i in flowvariable if flowvariable[i].varValue !=0))
        print (overprovisioning.varValue)
        