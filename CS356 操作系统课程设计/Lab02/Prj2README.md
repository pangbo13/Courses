# OS Project 2

## Overview
* `goldfish`: A directory containing all the modified kernel code. The file directory is organized according to the original structure of the kernel.
* `set_sched`: A program to modify the scheduling policy and priority of the specified process.
* `get_interval`: A program to output the time slice allocated to the specified process.
* `test_basic`: A program to automatically search for the `PID` of the test app and output scheduling information such as scheduling policy and time slice. It can also change the scheduling policy of the test app conveniently and output the results after the modifying.
* `simulation`: A python program used to simulate and compare the performance of 4 schedulers.

## File Structure
```
│  Prj2README.md
│  Report.md
│  Report.pdf
│
├─get_interval
│  └─jni
│          Android.mk
│          get_interval.c
│          sched_name.h
│
├─goldfish
│  ├─arch
│  │  └─arm
│  │      └─configs
│  │              goldfish_armv7_defconfig
│  │
│  ├─include
│  │  └─linux
│  │          init_task.h
│  │          sched.h
│  │
│  ├─init
│  │      Kconfig
│  │
│  └─kernel
│      └─sched
│              core.c
│              debug.c
│              Makefile
│              rt.c
│              sched.h
│              wrr.c
│
├─pic
│      ······
│
├─set_scheder
│  └─jni
│          Android.mk
│          sched_name.h
│          set_sched.c
│
├─simulation
│      gantt.py
│      main.py
│      scatter_plot.py
│
└─test_basic
    └─jni
            Android.mk
            sched_name.h
            test_basic.c
```

## Report

The complete project report can be found in [Report.md](./Report.md).

*For a better reading experience, you may click [here](./Report.pdf) for the PDF version or [here](https://notes.sjtu.edu.cn/67jFbFn9RKKir0XAHlMhnQ?view) for the online version.*