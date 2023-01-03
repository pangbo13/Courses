#include<linux/types.h> 
#ifndef __PRINFO_H__
#define __PRINFO_H__
struct prinfo
{
    pid_t parent_pid;
    pid_t pid;
    pid_t first_child_pid;
    pid_t next_sibling_pid;
    long state;
    long uid;
    char comm[64];
};
#endif