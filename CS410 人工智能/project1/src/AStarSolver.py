from queue import PriorityQueue
import numpy as np

from BaseSolver import BaseSolver,Tester

GAP_COST = 2
MISMATCH_COST = 3



class AStarSolver_2(BaseSolver):
    def __init__(self,seq):
        BaseSolver.__init__(self,seq)
        self.visited = np.zeros(shape=(len(seq[0])+1,len(seq[1])+1),dtype=np.bool)
        # self.heuristic = np.full(shape=self.visited.shape,fill_value=-1,dtype=np.int32)
        self.que = PriorityQueue()
        self.init_node = AStarNode(0,(0,0),None,self)
        self.target_node = None
        self.searched_node_count = 0
        self.match_cost = -1
    
    def solve(self):
        self.que.put(self.init_node)
        while True:
            cur_node = self.que.get()
            # print(cur_node.pos)
            if cur_node.is_target():
                self.match_cost = cur_node.cost
                self.target_node = cur_node
                return self.match_cost
            else:
                for node in cur_node.expand():
                    self.que.put(node)
    
    def align_seq(self):
        seq1 = ""
        seq2 = ""
        cur_node = self.target_node
        next_pos = None
        cur_pos = None
        while next_pos != (0,0):
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
            cur_node = cur_node.parent
        return (seq1[::-1],seq2[::-1])

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
        return 2*abs((len(self.solver.seq[0])-self.pos[0])-((len(self.solver.seq[1])-self.pos[1])))

    def is_target(self):
        return self.pos[0] == len(self.solver.seq[0]) and self.pos[1] == len(self.solver.seq[1])

    def Node(self,cost,pos):
        return AStarNode(cost,pos,self,self.solver)

    def expand(self):
        if self.solver.visited[self.pos]:
            return []
        else:
            self.solver.visited[self.pos] = True
            self.solver.searched_node_count += 1
            expand_nodes = []
            if self.pos[0] < len(self.solver.seq[0]):
                next_pos = self.pos[0]+1,self.pos[1]
                expand_nodes.append(self.Node(self.cost+GAP_COST,next_pos))
            if self.pos[1] < len(self.solver.seq[1]):
                next_pos = self.pos[0],self.pos[1]+1
                expand_nodes.append(self.Node(self.cost+GAP_COST,next_pos))
            if self.pos[0] < len(self.solver.seq[0]) and self.pos[1] < len(self.solver.seq[1]):
                next_pos = self.pos[0]+1,self.pos[1]+1
                if self.solver.seq[0][self.pos[0]] == self.solver.seq[1][self.pos[1]]:
                    expand_nodes.append(self.Node(self.cost,next_pos))
                else:
                    expand_nodes.append(self.Node(self.cost + MISMATCH_COST,next_pos))
            return expand_nodes



if __name__ == "__main__":
    query = input("Please input a sequence:")
    with open(f"AStar_2_{query[:10]}.txt",'w') as f:
        tester = Tester(AStarSolver_2,query,allow_skip=False,single_match=True,file=f)
        tester.run_test()
