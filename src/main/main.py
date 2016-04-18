'''
Created on 11 apr 2016

@author: peppone
'''
from entity.server import serverlist
from fileio.extractor import extractor
from graph.allocator import allocator


if __name__ == '__main__':
    file = open("./vm.txt",'r')
    se = serverlist();
    extract = extractor()
    n = extract.adjextractor('/home/peppone/git/FullAllocation/src/main/topology.txt')
    v = extract.vmgraphextractor('/home/peppone/git/FullAllocation/src/main/vm.txt')
#     lst = n.getConnectionList()
#     for elem in lst:
#             print(elem,lst[elem])
#     lst = n.getNodeList()
#     print([(elem,lst [elem]) for elem in lst if lst[elem]=="server"])
#     
#     lst = v.getConnectionList()
#     for elem in lst:
#             print(elem,lst[elem])
#     lst = v.getNodeList()
#     print([(elem,lst [elem])for elem in lst])
    alloc=allocator()
    alloc.firstallocation(v.getNodeList(),n.getNodeList(),policy="bf")
    alloc.firstallocation(v.getNodeList(),n.getNodeList(),policy="wf")
        
    