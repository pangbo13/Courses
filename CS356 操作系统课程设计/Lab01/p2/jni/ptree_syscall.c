/***************************************************
Ptree Test
A program to test system module ptree.
Author: pangbo
*****************************************************
compile:
    ndk-build

usage:
    ./ptree
    
return value:
    0 - exits normally.
    255 - error occurred during system call.
*/
#include <stdio.h>
#include <stdlib.h>
#include <sys/syscall.h>
#include "prinfo.h"

#define __NR_ptreecall 356
#define BUFFER_SIZE 200

void print_tasktree(struct prinfo *data,int *pos,int total,int ppid,int level){
    /*params:
    data: pointer to buffer
    pos: current position
    total: total number of entries in buffer
    ppid: pid of parent process
    level: levels of current process (number of \t)
    */
    struct prinfo* cur = data+*pos;
    int pid = cur->pid;
    if(cur->parent_pid==ppid){
        for(int i = 0;i<level;i++) printf("\t");
        printf("%s,%d,%ld,%d,%d,%d,%ld\n",cur->comm,cur->pid,cur->state,
            cur->parent_pid,cur->first_child_pid,cur->next_sibling_pid,cur->uid);
    }
    (*pos)++;
    //print info of all child processes
    while(*pos<total&&(data+*pos)->parent_pid==pid) {
        print_tasktree(data,pos,total,pid,level+1);
    }
}

int main(){
    int buf_size = BUFFER_SIZE;
    int total_num;
    int buf_used = buf_size;
    struct prinfo* buf;
    //allocate the buffer space
    buf = (struct prinfo*)malloc(sizeof(struct prinfo) * buf_size);

    //call the system call
    total_num = syscall(__NR_ptreecall,buf,&buf_used);
    
    if(total_num>0){
    //print the tree structure
        int pos = 0;
        print_tasktree(buf,&pos,buf_used,0,0);
    }else{
        printf("Error occurs during syscall: %d\n",total_num);
        free(buf);
        return -1;
    }

    free(buf);
    return 0;
}
