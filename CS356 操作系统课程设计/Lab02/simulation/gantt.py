import matplotlib.pyplot as plt
import json
from numpy.lib.function_base import average
import seaborn as sns

def drawGantt(wrr_task_list,rr10_task_list,rr100_task_list,fifo_task_list):
    time_list = []
    task_name_list = [task.name for task in wrr_task_list]
    color_list = sns.color_palette("husl", len(task_name_list))
    task_color = dict(zip(task_name_list,color_list))
    ystates=[]
    location=0
    plt.figure(figsize=(10, 5))

    for i in range(len(wrr_task_list)):
        task = wrr_task_list[i]
        for startTime,finishTime in task.run_time_intervals:
            intervalTime = finishTime-startTime
            location = startTime
            if i != 0:
                plt.barh(4,intervalTime,0.9,location,color = task_color[task.name], align="center", label = task.name)
            else:
                plt.barh(5,intervalTime,0.9,location,color = task_color[task.name], align="center", label = task.name)

                
    for i in range(len(rr10_task_list)):
        task = rr10_task_list[i]
        for startTime,finishTime in task.run_time_intervals:
            intervalTime = finishTime-startTime
            location = startTime
            if i != 0:
                plt.barh(7,intervalTime,0.9,location,color = task_color[task.name], align="center", label = task.name)
            else:
                plt.barh(8,intervalTime,0.9,location,color = task_color[task.name], align="center", label = task.name)
    

    for i in range(len(rr100_task_list)):
        task = rr100_task_list[i]
        for startTime,finishTime in task.run_time_intervals:
            intervalTime = finishTime-startTime
            location = startTime
            if i != 0:
                plt.barh(10,intervalTime,0.9,location,color = task_color[task.name], align="center", label = task.name)
            else:
                plt.barh(11,intervalTime,0.9,location,color = task_color[task.name], align="center", label = task.name)

    for i in range(len(fifo_task_list)):
        task = fifo_task_list[i]
        for startTime,finishTime in task.run_time_intervals:
            intervalTime = finishTime-startTime
            location = startTime
            if i != 0:
                plt.barh(13,intervalTime,0.9,location,color = task_color[task.name], align="center", label = task.name)
            else:
                plt.barh(14,intervalTime,0.9,location,color = task_color[task.name], align="center", label = task.name)
    plt.barh(12,0,0.9,align="center")

    text_x = sum(plt.xlim())/2
    plt.text(text_x,6,s="WRR",ha="center",va="top")
    plt.axhline(6.4,color='k',linestyle='solid')
    plt.text(text_x,9,s="RR with time quantum 10ms",ha="center",va="top")
    plt.axhline(9.4,color='k',linestyle='solid')
    plt.text(text_x,12,s="RR with time quantum 100ms",ha="center",va="top")
    plt.axhline(12.4,color='k',linestyle='solid')
    plt.text(text_x,15,s="FIFO",ha="center",va="top")
    plt.axhline(15.4,color='k',linestyle='solid')

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    by_label = dict(sorted(by_label.items(),key= lambda item:int(item[0][4:])))
    # plt.legend(by_label.values(), by_label.keys())
    # plt.legend()
    plt.yticks([])
    plt.xlabel("Time(msec)")

    plt.show()
