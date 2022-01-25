import numpy as np
from BaseSolver import BaseSolver,Tester
from numba import jit,prange
from DPSolver import DPSolver_2

GAP_COST = 2
MISMATCH_COST = 3
NUMBA_CACHE_ENABLED = True

class DPSolver_2_numba(DPSolver_2):
    def solve(self):
        if self.align_cost != -1:
            return self.align_cost
        self.align_cost = self.solve_speedup(self.matrix,self.steps,self.seq)
        return self.align_cost

    @staticmethod
    @jit(nopython=True,parallel=False,cache=NUMBA_CACHE_ENABLED)
    def solve_speedup(matrix,steps,seq):
        for xy in range(np.sum(np.array(matrix.shape)) - 3, -1 ,-1):
            for x in prange(max(0,xy - matrix.shape[1] + 1),min(xy + 1,matrix.shape[0])):
                y = xy - x
                choices = np.full(shape=3,fill_value=2147483647,dtype=np.int32)
                if x < matrix.shape[0] - 1:
                    choices[0]=matrix[x+1,y]+GAP_COST
                if y < matrix.shape[1] - 1:
                    choices[1]=matrix[x,y+1]+GAP_COST
                if x < matrix.shape[0] - 1 and y < matrix.shape[1] - 1:
                    if(seq[0][x] == seq[1][y]):
                        choices[2]=matrix[x+1,y+1]
                    else:
                        choices[2]=matrix[x+1,y+1] + MISMATCH_COST
                matrix[x,y] = min(choices)
                steps[x,y] = np.argmin(choices)
        return matrix[0,0]

if __name__ == "__main__":
    query = input("Please input a sequence:")
    with open(f"DP_2_{query[:10]}.txt",'w') as f:
        tester = Tester(DPSolver_2_numba,query,allow_skip=False,single_match=True,file=f)
        tester.run_test()