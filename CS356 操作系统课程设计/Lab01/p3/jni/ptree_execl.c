/***************************************************
Fork and Execl
The process will first ouput the pid of it self.
Then it will fork a child process, the child process will output its pid.
After that the child use execl to execute ptree.
A program to simulate Burger Buddies Problem.
Author: pangbo
*****************************************************

compile:
    ndk-bulid
Note: This program should be compiled under the standard of c11.

useage:
    ./ptree_execl

return value:
    0 - exits normally.
    otherwise - error occurred.
*/

#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(){
    char cwd[64];
    pid_t child_pid;
    printf("51903091xxxx Parent:%d\n",getpid());
    child_pid =  fork();
    if(child_pid==0){
        //child process
        printf("51903091xxxx Child:%d\n",getpid());
        getcwd(cwd,64);
        strcat(cwd,"/ptree");
        if(execl(cwd,"ptree",NULL)){
            //error occurs
            printf("Error occurs while execl ptree: %d\n",errno);
            return errno;
        };
    }else {
        wait(NULL);
        printf("Parent process exit.\n");
    }
    return 0;
}
