# OS Project 1

## Project Structure
```
│  OutputExample.md     Output examples of programs.
│  Prj1README.md        This file.
│
├─p1                    Problem 1, ptree module.
│      Makefile
│      ptree.c
│      prinfo.h
│
├─p2                    Problem 2, ptree module test.
│  └─jni
│          Android.mk
│          prinfo.h
│          ptree_syscall.c
│
├─p3                    Problem 3, fork and execl.
│  └─jni
│          Android.mk
│          ptree_execl.c
│
├─p4                    Problem 4, burger buddies problem.
│  └─jni
│          Android.mk
│          Application.mk
│          BurgerBuddies.c
│          Makefile
│
└─pic                   Screenshots.
        ptree_execl_output.jpg
        ptree_output.jpg
```
## Introduction
### Problem 1
+ source file: [p1/ptree.c](p1/ptree.c)
+ compile:
    ```sh
    make
    ```
  + Note: You can define `__PTREE_DEBUG` to enable the debug info output.

+ usage:
    ```c
    int ptree(struct prinfo *buf, int *nr);
    ```
  + return value:
    + \>0 - success, return the total number of processes.
    + otherwise - exception occurred.
  + params:
    + `buf`: a pointer to buffer space.
    + `nr`: a pointer to int, indicates the size of buffer, and stores the number of entries actually copied afer the system call.
### Problem 2
+ source file: [p2/jni/ptree_syscall.c](p2/jni/ptree_syscall.c)
+ compile:
    ```sh
    ndk-build
    ```
+ usage:
    ```sh
    ./ptree
    ```
+ return value:
    + 0 - exits normally.
    + 255 - error occurred during system call.
+ output:
    See [OutputExample.md Problem 2](OutputExample.md#problem-2).
### Problem 3
+ source file: [p3/jni/ptree_execl.c](p3/jni/ptree_execl.c)
+ compile:
    ```sh
    ndk-bulid
    ```
    + Note: This program should be compiled under the standard of c11.
+ useage:
    ```sh
    ./ptree_execl
    ```
+ return value:
    + 0 - exits normally.
    + otherwise - error occurred.
+ output:
    See [OutputExample.md Problem 3](OutputExample.md#problem-3) .
### Problem 4
+ source file: [p4/jni/BurgerBuddies.c](p4/jni/BurgerBuddies.c)
+ compile:
    ```sh
    ndk-build   #for android
    make        #for linux
    ```
    + macros:
        + `COOK_MAX_SLEEP_TIME`: max time (in microsecond) for a cook to make a burger.
        + `CUSTOM_MAX_COME_TIME`: the max time (in second) that the last customer comes.
        + `TIME_LIMIT`: max execute time, if not defined, the main thread will wait until all threads exit.
    + note: This program should be compiled under the standard of c11.
+ useage:
    ```
    BBC Cooks Cashiers Customers RackSize
    ```
+ params:
    + `Cooks`: number of cooks.
    + `Cashiers:` number of cashiers.
    + `Customers`: number of customers.
    + `RackSize`: size of rack.
+ return value:
    + 0 - program exits normally.
    + 255 - number of params error.
    + 254 - value of params error.
+ output:
    See [OutputExample.md Problem 4](OutputExample.md#problem-4) .