import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
 
sched_name = {
    "wrr":"WRR",
    "rr_10":"RR(tq=10ms)",
    "rr_100":"RR(tq=100ms)",
    "fifo":"FIFO"
}

def drawScatterPlot(res_data,xlabel = "",ylabel = ""):
    sns.set()
    data = pd.DataFrame(data=res_data,columns=("brust_time","turnaround_time","sched"))
    sns.scatterplot(x = "brust_time", y = "turnaround_time",data=data, hue='sched',style='sched',s=100,)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    handles, labels = plt.gca().get_legend_handles_labels()
    labels = [sched_name[lb] for lb in labels]
    by_label = dict(zip(labels, handles))
    by_label = dict(sorted(by_label.items()))
    plt.legend(by_label.values(), by_label.keys())
    plt.show()


if __name__ == "__main__":
    drawScatterPlot("test_result.csv")