import numpy as np
from itertools import combinations
import random
from BaseSolver import BaseSolver,Tester

class GASolver_2(BaseSolver):
    def __init__(self,seq):
        BaseSolver.__init__(self,seq)
        self.align_cost = -1
        self.best_indv = None

    def solve(self):
        if self.align_cost != -1:
            return self.align_cost

        cur_indvs = [Individual.init_indv(self) for _ in range(50)]
        best_indv = None
        pre_min = 2147483647
        not_imporove_since = 0
        while not_imporove_since < 50:
            cost_list = np.fromiter((ind.cost for ind in cur_indvs),dtype=np.int32)
            max_cost = max(cost_list)
            min_cost = min(cost_list)
            best_indv = cur_indvs[np.argmin(cost_list)]
            # print(max_cost,min_cost)
            bias = int(max(1+max_cost*1.5 ,max_cost+2*min_cost))
            probablity_list = bias - cost_list
            choices_list = random.choices(cur_indvs,weights=probablity_list,k=60)
            cross_over_list = [choices_list[0:10],choices_list[10:20]]
            alive_list = choices_list[20:30]
            mutation_list = choices_list[30:40]
            move_mutation_list = choices_list[40:60]
            cur_indvs = alive_list + list(map(Individual.mutation,mutation_list)) + \
                    list(map(Individual.move,move_mutation_list)) + \
                    list(Individual.cross_over(*pair) for pair in zip(*cross_over_list)) + [best_indv]
            if min_cost < pre_min:
                pre_min = min_cost
                not_imporove_since = 0
            else:
                not_imporove_since += 1
        self.best_indv = best_indv
        self.align_cost = best_indv.cost
        return self.align_cost

    def align_seq(self):
        return self.best_indv.align_seq()

class Individual(object):
    def __init__(self,gap_pos,solver):
        self.solver = solver
        self.gap_pos = gap_pos
        self.cost = None
        formated_seqs = self.align_seq()
        self.cost = Individual.calc_cost(formated_seqs)
    
    @staticmethod
    def init_indv(solver):
        max_len = max(map(len,solver.seq)) + 3
        pos = list(list(np.random.randint(0,len(seq)+1,max_len-len(seq))) for seq in solver.seq)
        return Individual(pos,solver)

    def align_seq(self):
        max_len = max(map(lambda x:len(x[0])+len(x[1]),zip(self.solver.seq,self.gap_pos)))
        formated_seqs = [Individual.format_seq(*x,max_len) for x in zip(self.solver.seq,self.gap_pos)]
        return formated_seqs

    @staticmethod
    def calc_cost(formated_seqs):
        return sum(map(Individual.calc_cost_chr,zip(*formated_seqs)))

    @staticmethod
    def calc_cost_chr(chrs):
        return sum(map(Individual.calc_cost_pair,combinations(chrs,2)))

    @staticmethod
    def calc_cost_pair(pair):
        if pair[0] == pair[1]:
            return 0
        elif '*' in pair:
            return 2
        else:
            return 3

    @staticmethod
    def format_seq(seq,pos,length):
        split_pos = pos + [0,len(seq)]
        split_pos.sort()
        seq_slices = []
        for i in range(1,len(split_pos)):
            seq_slices.append(seq[split_pos[i-1]:split_pos[i]])
        res = '*'.join(seq_slices).ljust(length,'*')
        return res

    @staticmethod
    def cross_over(indv1,indv2):
        gap_pos = list(Individual.cross_over_single(*pair) for pair in zip(indv1.gap_pos,indv2.gap_pos))
        return Individual(gap_pos,indv1.solver)

    @staticmethod
    def cross_over_single(pos1,pos2):
        return pos1[:random.randrange(0,len(pos1))]+pos2[random.randrange(0,len(pos2)):]

    @staticmethod
    def mutation(indv1):
        gap_pos = [Individual.mutation_single(indv1.gap_pos[i].copy(),len(indv1.solver.seq[i])) for i in range(len(indv1.solver.seq))]
        return Individual(gap_pos,indv1.solver)

    @staticmethod
    def mutation_single(pos1,seq_len):
        if len(pos1) > 3:
            del pos1[random.randrange(0,len(pos1)-1)]
        pos1.append(random.randrange(0,seq_len))
        return pos1

    @staticmethod
    def move(indv1):
        gap_pos = [Individual.move_single(indv1.gap_pos[i].copy(),len(indv1.solver.seq[i])) for i in range(len(indv1.solver.seq))]
        return Individual(gap_pos,indv1.solver)

    @staticmethod
    def move_single(pos1,seq_len):
        index = random.randrange(0,len(pos1))
        pos1[index] = random.randrange(max(0,pos1[index]-2),min(seq_len+1,pos1[index]+2))
        return pos1

if __name__ == '__main__':
    query = input("Please input a sequence:")
    with open(f"GA_2_{query[:10]}.txt",'w') as f:
        tester = Tester(GASolver_2,query,allow_skip=False,single_match=True,file=f)
        tester.run_test()
