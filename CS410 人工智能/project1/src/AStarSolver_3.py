from queue import PriorityQueue
import numpy as np
from BaseSolver import BaseSolver,Tester
try:
    from DPSolver_numba import DPSolver_2_numba as DPSolver_2
except ModuleNotFoundError:
    from DPSolver import DPSolver_2

GAP_COST = 2
MISMATCH_COST = 3

class AStarSolver_3(BaseSolver):
    def __init__(self,seq):
        BaseSolver.__init__(self,seq)
        self.visited = None
        self.que = None
        self.target_node = None
        self.init_node = None
        self.searched_node_count = 0
        self.align_cost = -1
        
        self.DP_xy = None
        self.DP_xz = None
        self.DP_yz = None

        self.DP2_evaluate = -1
        # self.DP2_evaluate = self.DP_xy.align_cost + self.DP_xz.align_cost + self.DP_yz.align_cost

    def get_lower_evaluation(self,speedup = None,cur_min = None):
        if self.DP2_evaluate != -1:
            return self.DP2_evaluate
        else:
            xy_cost,xz_cost,yz_cost = None,None,None
            if speedup is not None:
                xy_cost = speedup[(self.seq[0],self.seq[1])]
                xz_cost = speedup[(self.seq[0],self.seq[2])]
                yz_cost = speedup[(self.seq[1],self.seq[2])]
                if cur_min is not None:
                    cost = sum(filter(lambda c:c is not None,(xy_cost,xz_cost,yz_cost)))
                    if  cost > cur_min:
                        return cost
            if xy_cost is None:
                if self.DP_xy is None:
                    self.DP_xy = DPSolver_2((self.seq[0],self.seq[1]))
                xy_cost = self.DP_xy.solve()
                if speedup is not None:
                    speedup[(self.seq[0],self.seq[1])] = xy_cost
            if xz_cost is None:
                if self.DP_xz is None:
                    self.DP_xz = DPSolver_2((self.seq[0],self.seq[2]))
                xz_cost = self.DP_xz.solve()
                if speedup is not None:
                    speedup[(self.seq[0],self.seq[2])] = xz_cost
            if yz_cost is None:
                if self.DP_yz is None:
                    self.DP_yz = DPSolver_2((self.seq[1],self.seq[2]))
                yz_cost = self.DP_yz.solve()
                if speedup is not None:
                    speedup[(self.seq[1],self.seq[2])] = yz_cost
            self.DP2_evaluate = xy_cost+xz_cost+yz_cost
            return self.DP2_evaluate

    def solve(self):
        if self.align_cost != -1:
            return self.align_cost

        if self.DP_xy is None:
            self.DP_xy = DPSolver_2((self.seq[0],self.seq[1]))
            self.DP_xy.solve()
        if self.DP_xz is None:
            self.DP_xz = DPSolver_2((self.seq[0],self.seq[2]))
            self.DP_xz.solve()
        if self.DP_yz is None:
            self.DP_yz = DPSolver_2((self.seq[1],self.seq[2]))
            self.DP_yz.solve()
        
        self.visited = np.zeros(shape=(len(self.seq[0])+1,len(self.seq[1])+1,len(self.seq[2])+1),dtype=bool)
        self.que = PriorityQueue()
        self.init_node = AStarNode(0,(0,0,0),None,self)
        self.que.put(self.init_node)
        while True:
            cur_node = self.que.get()
            if cur_node.is_target():
                self.align_cost = cur_node.cost
                self.target_node = cur_node
                return self.align_cost
            else:
                for node in cur_node.expand():
                    self.que.put(node)
    
    def align_seq(self):
        seq1,seq2,seq3 = "","",""
        cur_node = self.target_node
        next_pos = None
        cur_pos = None
        while next_pos != (0,0,0):
            cur_pos = cur_node.pos
            next_pos = cur_node.parent.pos
            if next_pos[0] != cur_pos[0]:
                seq1 += self.seq[0][cur_pos[0]-1]
            else:
                seq1 += '*'
            if next_pos[1] != cur_pos[1]:
                seq2 += self.seq[1][cur_pos[1]-1]
            else:
                seq2 += '*'
            if next_pos[2] != cur_pos[2]:
                seq3 += self.seq[2][cur_pos[2]-1]
            else:
                seq3 += '*'
            cur_node = cur_node.parent
        return (seq1[::-1],seq2[::-1],seq3[::-1])

class AStarNode(object):
    def __init__(self,cost,pos,parent,solver):
        self.solver = solver
        self.parent = parent
        self.pos = pos
        self.cost = cost
        self.heur = self.heuristic()
        self.evalueated_cost = self.cost + self.heur

    def __lt__(self,other):
        return self.evalueated_cost < other.evalueated_cost

    def heuristic(self):
        return self.solver.DP_xy.get_sub_cost(self.pos[0],self.pos[1]) + \
                self.solver.DP_xz.get_sub_cost(self.pos[0],self.pos[2]) + \
                self.solver.DP_yz.get_sub_cost(self.pos[1],self.pos[2])

    def is_target(self):
        return self.pos[0] == len(self.solver.seq[0]) and \
                self.pos[1] == len(self.solver.seq[1]) and \
                self.pos[2] == len(self.solver.seq[2])

    def Node(self,cost,pos):
        return AStarNode(cost,pos,self,self.solver)

    def expand(self):
        if self.solver.visited[self.pos]:
            return []
        else:
            self.solver.visited[self.pos] = True
            self.solver.searched_node_count += 1
            seq = self.solver.seq
            x,y,z = self.pos
            x_max,y_max,z_max = map(len,seq)
            expand_nodes = []
            if x < x_max:
                next_pos = x+1,y,z
                expand_nodes.append(self.Node(self.cost+GAP_COST * 2,next_pos))
            if y < y_max:
                next_pos = x,y+1,z
                expand_nodes.append(self.Node(self.cost+GAP_COST * 2,next_pos))
            if z < z_max:
                next_pos = x,y,z+1
                expand_nodes.append(self.Node(self.cost+GAP_COST * 2,next_pos))
                
            if x < x_max and y < y_max:
                next_pos = x+1,y+1,z
                if seq[0][x] == seq[1][y]:
                    expand_nodes.append(self.Node(self.cost + GAP_COST * 2,next_pos))
                else:
                    expand_nodes.append(self.Node(self.cost + GAP_COST * 2 + MISMATCH_COST,next_pos))
            if x < x_max and z < z_max:
                next_pos = x+1,y,z+1
                if seq[0][x] == seq[2][z]:
                    expand_nodes.append(self.Node(self.cost + GAP_COST * 2,next_pos))
                else:
                    expand_nodes.append(self.Node(self.cost + GAP_COST * 2 + MISMATCH_COST,next_pos))
            if y < y_max and z < z_max:
                next_pos = x,y+1,z+1
                if seq[1][y] == seq[2][z]:
                    expand_nodes.append(self.Node(self.cost + GAP_COST * 2,next_pos))
                else:
                    expand_nodes.append(self.Node(self.cost + GAP_COST * 2 + MISMATCH_COST,next_pos))

            if x < x_max and y < y_max and z < z_max:
                next_pos = x+1,y+1,z+1
                mismatch = sum((seq[0][x] != seq[1][y],seq[0][x] != seq[2][z],seq[1][y] != seq[2][z]))
                expand_nodes.append(self.Node(self.cost + MISMATCH_COST * mismatch,next_pos))
            
            return expand_nodes

if __name__ == '__main__':
    query = input("Please input a sequence:")
    with open(f"AStar_3_{query[:10]}.txt",'w') as f:
        tester = Tester(AStarSolver_3,query,allow_skip=True,single_match=False,file=f,hashbin_enabled=True,quite=True)
        tester.run_test()
