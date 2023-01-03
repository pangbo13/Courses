import numpy as np
try:
    from DPSolver_numba import DPSolver_2_numba as DPSolver_2
except ModuleNotFoundError:
    from DPSolver import DPSolver_2
from BaseSolver import BaseSolver,Tester

GAP_COST = 2
MISMATCH_COST = 3

class DPSolver_3(BaseSolver):
    def __init__(self,seq):
        BaseSolver.__init__(self,seq)
        self.matrix = None
        self.steps = None
        self.align_cost = -1
        self.DP2_evaluate = -1
    
    def get_lower_evaluation(self,speedup = None,cur_min = None):
        if self.DP2_evaluate != -1:
            return self.DP2_evaluate
        else:
            if speedup is None:
                seq = self.seq
                DP2 = DPSolver_2((seq[0],seq[1])),DPSolver_2((seq[0],seq[2])),DPSolver_2((seq[1],seq[2]))
                self.DP2_evaluate = sum(map(lambda s: s.solve(),DP2))
                return self.DP2_evaluate
            else:
                xy_cost = speedup[(self.seq[0],self.seq[1])]
                xz_cost = speedup[(self.seq[0],self.seq[2])]
                yz_cost = speedup[(self.seq[1],self.seq[2])]
                if cur_min is not None:
                    cost = sum(filter(lambda c:c is not None,(xy_cost,xz_cost,yz_cost)))
                    if cost > cur_min:
                        return cost
                if xy_cost is None:
                    xy_cost = DPSolver_2((self.seq[0],self.seq[1])).solve()
                    if speedup is not None:
                        speedup[(self.seq[0],self.seq[1])] = xy_cost
                if xz_cost is None:
                    xz_cost = DPSolver_2((self.seq[0],self.seq[2])).solve()
                    if speedup is not None:
                        speedup[(self.seq[0],self.seq[2])] = xz_cost
                if yz_cost is None:
                    yz_cost = DPSolver_2((self.seq[1],self.seq[2])).solve()
                    if speedup is not None:
                        speedup[(self.seq[1],self.seq[2])] = yz_cost
                self.DP2_evaluate = xy_cost+xz_cost+yz_cost
                return self.DP2_evaluate
    
    def solve(self):
        if self.align_cost != -1:
            return self.align_cost
        seq = self.seq
        max_x = len(seq[0])
        max_y = len(seq[1])
        max_z = len(seq[2])

        self.matrix = np.zeros((max_x+1,max_y+1,max_z+1),dtype=np.int32)
        self.steps = np.full(self.matrix.shape,fill_value=-1,dtype=np.int8)
        for xyz in range(max_x+max_y+max_z-1,-1,-1):
            for x in range(max(0,xyz-max_y-max_z),min(xyz,max_x)+1):
                yz = xyz - x
                for y in range(max(0,yz-max_z),min(yz,max_y)+1):
                    z = yz - y
                    choices = np.full(7,fill_value=2147483647,dtype=np.int32)
                    if x < max_x:
                        choices[0] = self.matrix[x+1, y, z] + GAP_COST * 2
                    if y < max_y:
                        choices[1] = self.matrix[x, y+1, z] + GAP_COST * 2
                    if z < max_z:
                        choices[2] = self.matrix[x, y, z+1] + GAP_COST * 2
                    if x < max_x and y < max_y:
                        if seq[0][x] == seq[1][y]:
                            choices[3] = self.matrix[x+1, y+1, z] + GAP_COST * 2
                        else:
                            choices[3] = self.matrix[x+1, y+1, z] + GAP_COST * 2 + MISMATCH_COST
                    if x < max_x and z < max_z:
                        if seq[0][x] == seq[2][z]:
                            choices[4] = self.matrix[x+1, y, z+1] + GAP_COST * 2
                        else:
                            choices[4] = self.matrix[x+1, y, z+1] + GAP_COST * 2 + MISMATCH_COST
                    if y < max_y and z < max_z:
                        if seq[1][y] == seq[2][z]:
                            choices[5] = self.matrix[x, y+1, z+1] + GAP_COST * 2
                        else:
                            choices[5] = self.matrix[x, y+1, z+1] + GAP_COST * 2 + MISMATCH_COST
                    if x < max_x and y < max_y and z < max_z:
                        choices[6] = self.matrix[x+1, y+1, z+1] + MISMATCH_COST * \
                            sum((seq[0][x] != seq[1][y],seq[0][x] != seq[2][z],seq[1][y] != seq[2][z]))
                    self.steps[x,y,z] = np.argmin(choices)
                    self.matrix[x,y,z] = min(choices)
        self.align_cost = self.matrix[0,0,0]
        return self.align_cost
    
    def align_seq(self):
        seq = self.seq
        x,y,z = [0,0,0]
        movement = ((1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1),(1,1,1))
        max_x = len(seq[0])
        max_y = len(seq[1])
        max_z = len(seq[2])
        seq1,seq2,seq3 = "","",""
        while x < max_x or y < max_y or z < max_z:
            move = movement[self.steps[x,y,z]]
            x += move[0]
            y += move[1]
            z += move[2]
            if move[0] == 0:
                seq1 += "*"
            else:
                seq1 += seq[0][x-1]
            if move[1] == 0:
                seq2 += "*"
            else:
                seq2 += seq[1][y-1]
            if move[2] == 0:
                seq3 += "*"
            else:
                seq3 += seq[2][z-1]
        return seq1,seq2,seq3

if __name__ == "__main__":
    query = input("Please input a sequence:")
    with open(f"DP_3_{query[:10]}.txt",'w') as f:
        tester = Tester(DPSolver_3,query,allow_skip=True,single_match=False,file=f,hashbin_enabled=True,quite=True)
        # tester = Tester(DPSolver_3,query,allow_skip=False,single_align=False,file=f,speedup_enable=False)
        tester.run_test()
