/*
* File Name: set_sched.c
* Author: pangbo
*
* This program can set both the scheduling policy 
* and parameters for the specified process. 
*/
#include <linux/types.h>
#include <linux/sched.h>
#include <errno.h>
#include <sched.h>
#include <stdio.h>

#include "sched_name.h"

void print_current_policy(pid_t pid){
    int policy;
    policy = sched_getscheduler(pid);
    if(policy>=0&&policy<=6){
        printf("Current policy of pid %d is:%s",pid,SCHED_NAME_LIST[policy]);
    }
}

int main(){
    struct sched_param param;
    pid_t pid;
    int policy,priority;
    printf("please input pid:");
    scanf("%d",&pid);
    // print_current_policy(pid);
    policy = sched_getscheduler(pid);
    if(policy>=0&&policy<=6)
        printf("Current policy of pid %d is:%s\n",pid,SCHED_NAME_LIST[policy]);
    else if(policy==-1){
        printf("error occurred: %d\n",errno);
        if(errno==ESRCH) printf("PID %d not found!\n",pid);
        return errno;
    }else printf("Unknown policy\n");
    for(int i=0;i<(sizeof(SCHED_NAME_LIST)/sizeof(SCHED_NAME_LIST[0]));i++){
        if(SCHED_NAME_LIST[i])
            printf("%d-%s\n",i,SCHED_NAME_LIST[i]);
    }
    printf("please input the new policy:\n");
    scanf("%d",&policy);
    printf("please input the new priority:\n");
    scanf("%d",&param.sched_priority);
    if(!sched_setscheduler(pid,policy,&param)){
        printf("finish!");
    }
}
