/****************************************************
Ptree Module
A new system call in Linux which returns information of processes and relatioship between processes.
Author: pangbo
*****************************************************
compile:
    make
    Note: You can define __PTREE_DEBUG to enable the debug info output.
    
usage:
    int ptree(struct prinfo *buf, int *nr);
return value:
    >0 - number of processes.
    otherwise - exception occurred.
params:
    buf: a pointer to buffer space.
    nr: a pointer to int, indicates the size of buffer, and stores the number of entries actually copied afer the system call.

*/

#include<linux/module.h>
#include<linux/kernel.h>
#include<linux/init.h>
#include<linux/sched.h>
#include<linux/unistd.h>
#include<linux/highmem.h>
#include<linux/slab.h>

#include<asm/uaccess.h>

#include "prinfo.h"

MODULE_LICENSE("Dual BSD/GPL");
#define __NR_ptreecall 356
//uncomment the following line to enable debug output
// #define __PTREE_DEBUG 

int dfs_ptree(struct task_struct *root,struct prinfo* buf,int* num,int nr);
static int (*oldcall)(void);
static int sys_ptreecall(struct prinfo *buf, int *nr)
{
    /*params:
    buf: a pointer to buffer space.
    nr: a pointer to int, indicates the size of buffer, and stores the number of entries actually copied afer the system call.
    */
    //declare all variables before code (ISO C90)
    int new_nr = 0,user_nr;
    struct prinfo* user_buf;
    struct prinfo* kernel_buf;
    //check the accessiblity of the pointer address
    if (get_user(user_nr, nr)) {
        printk(KERN_INFO "bad nr addr:%ld\n",(long)nr);
        printk(KERN_INFO "access_ok result:%d\n",access_ok(VERIFY_WRITE,nr,sizeof(int)));
        return -EFAULT;
    }
    if(!access_ok(VERIFY_WRITE,nr,sizeof(int))||
        !access_ok(VERIFY_WRITE,buf,(*nr)*sizeof(struct prinfo))) return -EFAULT;
    #ifdef __PTREE_DEBUG
    printk("buf:%u,nr:%u\n",buf,nr);
    #endif

    //save the pointer of user buffer
    user_buf = buf;
    // allocate memory in kernel
    #ifdef __PTREE_DEBUG
    printk("user_nr:%d\n",user_nr);
    #endif
    kernel_buf = kmalloc(sizeof(struct prinfo) * (unsigned int) user_nr, GFP_KERNEL);
    #ifdef __PTREE_DEBUG
    printk("kernel_buf_addr:%u\n",kernel_buf);
    printk("kernel_buf_size:%u\n",sizeof(struct prinfo) * (unsigned int) user_nr);
    #endif
    // check if allocated
    if (kernel_buf == NULL) {
        printk(KERN_WARNING "ptree failed to allocate kernel memory\n");
        return -EFAULT;
    }

    //lock while reading
    read_lock(&tasklist_lock);
    dfs_ptree(&init_task,kernel_buf,&new_nr,*nr);
    read_unlock(&tasklist_lock);

    //copy result back to user space
    if (copy_to_user(buf, kernel_buf, sizeof(struct prinfo) * (unsigned int) user_nr)) {
        //fail to copy, return with exception
        kfree(kernel_buf);
        *nr = 0;
        printk(KERN_WARNING "ptree failed to copy back to user buffer\n");  
        return -EFAULT;
    }else   //free kernel memory
        kfree(kernel_buf);
    
    //store the number of entries actually copied
    if(new_nr<*nr)
        *nr = new_nr;
    #ifdef __PTREE_DEBUG
    printk(KERN_INFO "ptree finish");
    #endif
    return new_nr;
}

int dfs_ptree(struct task_struct *root,struct prinfo* buf,int* num,int nr){
    struct list_head *child_task, *sibling_task;
    struct prinfo* pos;
    struct list_head* node;
    
    if(*num < nr){ //check if buffer is full.
        #ifdef __PTREE_DEBUG
            printk(KERN_INFO "nr_addr:%d,num:%d\n",nr,*num);
            printk(KERN_INFO "root_addr:%u,buf_addr:%u\n",root,buf);
        #endif
        //pos=current postion in buf.
        pos = buf + *num;
        if (root->parent) 
            pos->parent_pid = root->parent->pid;
        else 
            pos->parent_pid = 0;
        
        //copy basic info
        pos->pid = root->pid;
        pos->state = root->state;
        pos->uid = root->cred->uid;
        get_task_comm(pos->comm,root);
        #ifdef __PTREE_DEBUG
            printk(KERN_INFO "com:%s\n",pos->comm);
            printk(KERN_INFO "pid:%d,sta:%d,uid:%d\n",root->pid,root->state,root->cred->uid);
        #endif

        //get child process info
        child_task = &(root->children);
        if (list_empty(child_task))
            pos->first_child_pid = 0;
        else
            pos->first_child_pid = list_first_entry(child_task,
                struct task_struct, sibling)->pid;
        
        //get sibling process info
        sibling_task = &(root->sibling);
        if (list_empty(sibling_task))
            pos->next_sibling_pid = 0;
        else
            pos->next_sibling_pid = list_first_entry(sibling_task, 
                struct task_struct, sibling)->pid;
        #ifdef __PTREE_DEBUG
            printk(KERN_INFO "chi:%d,sib:%d\n",pos->first_child_pid,pos->next_sibling_pid);
        #endif
    }else{
        child_task = &(root->children);
    }
    
    //add the number of prinfo
    (*num)+=1;
    
    //operate dfs
    list_for_each(node, child_task){
        struct task_struct* next_child;
        next_child = list_entry(node, struct task_struct, sibling);
        dfs_ptree(next_child,buf,num,nr);
    }
    
    //another possible method of dfs (but with some bug :D)
    /*
    if (!(list_empty(child_task))) 
        dfs_ptree(list_first_entry(child_task,struct task_struct, sibling),buf,num,nr);
    if (!(list_empty(sibling_task)))
        dfs_ptree(list_first_entry(sibling_task,struct task_struct, sibling),buf,num,nr);
    */
    return *num;
}
static int addsyscall_init(void)
{
    long *syscall = (long*)0xc000d8c4;
    oldcall = (int(*)(void))(syscall[__NR_ptreecall]);
    syscall[__NR_ptreecall] = (unsigned long)sys_ptreecall;
    printk(KERN_INFO "ptree module loaded\n");
    return 0;
}
static void addsyscall_exit(void)
{
    long *syscall = (long*)0xc000d8c4;
    syscall[__NR_ptreecall] = (unsigned long )oldcall;
    printk(KERN_INFO "module exit!\n");
}
module_init(addsyscall_init);
module_exit(addsyscall_exit);
