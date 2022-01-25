import numpy as np
from numba import jit,prange

from DPSolver_3 import DPSolver_3
from BaseSolver import BaseSolver,Tester

GAP_COST = 2
MISMATCH_COST = 3
NUMBA_CACHE_ENABLED = True

class DPSolver_3_numba(DPSolver_3):
    def solve(self):
        if self.align_cost != -1:
            return self.align_cost
        seq = self.seq
        max_x = len(seq[0])
        max_y = len(seq[1])
        max_z = len(seq[2])

        self.matrix = np.zeros((max_x+1,max_y+1,max_z+1),dtype=np.int32)
        self.steps = np.full(self.matrix.shape,fill_value=-1,dtype=np.int8)
    
        self.solve_speedup(self.matrix,self.steps,self.seq)
       
        self.align_cost = self.matrix[0,0,0]
        return self.align_cost
    
    @staticmethod
    @jit(nopython=True,cache=NUMBA_CACHE_ENABLED)
    def solve_speedup(matrix,steps,seq):
        max_x = len(seq[0])
        max_y = len(seq[1])
        max_z = len(seq[2])
        seq1,seq2,seq3 = seq
        for xyz in range(max_x+max_y+max_z-1,-1,-1):
            for x in range(max(0,xyz-max_y-max_z),min(xyz,max_x)+1):
                yz = xyz - x
                for y in range(max(0,yz-max_z),min(yz,max_y)+1):
                    z = yz - y
                    choices = np.full(7,fill_value=2147483647,dtype=np.int32)
                    if x < max_x:
                        choices[0] = matrix[x+1, y, z] + GAP_COST * 2
                    if y < max_y:
                        choices[1] = matrix[x, y+1, z] + GAP_COST * 2
                    if z < max_z:
                        choices[2] = matrix[x, y, z+1] + GAP_COST * 2
                    if x < max_x and y < max_y:
                        if seq1[x] == seq2[y]:
                            choices[3] = matrix[x+1, y+1, z] + GAP_COST * 2
                        else:
                            choices[3] = matrix[x+1, y+1, z] + GAP_COST * 2 + MISMATCH_COST
                    if x < max_x and z < max_z:
                        if seq1[x] == seq3[z]:
                            choices[4] = matrix[x+1, y, z+1] + GAP_COST * 2
                        else:
                            choices[4] = matrix[x+1, y, z+1] + GAP_COST * 2 + MISMATCH_COST
                    if y < max_y and z < max_z:
                        if seq2[y] == seq3[z]:
                            choices[5] = matrix[x, y+1, z+1] + GAP_COST * 2
                        else:
                            choices[5] = matrix[x, y+1, z+1] + GAP_COST * 2 + MISMATCH_COST
                    if x < max_x and y < max_y and z < max_z:
                        choices[6] = matrix[x+1, y+1, z+1] + MISMATCH_COST * \
                            np.sum(np.array((seq1[x] != seq2[y],seq1[x] != seq3[z],seq2[y] != seq3[z])))
                    steps[x,y,z] = np.argmin(choices)
                    matrix[x,y,z] = min(choices)

if __name__ == "__main__":
    query = input("Please input a sequence:")
    with open(f"DP_3_{query[:10]}.txt",'w') as f:
        tester = Tester(DPSolver_3_numba,query,allow_skip=True,single_match=False,file=f,hashbin_enabled=True,quite=True)
        tester.run_test()
