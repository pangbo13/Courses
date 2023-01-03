/*
* File Name: test_basic.c
* Author: pangbo
* 
* This program will automatically search for the PID of the test APP, 
* read its scheduling status and provide scheduling adjustment functions.
*/

#include <sys/types.h>
#include <linux/types.h>
#include <linux/sched.h>
#include <errno.h>
#include <sched.h>
#include <dirent.h>
#include <stdio.h>
#include <string.h>
 
#include "sched_name.h"

#define BUF_SIZE 1024

int get_pid_by_cmd(pid_t *pid, char *task_name)
{
    DIR *dir;
    struct dirent *ptr;
    FILE *fp;
    char filepath[50];
    char buf[BUF_SIZE];
    int found = 0;
 
    dir = opendir("/proc"); 
    if (dir != NULL)
    {
        while ((ptr = readdir(dir)) != NULL && !found)
        {
            if ((strcmp(ptr->d_name, ".") == 0) || (strcmp(ptr->d_name, "..") == 0))
                continue;
            if (DT_DIR != ptr->d_type)
                continue;
            sprintf(filepath, "/proc/%s/cmdline", ptr->d_name);
            fp = fopen(filepath, "r");
            if (fp)
            {
                if( fgets(buf, BUF_SIZE-1, fp)== NULL ){
                    fclose(fp);
                    continue;
                }
                if (!strcmp(buf, task_name)){
                    sscanf(ptr->d_name, "%d", pid);
                    found = 1;
                }
                fclose(fp);
            }
        }
        closedir(dir);
    }
    return found;
}

int get_process_group(pid_t pid){
    //0-fg 1-bg
    char buf[BUF_SIZE];
    char task_cgroup[64];
    char filepath[50];
    FILE *fp;
    sprintf(filepath, "/proc/%d/cgroup", pid);
    fp = fopen(filepath, "r");
    if (fp){
        if( fgets(buf, BUF_SIZE-1, fp)== NULL ){
            fclose(fp);
        }
        sscanf(buf, "2:cpu:%s", task_cgroup);
        if (!strcmp(task_cgroup, "/")){
            fclose(fp);
            return 0;
        }else{
            fclose(fp);
            return 1;
        }
    }
    
}

int get_time_interval(pid_t pid){
    struct timespec t;
    sched_rr_get_interval(pid, &t);
    return t.tv_nsec/1000000;
}

void set_new_sched(pid_t pid){
    struct sched_param param;
    int policy;
    for(int i=0;i<(sizeof(SCHED_NAME_LIST)/sizeof(SCHED_NAME_LIST[0]));i++){
            if(SCHED_NAME_LIST[i])
                printf("\t%d - %s\n",i,SCHED_NAME_LIST[i]);
        }
    printf("Please input the new policy:\n");
    scanf("%d",&policy);
    printf("Please input the new priority:");
    printf("(%d-%d)\n",sched_get_priority_min(policy),sched_get_priority_max(policy));
    scanf("%d",&param.sched_priority);
    if(!sched_setscheduler(pid,policy,&param))
        printf("Scheduler policy is set to %s.\n",SCHED_NAME_LIST[policy]);
    else{
        printf("Fail to change policy.\n");
        switch (errno)
        {
        case EINVAL:
            printf("This error may caused by following reasons:\n");
            printf("Invalid arguments: pid is negative or param is NULL.\n");
            printf("policy is not one of the recognized policies.\n");
            printf("param does not make sense for the specified policy.\n");
            break;
        case EPERM:
            printf("The calling thread does not have appropriate privileges.\n");
            break;
        case ESRCH:
            printf("The thread whose ID is pid could not be found.\n");
            break;
        default:
            break;
        }
    }
}

int main(int argc, char** argv)
{
    char* task_name="com.osprj.test.processtest";
    pid_t pid;
    int cgroup;
    printf("Task name: %s\n", task_name);
    if(get_pid_by_cmd(&pid, task_name)){
        printf("Pid: %d\n",pid);
        cgroup = get_process_group(pid);
        printf("Group: %s\n",cgroup?"background":"foreground");
        printf("Current policy of pid %d is: %s\n",pid,SCHED_NAME_LIST[sched_getscheduler(pid)]);
        printf("Time slice of pid %d is %d msec(s).\n",pid,get_time_interval(pid));
        set_new_sched(pid);
        printf("Group: %s\n",cgroup?"background":"foreground");
        printf("Current policy of pid %d is: %s\n",pid,SCHED_NAME_LIST[sched_getscheduler(pid)]);
        printf("Time slice of pid %d is %d msec(s).\n",pid,get_time_interval(pid));
    }else{
        printf("Could not find the process: %s\n", task_name);
    }
    return 0;
}