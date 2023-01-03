/*
* File Name: get_interval.c
* Author: pangbo
*
* The program will output the time slice
* length of the specified process.
*/

#include <linux/types.h>
#include <linux/sched.h>
#include <errno.h>
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>

int main(){
    pid_t pid;
    struct timespec t;
    printf("Please input pid:\n");
    scanf("%d",&pid);
    sched_rr_get_interval(pid, &t);
    printf("Time slice of pid %d is %ld msec(s).\n",pid,t.tv_nsec/1000000);
}