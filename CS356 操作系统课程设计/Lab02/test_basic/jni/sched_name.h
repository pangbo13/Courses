#ifndef __SCHED_NAME_H
#define __SCHED_NAME_H

#define SCHED_NORMAL		0
#define SCHED_FIFO		1
#define SCHED_RR		2
#define SCHED_BATCH		3
#define SCHED_WRR       6
#define SCHED_IDLE		5

const char* SCHED_NAME_LIST[]={
    "SCHED_NORMAL",
    "SCHED_FIFO",
    "SCHED_RR",
    "SCHED_BATCH",
    NULL,
    "SCHED_IDLE",
    "SCHED_WRR"
};

#endif