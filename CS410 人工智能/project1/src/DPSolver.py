import numpy as np
from BaseSolver import BaseSolver,Tester

GAP_COST = 2
MISMATCH_COST = 3

class DPSolver_2(BaseSolver):
    def __init__(self,seq):
        BaseSolver.__init__(self,seq)
        self.matrix = np.zeros(shape=(len(seq[0])+1,len(seq[1])+1),dtype=np.int32)
        self.steps = np.zeros(shape=(len(seq[0])+1,len(seq[1])+1),dtype=np.int32)
        self.align_cost = -1

    def solve(self):
        if self.align_cost != -1:
            return self.align_cost
        for xy in range(np.sum(self.matrix.shape) - 3, -1 ,-1):
            for x in range(max(0,xy-self.matrix.shape[1] + 1),min(xy + 1,self.matrix.shape[0])):
                y = xy - x
                # if x >= self.matrix.shape[0] or y >= self.matrix.shape[1]:
                #     break
                choices = np.full(shape=3,fill_value=2147483647,dtype=np.int32)
                if x < self.matrix.shape[0] - 1:
                    choices[0]=self.matrix[x+1,y]+GAP_COST
                if y < self.matrix.shape[1] - 1:
                    choices[1]=self.matrix[x,y+1]+GAP_COST
                if x < self.matrix.shape[0] - 1 and y < self.matrix.shape[1] - 1:
                    if(self.seq[0][x] == self.seq[1][y]):
                        choices[2]=self.matrix[x+1,y+1]
                    else:
                        choices[2]=self.matrix[x+1,y+1] + MISMATCH_COST
                self.matrix[x,y] = min(choices)
                self.steps[x,y] = np.argmin(choices)
        self.align_cost = self.matrix[0,0]
        return self.align_cost

    def align_seq(self):
        x,y = 0,0
        formated_seq1,formated_seq2 = "",""
        while x < len(self.seq[0]) or y < len(self.seq[1]):
            step = self.steps[x,y]
            if step == 0:
                formated_seq1 += self.seq[0][x]
                formated_seq2 += '*'
                x += 1
            elif step == 1:
                formated_seq1 += '*'
                formated_seq2 += self.seq[1][y]
                y += 1
            elif step == 2:
                formated_seq1 += self.seq[0][x]
                formated_seq2 += self.seq[1][y]
                x += 1
                y += 1
        return formated_seq1,formated_seq2

    def get_sub_cost(self,d1,d2):
        if self.align_cost == -1:
            self.solve()
        return self.matrix[d1,d2]

if __name__ == "__main__":
    query = input("Please input a sequence:")
    with open(f"DP_2_{query[:10]}.txt",'w') as f:
        tester = Tester(DPSolver_2,query,allow_skip=False,single_match=True,file=f)
        tester.run_test()