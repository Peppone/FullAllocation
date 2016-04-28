'''
Created on 11 apr 2016

@author: peppone
'''
import cplex
import os
import pulp

from entity.server import serverlist
from fileio.extractor import extractor
from graph.allocator import allocator
from optimizer.pulpopt import pulpopt


if __name__ == '__main__':
    file = open("./vm.txt",'r')
    se = serverlist();
    extract = extractor()
   # n = extract.adjextractor('/home/peppone/git/FullAllocation/src/main/topology.txt')
   # v = extract.vmgraphextractor('/home/peppone/git/FullAllocation/src/main/vm.txt')
    n = extract.adjextractor('/home/peppone/git/FullAllocation/src/main/topologytest.txt')
    v = extract.vmgraphextractor('/home/peppone/git/FullAllocation/src/main/vmtest.txt')
    os.environ["GUROBI_HOME"]="/home/peppone/gurobi651/linux64/"
    os.environ["PATH"]= os.environ["PATH"]+":/home/peppone/gurobi651/linux64/bin"
    os.environ["LD_LIBRARY_PATH"]="/home/peppone/ibm/ILOG/CPLEX_Studio1262/opl/bin/x86-64_linux/:"\
     +"/home/peppone/gurobi651/linux64/lib/"
    print (os.environ.get("LD_LIBRARY_PATH"))
    print (os.environ.get("PATH"))
    
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
    bfallocation = alloc.firstallocation(v.getNodeList(),n.getNodeList(),policy="bf")
    wfallocation= alloc.firstallocation(v.getNodeList(),n.getNodeList(),policy="wf")
    demandsdict= extract.demandgeneration(v.getConnectionList(), wfallocation)
    solver=cplex.Cplex();
    solver.variables.add([float(i) for i in range(0,2)],names=["x{}".format(i) for i in range(0,2)])
    solver.objective.set_linear(0,1)
    solver.objective.set_linear(1,1)
    solver.linear_constraints.add(lin_expr = [cplex.SparsePair(ind=[0,1],val=[1,1]),\
                                             cplex.SparsePair(ind=["x0","x1"],val=[1,-1]),\
                                             cplex.SparsePair(ind=["x0","x1"],val=[1,0])],\
                                             senses = ["L","G","R"],rhs=[1,0,0.5],range_values=[0,0,0])
    #solver.read("model.lp")
    solver.get_problem_name();
#     for i in range(0,2):
#         for j in range(0,2):
#             print (solver.linear_constraints.get_coefficients(i,j),solver.linear_constraints.get_num() )
    solver.solve()
    pulp.gurobi_path="gurobi.sh"
    print(solver.solution.get_objective_value())
    print (solver.solution.get_values())
    problemsolver=pulpopt()
    problemsolver.initproblem(demandsdict,n.getConnectionList())
    
    print(len(problemsolver.getlink(n.getConnectionList())))
        
    