from time import time
from Dataset import *

class FakeFile(object):
    def write(self,*args,**kwargs):
        return 0
    def read(self,*args,**kwargs):
        return ''

class BaseSolver(object):
    def __init__(self,seq):
        self.seq = seq
        self.align_cost = -1
    
    def solve(self):
        raise NotImplementedError
    
    def get_align_cost(self,*args,**kwargs):
        if self.align_cost != -1:
            return self.align_cost
        else:
            return self.solve()

    def get_lower_evaluation(self,*args,**kwargs):
        return -1

    def align_seq(self):
        raise NotImplementedError
    
    def clean(self,*args,**kwargs):
        return

class Tester(object):
    def __init__(self,SolverClass,query,allow_skip = False,
            single_match = True,file = FakeFile(),hashbin_enabled = False,
            quite = False):
        self.query = query
        self.file = file
        self.SolverClass = SolverClass
        self.allow_skip = allow_skip
        self.skiped = 0
        self.min_cost = 2147483647
        self.min_align = None
        self.quite = quite
        if single_match:
            self.test_data = dataset_single()
            self.test_data_size = dataset_single_size()
        else:
            self.test_data = dataset_combination()
            self.test_data_size = dataset_combination_size()
        if hashbin_enabled:
            self.speedup_hashbin = SpeedupHashBin()
        else:
            self.speedup_hashbin = None
        
    def run_test(self,*args,**kwargs):
        f = self.file
        min_cost = 2147483647
        min_align = None

        total_loop = self.test_data_size
        loop = 0

        start_time = time()
        for comb in self.test_data:
            loop += 1
            if not self.quite:
                print(f"{loop}/{total_loop},min:{min_cost},time used:{int(time()-start_time)}sec")
            seqs = *comb,self.query
            solver = self.SolverClass(seqs)
            if self.allow_skip:
                if self.speedup_hashbin is not None:
                    lower_bound = solver.get_lower_evaluation(self.speedup_hashbin,min_cost)
                else:
                    lower_bound = solver.get_lower_evaluation()
                if lower_bound > min_cost:
                    if not self.quite:
                        print(f"Skipped! evaluated lower bound:{lower_bound}")
                    self.skiped += 1
                    continue
            cost = solver.solve(*args,**kwargs)
            align = solver.align_seq()
            if not self.quite:
                print(cost)
            f.write(str(cost)+'\n')
            for s in align:
                f.write(s)
                f.write('\n')
                if not self.quite:
                    print(s)
            if cost<min_cost:
                min_cost = cost
                min_align = align

        self.time_used = time()-start_time
        self.min_cost = min_cost
        self.min_align = min_align
        print("RESULT".center(60,'*'))
        print(f"time used:{int(self.time_used)}sec")
        print(min_cost)
        f.write(str(min_cost)+'\n')
        for s in min_align:
                f.write(s)
                f.write('\n')
                print(s)

class SpeedupHashBin(object):
    def __init__(self,*args,**kwargs):
        self.hashbin = dict()
    
    def __calc_hash(self,obj):
        return min(hash(tuple(obj)),hash(tuple(reversed(obj))))

    def __on_hashhit(self):
        # for performance analysis only
        pass

    def __getitem__(self,index):
        # item = self.hashbin.get(self.__calc_hash(index),None)
        # if item is not None:
        #     self.__on_hashhit()
        # return item
        return self.hashbin.get(self.__calc_hash(index),None)

    def __setitem__(self,index,item):
        self.hashbin[self.__calc_hash(index)] = item

