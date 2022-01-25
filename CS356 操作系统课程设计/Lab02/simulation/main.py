import numpy as np
import json
from math import inf
from queue import Queue,PriorityQueue
import heapq

from numpy.core.numeric import Inf

from gantt import drawGantt
from scatter_plot import drawScatterPlot

TASK_NUM = 10
BRUST_TIME_MEAN = 150
# SINGLE_TEST = True
# MULTI_TEST = False
SINGLE_TEST = False
MULTI_TEST = True

class Task():
    def __init__(self,name,start_time,brust_time,fg = False):
        self.name = name
        self.start_time = start_time
        self.brust_time = brust_time
        self.finish_time = -1
        self.left_time = brust_time
        self.fg = fg
        self.time_quantum = None
        self.turnaround_time = None
        self.run_time_intervals = []
    def execute(self,cur_time):
        run_time = min(self.left_time,self.time_quantum)
        self.left_time -= run_time
        self.run_time_intervals.append((cur_time,cur_time+run_time))
        if self.left_time == 0 and self.finish_time == -1:
            self.finish_time = cur_time + run_time
            self.turnaround_time = self.finish_time - self.start_time
        return run_time
    def finished(self):
        return self.left_time == 0
    def set_fg(self,fg):
        self.fg = fg
    def __lt__(self,other):
        return self.start_time < other.start_time

class WRR_Task(Task):
    def __init__(self,name,start_time,brust_time,time_quantum = (100,10),fg = False):
        Task.__init__(self,name,start_time,brust_time,fg)
        self.fg = fg
        self.time_quantum_setting = time_quantum
        if fg:
            self.time_quantum = time_quantum[0]
        else:
            self.time_quantum = time_quantum[1]
    def set_fg(self,fg):
        Task.set_fg(self,fg)
        if fg:
            self.time_quantum = self.time_quantum_setting[0]
        else:
            self.time_quantum = self.time_quantum_setting[1]

class RR_Task(Task):
    def __init__(self,name,start_time,brust_time,time_quantum = 10,fg = False):
        Task.__init__(self,name,start_time,brust_time,fg)
        self.time_quantum = time_quantum

class FIFO_Task(Task):
    def __init__(self,name,start_time,brust_time,time_quantum = 0,fg = False):
        Task.__init__(self,name,start_time,brust_time,fg)
        self.time_quantum = inf

class Test():
    def __init__(self):
        self.task_queue = []
        self.task_list = None
        self.ready_queue = Queue()
        self.cur_time = 0
    def get_next_time(self):
        if self.ready_queue.empty():
            if len(self.task_queue) == 0:
                return -1
            else:
                return self.task_queue[0].start_time
        else:
            cur_task = self.ready_queue.get()
            next_time = self.cur_time + cur_task.execute(self.cur_time)
            if not cur_task.finished():
                self.ready_queue.put(cur_task)
            return next_time
    def update_ready(self):
        while len(self.task_queue)>0 and self.cur_time >= self.task_queue[0].start_time:
            self.ready_queue.put(heapq.heappop(self.task_queue))
    def simulate(self):
        self.cur_time = self.get_next_time()
        while self.cur_time != -1:
            self.update_ready()
            self.cur_time = self.get_next_time()
    def get_avg_turnaround_time(self):
        return sum([tsk.turnaround_time for tsk in self.task_list])/len(self.task_list)
    def get_avg_brust_time(self):
        return sum([tsk.brust_time for tsk in self.task_list])/len(self.task_list)
    def get_last_finish_time(self):
        return max([tsk.finish_time for tsk in self.task_list])
    def print_result(self,title = None):
        if title: print(title)
        for task in self.task_list:
            print("{}\t{}\t{}\t{}\t{}".format(
                task.name,task.start_time,task.finish_time,task.brust_time,task.finish_time-task.start_time))

class WRR_test(Test):
    def __init__(self,start_time_list,brust_time_list,time_quantum = (100,10)):
        Test.__init__(self)
        for i in range(len(start_time_list)):
            self.task_queue.append(WRR_Task(f"TASK-{i}",start_time_list[i],brust_time_list[i],time_quantum))
        self.task_queue[0].set_fg(True)
        self.task_list = tuple(self.task_queue)
        heapq.heapify(self.task_queue)

class RR_test(Test):
    def __init__(self,start_time_list,brust_time_list,time_quantum = 10):
        Test.__init__(self)
        for i in range(len(start_time_list)):
            self.task_queue.append(RR_Task(f"TASK-{i}",start_time_list[i],brust_time_list[i],time_quantum))
        self.task_queue[0].set_fg(True)
        self.task_list = tuple(self.task_queue)
        heapq.heapify(self.task_queue)

class FIFO_test(Test):
    def __init__(self,start_time_list,brust_time_list,time_quantum = 0):
        Test.__init__(self)
        for i in range(len(start_time_list)):
            self.task_queue.append(FIFO_Task(f"TASK-{i}",start_time_list[i],brust_time_list[i],time_quantum))
        self.task_queue[0].set_fg(True)
        self.task_list = tuple(self.task_queue)
        heapq.heapify(self.task_queue)

if __name__ == "__main__":
    if SINGLE_TEST:
        start_time_list = np.random.randint(0,500,TASK_NUM)
        brust_time_list = np.clip(np.round(np.random.normal(BRUST_TIME_MEAN,30,TASK_NUM)),5,200).astype(int)
        wrr = WRR_test(start_time_list,brust_time_list)
        rr_10 = RR_test(start_time_list,brust_time_list)
        rr_100 = RR_test(start_time_list,brust_time_list,time_quantum = 100)
        fifo = FIFO_test(start_time_list,brust_time_list)
        wrr.simulate()
        rr_10.simulate()
        rr_100.simulate()
        fifo.simulate()
        wrr.print_result("WRR")
        rr_10.print_result("RR with tq=10")
        rr_100.print_result("RR with tq=10")
        drawGantt(wrr.task_list,rr_10.task_list,rr_100.task_list,fifo.task_list)
    if MULTI_TEST:
        res_fore = []
        res_avg = []
        res_fin = []
        for btm in range(10,220):
            start_time_list = np.random.randint(0,500,TASK_NUM)
            brust_time_list = np.clip(np.round(np.random.normal(btm,30,TASK_NUM)),3,250).astype(int)
            wrr = WRR_test(start_time_list,brust_time_list)
            rr_10 = RR_test(start_time_list,brust_time_list)
            rr_100 = RR_test(start_time_list,brust_time_list,time_quantum = 100)
            fifo = FIFO_test(start_time_list,brust_time_list)
            wrr.simulate()
            rr_10.simulate()
            rr_100.simulate()
            fifo.simulate()
            res_fore.append((fifo.task_list[0].brust_time,fifo.task_list[0].turnaround_time,"fifo"))
            res_fore.append((rr_10.task_list[0].brust_time,rr_10.task_list[0].turnaround_time,"rr_10"))
            res_fore.append((rr_100.task_list[0].brust_time,rr_100.task_list[0].turnaround_time,"rr_100"))
            res_fore.append((wrr.task_list[0].brust_time,wrr.task_list[0].turnaround_time,"wrr"))

            res_avg.append((fifo.get_avg_brust_time(),fifo.get_avg_turnaround_time(),"fifo"))
            res_avg.append((rr_10.get_avg_brust_time(),rr_10.get_avg_turnaround_time(),"rr_10"))
            res_avg.append((rr_100.get_avg_brust_time(),rr_100.get_avg_turnaround_time(),"rr_100"))
            res_avg.append((wrr.get_avg_brust_time(),wrr.get_avg_turnaround_time(),"wrr"))

            res_fin.append((fifo.get_avg_brust_time(),fifo.get_last_finish_time(),"fifo"))
            res_fin.append((rr_10.get_avg_brust_time(),rr_10.get_last_finish_time(),"rr_10"))
            res_fin.append((rr_100.get_avg_brust_time(),rr_100.get_last_finish_time(),"rr_100"))
            res_fin.append((wrr.get_avg_brust_time(),wrr.get_last_finish_time(),"wrr"))
        drawScatterPlot(res_fore,"Brust Time of Foreground Task (msec)","Turnaround Time of Foreground Task (msec)")
        drawScatterPlot(res_avg,"Average Brust Time of Tasks (msec)","Average Turnaround Time of Tasks (msec)")
        drawScatterPlot(res_fin,"Average Brust Time of Tasks (msec)","Time to Finish all the Tasks (msec)")



