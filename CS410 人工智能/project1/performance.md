[toc]

# 3-MSA

##DP

### SEQ1 (IPZJJLMLTKJU)

#### LBE

```
 121540675 function calls (121462614 primitive calls) in 164.963 seconds

   Ordered by: cumulative time
   List reduced from 4877 to 22 due to restriction <'Solver'>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000  164.969  164.969 DPSolver_3.py:1(<module>)
        1    0.036    0.036  164.321  164.321 BaseSolver.py:57(run_test)
       18   62.645    3.480  124.590    6.922 DPSolver_3.py:51(solve)
     4950    0.015    0.000   39.685    0.008 DPSolver_3.py:19(get_lower_evaluation)
    14850    0.007    0.000   39.562    0.003 DPSolver_3.py:26(<lambda>)
    14850    0.075    0.000   39.555    0.003 DPSolver_numba.py:11(solve)
    14850   38.713    0.003   38.713    0.003 DPSolver_numba.py:17(solve_speedup)
        1    0.000    0.000    0.523    0.523 DPSolver_numba.py:1(<module>)
    14850    0.029    0.000    0.099    0.000 DPSolver.py:10(__init__)
        1    0.000    0.000    0.032    0.032 DPSolver_numba.py:10(DPSolver_2_numba)
     4950    0.004    0.000    0.006    0.000 DPSolver_3.py:12(__init__)
    19800    0.004    0.000    0.004    0.000 BaseSolver.py:12(__init__)
       18    0.002    0.000    0.002    0.000 DPSolver_3.py:96(align_seq)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 DPSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:35(__init__)
        1    0.000    0.000    0.000    0.000 DPSolver_3.py:11(DPSolver_3)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:11(BaseSolver)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:108(SpeedupHashBin)
        1    0.000    0.000    0.000    0.000 DPSolver.py:9(DPSolver_2)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:34(Tester)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:5(FakeFile)
```



#### LBE+HashBin

```
120621942 function calls (120600093 primitive calls) in 126.485 seconds

   Ordered by: cumulative time
   List reduced from 4881 to 26 due to restriction <'Solver'>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000  126.487  126.487 DPSolver_3.py:1(<module>)
        1    0.010    0.010  125.866  125.866 BaseSolver.py:57(run_test)
       18   63.891    3.550  123.815    6.879 DPSolver_3.py:51(solve)
     4950    0.011    0.000    2.034    0.000 DPSolver_3.py:19(get_lower_evaluation)
      797    0.004    0.000    1.989    0.002 DPSolver_numba.py:11(solve)
      797    1.732    0.002    1.732    0.002 DPSolver_numba.py:17(solve_speedup)
        1    0.000    0.000    0.505    0.505 DPSolver_numba.py:1(<module>)
        1    0.000    0.000    0.031    0.031 DPSolver_numba.py:10(DPSolver_2_numba)
    14850    0.005    0.000    0.023    0.000 BaseSolver.py:119(__getitem__)
    15647    0.012    0.000    0.017    0.000 BaseSolver.py:112(__calc_hash)
      797    0.002    0.000    0.006    0.000 DPSolver.py:10(__init__)
     4950    0.002    0.000    0.003    0.000 DPSolver_3.py:12(__init__)
      797    0.001    0.000    0.002    0.000 BaseSolver.py:126(__setitem__)
       18    0.002    0.000    0.002    0.000 DPSolver_3.py:96(align_seq)
    14850    0.001    0.000    0.001    0.000 DPSolver_3.py:33(<lambda>)
     5747    0.001    0.000    0.001    0.000 BaseSolver.py:12(__init__)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 DPSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:35(__init__)
        1    0.000    0.000    0.000    0.000 DPSolver.py:9(DPSolver_2)
        1    0.000    0.000    0.000    0.000 DPSolver_3.py:11(DPSolver_3)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:109(__init__)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:11(BaseSolver)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:34(Tester)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:108(SpeedupHashBin)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:5(FakeFile)
```



#### LBE+HashBin+Numba

```
   5460214 function calls (5214636 primitive calls) in 17.972 seconds

   Ordered by: cumulative time
   List reduced from 6529 to 29 due to restriction <'Solver'>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   17.976   17.976 DPSolver_3_numba.py:1(<module>)
        1    0.010    0.010   17.365   17.365 BaseSolver.py:57(run_test)
       18    0.000    0.000   15.295    0.850 DPSolver_3_numba.py:12(solve)
       18   12.243    0.680   12.243    0.680 DPSolver_3_numba.py:28(solve_speedup)
     4950    0.011    0.000    2.053    0.000 DPSolver_3.py:19(get_lower_evaluation)
      797    0.005    0.000    2.004    0.003 DPSolver_numba.py:11(solve)
      797    1.745    0.002    1.745    0.002 DPSolver_numba.py:17(solve_speedup)
        1    0.000    0.000    0.032    0.032 DPSolver_3.py:1(<module>)
        1    0.000    0.000    0.032    0.032 DPSolver_numba.py:1(<module>)
        1    0.000    0.000    0.031    0.031 DPSolver_numba.py:10(DPSolver_2_numba)
    14850    0.005    0.000    0.023    0.000 BaseSolver.py:119(__getitem__)
    15647    0.012    0.000    0.019    0.000 BaseSolver.py:112(__calc_hash)
      797    0.002    0.000    0.007    0.000 DPSolver.py:10(__init__)
      797    0.001    0.000    0.003    0.000 BaseSolver.py:126(__setitem__)
     4950    0.002    0.000    0.003    0.000 DPSolver_3.py:12(__init__)
       18    0.001    0.000    0.001    0.000 DPSolver_3.py:96(align_seq)
    14850    0.001    0.000    0.001    0.000 DPSolver_3.py:33(<lambda>)
     5747    0.001    0.000    0.001    0.000 BaseSolver.py:12(__init__)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 DPSolver_3_numba.py:11(DPSolver_3_numba)
        1    0.000    0.000    0.000    0.000 DPSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:35(__init__)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:11(BaseSolver)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:109(__init__)
        1    0.000    0.000    0.000    0.000 DPSolver_3.py:11(DPSolver_3)
        1    0.000    0.000    0.000    0.000 DPSolver.py:9(DPSolver_2)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:34(Tester)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:5(FakeFile)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:108(SpeedupHashBin)
```



#### LBE+HashBin+Numba(Cached)

```
957994 function calls (935984 primitive calls) in 14.390 seconds

   Ordered by: cumulative time
   List reduced from 4879 to 29 due to restriction <'Solver'>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   14.391   14.391 DPSolver_3_numba.py:1(<module>)
        1    0.009    0.009   13.780   13.780 BaseSolver.py:57(run_test)
       18    0.000    0.000   11.895    0.661 DPSolver_3_numba.py:12(solve)
       18   11.882    0.660   11.882    0.660 DPSolver_3_numba.py:28(solve_speedup)
     4950    0.009    0.000    1.870    0.000 DPSolver_3.py:19(get_lower_evaluation)
      797    0.004    0.000    1.829    0.002 DPSolver_numba.py:11(solve)
      797    1.581    0.002    1.581    0.002 DPSolver_numba.py:17(solve_speedup)
        1    0.000    0.000    0.032    0.032 DPSolver_3.py:1(<module>)
        1    0.000    0.000    0.031    0.031 DPSolver_numba.py:1(<module>)
        1    0.000    0.000    0.030    0.030 DPSolver_numba.py:10(DPSolver_2_numba)
    14850    0.005    0.000    0.021    0.000 BaseSolver.py:119(__getitem__)
    15647    0.011    0.000    0.016    0.000 BaseSolver.py:112(__calc_hash)
      797    0.002    0.000    0.005    0.000 DPSolver.py:10(__init__)
     4950    0.002    0.000    0.003    0.000 DPSolver_3.py:12(__init__)
      797    0.001    0.000    0.002    0.000 BaseSolver.py:126(__setitem__)
       18    0.001    0.000    0.001    0.000 DPSolver_3.py:96(align_seq)
        1    0.000    0.000    0.001    0.001 DPSolver_3_numba.py:11(DPSolver_3_numba)
    14850    0.001    0.000    0.001    0.000 DPSolver_3.py:33(<lambda>)
     5747    0.001    0.000    0.001    0.000 BaseSolver.py:12(__init__)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 DPSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:35(__init__)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:11(BaseSolver)
        1    0.000    0.000    0.000    0.000 DPSolver_3.py:11(DPSolver_3)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:109(__init__)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:34(Tester)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:108(SpeedupHashBin)
        1    0.000    0.000    0.000    0.000 DPSolver.py:9(DPSolver_2)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:5(FakeFile)
```



### SEQ2 (IWTJBGTJGJTW)

#### LBE

```
 62815867 function calls (62737806 primitive calls) in 99.267 seconds

   Ordered by: cumulative time
   List reduced from 4877 to 22 due to restriction <'Solver'>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   99.273   99.273 DPSolver_3.py:1(<module>)
        1    0.035    0.035   98.667   98.667 BaseSolver.py:57(run_test)
        8   27.992    3.499   56.654    7.082 DPSolver_3.py:51(solve)
     4950    0.014    0.000   41.970    0.008 DPSolver_3.py:19(get_lower_evaluation)
    14850    0.008    0.000   41.850    0.003 DPSolver_3.py:26(<lambda>)
    14850    0.072    0.000   41.842    0.003 DPSolver_numba.py:11(solve)
    14850   41.014    0.003   41.014    0.003 DPSolver_numba.py:17(solve_speedup)
        1    0.000    0.000    0.489    0.489 DPSolver_numba.py:1(<module>)
    14850    0.027    0.000    0.098    0.000 DPSolver.py:10(__init__)
        1    0.000    0.000    0.031    0.031 DPSolver_numba.py:10(DPSolver_2_numba)
     4950    0.004    0.000    0.006    0.000 DPSolver_3.py:12(__init__)
    19800    0.004    0.000    0.004    0.000 BaseSolver.py:12(__init__)
        8    0.001    0.000    0.001    0.000 DPSolver_3.py:96(align_seq)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 DPSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:35(__init__)
        1    0.000    0.000    0.000    0.000 DPSolver_3.py:11(DPSolver_3)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:108(SpeedupHashBin)
        1    0.000    0.000    0.000    0.000 DPSolver.py:9(DPSolver_2)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:11(BaseSolver)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:34(Tester)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:5(FakeFile)
```

#### LBE+HashBin

```
  61859164 function calls (61839287 primitive calls) in 56.515 seconds

   Ordered by: cumulative time
   List reduced from 4881 to 26 due to restriction <'Solver'>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   56.517   56.517 DPSolver_3.py:1(<module>)
        1    0.007    0.007   55.877   55.877 BaseSolver.py:57(run_test)
        8   27.734    3.467   54.916    6.865 DPSolver_3.py:51(solve)
     4950    0.008    0.000    0.949    0.000 DPSolver_3.py:19(get_lower_evaluation)
      304    0.002    0.000    0.913    0.003 DPSolver_numba.py:11(solve)
      304    0.667    0.002    0.667    0.002 DPSolver_numba.py:17(solve_speedup)
        1    0.000    0.000    0.520    0.520 DPSolver_numba.py:1(<module>)
        1    0.000    0.000    0.031    0.031 DPSolver_numba.py:10(DPSolver_2_numba)
    14850    0.005    0.000    0.021    0.000 BaseSolver.py:119(__getitem__)
    15154    0.010    0.000    0.015    0.000 BaseSolver.py:112(__calc_hash)
     4950    0.002    0.000    0.003    0.000 DPSolver_3.py:12(__init__)
      304    0.001    0.000    0.002    0.000 DPSolver.py:10(__init__)
    14850    0.001    0.000    0.001    0.000 DPSolver_3.py:33(<lambda>)
      304    0.000    0.000    0.001    0.000 BaseSolver.py:126(__setitem__)
     5254    0.001    0.000    0.001    0.000 BaseSolver.py:12(__init__)
        8    0.001    0.000    0.001    0.000 DPSolver_3.py:96(align_seq)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 DPSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:35(__init__)
        1    0.000    0.000    0.000    0.000 DPSolver_3.py:11(DPSolver_3)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:109(__init__)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:108(SpeedupHashBin)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:11(BaseSolver)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:34(Tester)
        1    0.000    0.000    0.000    0.000 DPSolver.py:9(DPSolver_2)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:5(FakeFile)
```

#### LBE+HashBin+Numba

```
   5413810 function calls (5170241 primitive calls) in 11.740 seconds

   Ordered by: cumulative time
   List reduced from 6529 to 29 due to restriction <'Solver'>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   11.744   11.744 DPSolver_3_numba.py:1(<module>)
        1    0.010    0.010   11.103   11.103 BaseSolver.py:57(run_test)
        8    0.000    0.000   10.050    1.256 DPSolver_3_numba.py:13(solve)
        8    6.833    0.854    6.833    0.854 DPSolver_3_numba.py:29(solve_speedup)
     4950    0.011    0.000    1.038    0.000 DPSolver_3.py:19(get_lower_evaluation)
      304    0.002    0.000    0.992    0.003 DPSolver_numba.py:11(solve)
      304    0.743    0.002    0.743    0.002 DPSolver_numba.py:17(solve_speedup)
        1    0.000    0.000    0.034    0.034 DPSolver_3.py:1(<module>)
        1    0.000    0.000    0.034    0.034 DPSolver_numba.py:1(<module>)
        1    0.000    0.000    0.033    0.033 DPSolver_numba.py:10(DPSolver_2_numba)
    14850    0.006    0.000    0.026    0.000 BaseSolver.py:119(__getitem__)
    15154    0.012    0.000    0.018    0.000 BaseSolver.py:112(__calc_hash)
     4950    0.003    0.000    0.004    0.000 DPSolver_3.py:12(__init__)
      304    0.001    0.000    0.003    0.000 DPSolver.py:10(__init__)
    14850    0.001    0.000    0.001    0.000 DPSolver_3.py:33(<lambda>)
      304    0.000    0.000    0.001    0.000 BaseSolver.py:126(__setitem__)
     5254    0.001    0.000    0.001    0.000 BaseSolver.py:12(__init__)
        8    0.001    0.000    0.001    0.000 DPSolver_3.py:96(align_seq)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 DPSolver_3_numba.py:12(DPSolver_3_numba)
        1    0.000    0.000    0.000    0.000 DPSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:35(__init__)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:11(BaseSolver)
        1    0.000    0.000    0.000    0.000 DPSolver_3.py:11(DPSolver_3)
        1    0.000    0.000    0.000    0.000 DPSolver.py:9(DPSolver_2)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:109(__init__)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:34(Tester)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:108(SpeedupHashBin)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:5(FakeFile)

         919089 function calls (899101 primitive calls) in 8.716 seconds
```

#### LBE+HashBin+Numba(Cached)

```
   919089 function calls (899101 primitive calls) in 8.278 seconds

   Ordered by: cumulative time
   List reduced from 4879 to 29 due to restriction <'Solver'>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    8.279    8.279 DPSolver_3_numba.py:1(<module>)
        1    0.007    0.007    7.604    7.604 BaseSolver.py:57(run_test)
        8    0.000    0.000    6.611    0.826 DPSolver_3_numba.py:12(solve)
        8    6.599    0.825    6.599    0.825 DPSolver_3_numba.py:28(solve_speedup)
     4950    0.008    0.000    0.981    0.000 DPSolver_3.py:19(get_lower_evaluation)
      304    0.002    0.000    0.945    0.003 DPSolver_numba.py:11(solve)
      304    0.703    0.002    0.703    0.002 DPSolver_numba.py:17(solve_speedup)
        1    0.000    0.000    0.033    0.033 DPSolver_3.py:1(<module>)
        1    0.000    0.000    0.033    0.033 DPSolver_numba.py:1(<module>)
        1    0.000    0.000    0.032    0.032 DPSolver_numba.py:10(DPSolver_2_numba)
    14850    0.005    0.000    0.022    0.000 BaseSolver.py:119(__getitem__)
    15154    0.011    0.000    0.016    0.000 BaseSolver.py:112(__calc_hash)
     4950    0.002    0.000    0.003    0.000 DPSolver_3.py:12(__init__)
      304    0.001    0.000    0.002    0.000 DPSolver.py:10(__init__)
    14850    0.001    0.000    0.001    0.000 DPSolver_3.py:33(<lambda>)
      304    0.000    0.000    0.001    0.000 BaseSolver.py:126(__setitem__)
     5254    0.001    0.000    0.001    0.000 BaseSolver.py:12(__init__)
        1    0.000    0.000    0.001    0.001 DPSolver_3_numba.py:11(DPSolver_3_numba)
        8    0.001    0.000    0.001    0.000 DPSolver_3.py:96(align_seq)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 DPSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:35(__init__)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:11(BaseSolver)
        1    0.000    0.000    0.000    0.000 DPSolver_3.py:11(DPSolver_3)
        1    0.000    0.000    0.000    0.000 DPSolver.py:9(DPSolver_2)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:109(__init__)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:34(Tester)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:108(SpeedupHashBin)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:5(FakeFile)
```

## A*

### SEQ1

#### LBE

```
9685160 function calls (9607110 primitive calls) in 44.868 seconds

   Ordered by: cumulative time
   List reduced from 4893 to 29 due to restriction <'Solver'>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   44.875   44.875 AStarSolver_3.py:1(<module>)
        1    0.041    0.041   44.210   44.210 BaseSolver.py:57(run_test)
     4950    0.036    0.000   40.927    0.008 AStarSolver_3.py:29(get_lower_evaluation)
    14850    0.092    0.000   40.738    0.003 DPSolver_numba.py:11(solve)
    14850   39.770    0.003   39.770    0.003 DPSolver_numba.py:17(solve_speedup)
       18    0.212    0.012    3.229    0.179 AStarSolver_3.py:63(solve)
   131556    0.341    0.000    1.132    0.000 AStarSolver_3.py:139(expand)
   217823    0.116    0.000    0.759    0.000 AStarSolver_3.py:136(Node)
   217841    0.187    0.000    0.642    0.000 AStarSolver_3.py:115(__init__)
        1    0.000    0.000    0.538    0.538 DPSolver_numba.py:1(<module>)
   217841    0.284    0.000    0.456    0.000 AStarSolver_3.py:126(heuristic)
  2133897    0.296    0.000    0.296    0.000 AStarSolver_3.py:123(__lt__)
   653523    0.172    0.000    0.172    0.000 DPSolver.py:57(get_sub_cost)
    14850    0.041    0.000    0.153    0.000 DPSolver.py:8(__init__)
   131574    0.051    0.000    0.063    0.000 AStarSolver_3.py:131(is_target)
        1    0.000    0.000    0.042    0.042 DPSolver_numba.py:10(DPSolver_2_numba)
     4950    0.008    0.000    0.010    0.000 AStarSolver_3.py:13(__init__)
    19800    0.006    0.000    0.006    0.000 BaseSolver.py:12(__init__)
       18    0.001    0.000    0.001    0.000 AStarSolver_3.py:91(align_seq)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 DPSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:35(__init__)
        1    0.000    0.000    0.000    0.000 AStarSolver_3.py:114(AStarNode)
        1    0.000    0.000    0.000    0.000 AStarSolver_3.py:12(AStarSolver_3)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:34(Tester)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:11(BaseSolver)
        1    0.000    0.000    0.000    0.000 DPSolver.py:7(DPSolver_2)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:108(SpeedupHashBin)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:5(FakeFile)
```



#### LBE+HashBin

```
8788073 function calls (8766135 primitive calls) in 5.289 seconds

   Ordered by: cumulative time
   List reduced from 4898 to 34 due to restriction <'Solver'>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    5.290    5.290 AStarSolver_3.py:1(<module>)
        1    0.007    0.007    4.703    4.703 BaseSolver.py:57(run_test)
       18    0.177    0.010    2.784    0.155 AStarSolver_3.py:63(solve)
      822    0.004    0.000    1.916    0.002 DPSolver_numba.py:11(solve)
     4950    0.009    0.000    1.905    0.000 AStarSolver_3.py:29(get_lower_evaluation)
      822    1.670    0.002    1.670    0.002 DPSolver_numba.py:17(solve_speedup)
   131556    0.289    0.000    0.939    0.000 AStarSolver_3.py:139(expand)
   217823    0.099    0.000    0.624    0.000 AStarSolver_3.py:136(Node)
   217841    0.139    0.000    0.525    0.000 AStarSolver_3.py:115(__init__)
        1    0.000    0.000    0.472    0.472 DPSolver_numba.py:1(<module>)
   217841    0.243    0.000    0.386    0.000 AStarSolver_3.py:126(heuristic)
  2133897    0.252    0.000    0.252    0.000 AStarSolver_3.py:123(__lt__)
   653523    0.142    0.000    0.142    0.000 DPSolver.py:57(get_sub_cost)
   131574    0.040    0.000    0.050    0.000 AStarSolver_3.py:131(is_target)
        1    0.000    0.000    0.030    0.030 DPSolver_numba.py:10(DPSolver_2_numba)
    14850    0.005    0.000    0.022    0.000 BaseSolver.py:119(__getitem__)
    15647    0.011    0.000    0.017    0.000 BaseSolver.py:112(__calc_hash)
      822    0.002    0.000    0.006    0.000 DPSolver.py:8(__init__)
     4950    0.003    0.000    0.004    0.000 AStarSolver_3.py:13(__init__)
      797    0.001    0.000    0.002    0.000 BaseSolver.py:126(__setitem__)
    14850    0.001    0.000    0.001    0.000 AStarSolver_3.py:39(<lambda>)
       18    0.001    0.000    0.001    0.000 AStarSolver_3.py:91(align_seq)
     5772    0.001    0.000    0.001    0.000 BaseSolver.py:12(__init__)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 DPSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:35(__init__)
        1    0.000    0.000    0.000    0.000 AStarSolver_3.py:114(AStarNode)
        1    0.000    0.000    0.000    0.000 AStarSolver_3.py:12(AStarSolver_3)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:109(__init__)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:11(BaseSolver)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:34(Tester)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:108(SpeedupHashBin)
        1    0.000    0.000    0.000    0.000 DPSolver.py:7(DPSolver_2)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:5(FakeFile)
```



### SEQ2

#### LBE

```
4530680 function calls (4452630 primitive calls) in 44.317 seconds

   Ordered by: cumulative time
   List reduced from 4893 to 29 due to restriction <'Solver'>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   44.323   44.323 AStarSolver_3.py:1(<module>)
        1    0.023    0.023   43.733   43.733 BaseSolver.py:57(run_test)
     4950    0.025    0.000   42.685    0.009 AStarSolver_3.py:29(get_lower_evaluation)
    14850    0.063    0.000   42.552    0.003 DPSolver_numba.py:11(solve)
    14850   41.773    0.003   41.773    0.003 DPSolver_numba.py:17(solve_speedup)
        8    0.063    0.008    1.017    0.127 AStarSolver_3.py:63(solve)
        1    0.000    0.000    0.475    0.475 DPSolver_numba.py:1(<module>)
    42871    0.118    0.000    0.361    0.000 AStarSolver_3.py:139(expand)
    76669    0.026    0.000    0.234    0.000 AStarSolver_3.py:136(Node)
    76677    0.054    0.000    0.208    0.000 AStarSolver_3.py:115(__init__)
    76677    0.094    0.000    0.153    0.000 AStarSolver_3.py:126(heuristic)
    14850    0.033    0.000    0.108    0.000 DPSolver.py:8(__init__)
   729778    0.090    0.000    0.090    0.000 AStarSolver_3.py:123(__lt__)
   230031    0.059    0.000    0.059    0.000 DPSolver.py:57(get_sub_cost)
        1    0.000    0.000    0.030    0.030 DPSolver_numba.py:10(DPSolver_2_numba)
    42879    0.016    0.000    0.020    0.000 AStarSolver_3.py:131(is_target)
    19800    0.007    0.000    0.007    0.000 BaseSolver.py:12(__init__)
     4950    0.005    0.000    0.006    0.000 AStarSolver_3.py:13(__init__)
        8    0.001    0.000    0.001    0.000 AStarSolver_3.py:91(align_seq)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:35(__init__)
        1    0.000    0.000    0.000    0.000 DPSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 AStarSolver_3.py:12(AStarSolver_3)
        1    0.000    0.000    0.000    0.000 AStarSolver_3.py:114(AStarNode)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:11(BaseSolver)
        1    0.000    0.000    0.000    0.000 DPSolver.py:7(DPSolver_2)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:34(Tester)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:108(SpeedupHashBin)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:5(FakeFile)
```

#### LBE+HashBin

```
3594723 function calls (3574805 primitive calls) in 2.534 seconds

   Ordered by: cumulative time
   List reduced from 4898 to 34 due to restriction <'Solver'>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    2.535    2.535 AStarSolver_3.py:1(<module>)
        1    0.005    0.005    1.945    1.945 BaseSolver.py:57(run_test)
        8    0.061    0.008    1.004    0.126 AStarSolver_3.py:63(solve)
     4950    0.007    0.000    0.930    0.000 AStarSolver_3.py:29(get_lower_evaluation)
      317    0.002    0.000    0.926    0.003 DPSolver_numba.py:11(solve)
      317    0.701    0.002    0.701    0.002 DPSolver_numba.py:17(solve_speedup)
        1    0.000    0.000    0.474    0.474 DPSolver_numba.py:1(<module>)
    42871    0.109    0.000    0.340    0.000 AStarSolver_3.py:139(expand)
    76669    0.026    0.000    0.222    0.000 AStarSolver_3.py:136(Node)
    76677    0.051    0.000    0.195    0.000 AStarSolver_3.py:115(__init__)
    76677    0.090    0.000    0.144    0.000 AStarSolver_3.py:126(heuristic)
   729778    0.089    0.000    0.089    0.000 AStarSolver_3.py:123(__lt__)
   230031    0.055    0.000    0.055    0.000 DPSolver.py:57(get_sub_cost)
        1    0.000    0.000    0.030    0.030 DPSolver_numba.py:10(DPSolver_2_numba)
    14850    0.005    0.000    0.020    0.000 BaseSolver.py:119(__getitem__)
    42879    0.015    0.000    0.018    0.000 AStarSolver_3.py:131(is_target)
    15154    0.010    0.000    0.015    0.000 BaseSolver.py:112(__calc_hash)
     4950    0.003    0.000    0.003    0.000 AStarSolver_3.py:13(__init__)
      317    0.001    0.000    0.003    0.000 DPSolver.py:8(__init__)
    14850    0.001    0.000    0.001    0.000 AStarSolver_3.py:39(<lambda>)
     5267    0.001    0.000    0.001    0.000 BaseSolver.py:12(__init__)
      304    0.000    0.000    0.001    0.000 BaseSolver.py:126(__setitem__)
        8    0.001    0.000    0.001    0.000 AStarSolver_3.py:91(align_seq)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 DPSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:35(__init__)
        1    0.000    0.000    0.000    0.000 AStarSolver_3.py:114(AStarNode)
        1    0.000    0.000    0.000    0.000 AStarSolver_3.py:12(AStarSolver_3)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:11(BaseSolver)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:34(Tester)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:109(__init__)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:108(SpeedupHashBin)
        1    0.000    0.000    0.000    0.000 DPSolver.py:7(DPSolver_2)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:5(FakeFile)
```

## GA

### SEQ1

#### LBE+HashBin

```
212443776 function calls (178901762 primitive calls) in 68.974 seconds

   Ordered by: cumulative time
   List reduced from 4918 to 49 due to restriction <'Solver'>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   68.975   68.975 GASolver_3.py:1(<module>)
        1    0.054    0.054   68.363   68.363 BaseSolver.py:56(run_test)
      104    0.428    0.004   63.805    0.614 GASolver_3.py:17(solve)
   369200    0.332    0.000   55.007    0.000 GASolver_3.py:86(__init__)
   369200    0.253    0.000   44.402    0.000 GASolver_3.py:104(calc_cost)
 33518754   12.746    0.000   39.810    0.000 GASolver_3.py:108(calc_cost_chr)
   208000    0.303    0.000   34.730    0.000 GASolver_3.py:152(move)
   104000    0.159    0.000   17.213    0.000 GASolver_3.py:140(mutation)
100556262   12.971    0.000   12.971    0.000 GASolver_3.py:112(calc_cost_pair)
   369304    0.522    0.000   10.276    0.000 GASolver_3.py:99(align_seq)
   369304    0.688    0.000    8.963    0.000 GASolver_3.py:101(<listcomp>)
    62400    0.024    0.000    8.632    0.000 GASolver_3.py:40(<genexpr>)
    52000    0.103    0.000    8.607    0.000 GASolver_3.py:131(cross_over)
  1107912    4.217    0.000    8.275    0.000 GASolver_3.py:121(format_seq)
   208000    0.436    0.000    3.511    0.000 GASolver_3.py:154(<listcomp>)
     4950    0.027    0.000    3.025    0.001 GASolver_3.py:50(get_lower_evaluation)
   624000    0.810    0.000    2.932    0.000 GASolver_3.py:157(move_single)
     1151    0.016    0.000    2.913    0.003 DPSolver_numba.py:11(solve)
     1151    2.585    0.002    2.585    0.002 DPSolver_numba.py:17(solve_speedup)
   104000    0.226    0.000    1.508    0.000 GASolver_3.py:142(<listcomp>)
   312000    0.332    0.000    1.212    0.000 GASolver_3.py:145(mutation_single)
      104    0.002    0.000    1.013    0.010 GASolver_3.py:21(<listcomp>)
     5200    0.013    0.000    1.011    0.000 GASolver_3.py:93(init_indv)
   208000    0.060    0.000    0.697    0.000 GASolver_3.py:133(<genexpr>)
   156000    0.185    0.000    0.637    0.000 GASolver_3.py:136(cross_over_single)
  1107912    0.369    0.000    0.518    0.000 GASolver_3.py:100(<lambda>)
        1    0.000    0.000    0.493    0.493 DPSolver_numba.py:1(<module>)
    20800    0.041    0.000    0.226    0.000 GASolver_3.py:96(<genexpr>)
    14850    0.010    0.000    0.050    0.000 BaseSolver.py:118(__getitem__)
   489216    0.046    0.000    0.046    0.000 GASolver_3.py:27(<genexpr>)
    16001    0.027    0.000    0.040    0.000 BaseSolver.py:111(__calc_hash)
        1    0.000    0.000    0.032    0.032 DPSolver_numba.py:10(DPSolver_2_numba)
     1151    0.006    0.000    0.021    0.000 DPSolver.py:8(__init__)
     4950    0.006    0.000    0.009    0.000 GASolver_3.py:11(__init__)
     1151    0.002    0.000    0.006    0.000 BaseSolver.py:125(__setitem__)
     6101    0.004    0.000    0.004    0.000 BaseSolver.py:11(__init__)
      104    0.000    0.000    0.003    0.000 GASolver_3.py:82(align_seq)
    14850    0.002    0.000    0.002    0.000 GASolver_3.py:64(<lambda>)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 DPSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:34(__init__)
        1    0.000    0.000    0.000    0.000 GASolver_3.py:85(Individual)
        1    0.000    0.000    0.000    0.000 GASolver_3.py:10(GASolver_3)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:108(__init__)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:10(BaseSolver)
        1    0.000    0.000    0.000    0.000 DPSolver.py:7(DPSolver_2)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:33(Tester)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:107(SpeedupHashBin)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:4(FakeFile)
```



### SEQ2

#### LBE+HashBin

```
111791989 function calls (94243869 primitive calls) in 37.686 seconds

   Ordered by: cumulative time
   List reduced from 4930 to 49 due to restriction <'Solver'>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   37.687   37.687 GASolver_3.py:1(<module>)
        1    0.050    0.050   37.024   37.024 BaseSolver.py:56(run_test)
       48    0.211    0.004   34.135    0.711 GASolver_3.py:17(solve)
   170400    0.153    0.000   29.916    0.000 GASolver_3.py:86(__init__)
   170400    0.121    0.000   23.141    0.000 GASolver_3.py:104(calc_cost)
 17527332    6.822    0.000   20.735    0.000 GASolver_3.py:108(calc_cost_chr)
    96000    0.147    0.000   18.630    0.000 GASolver_3.py:152(move)
    48000    0.077    0.000    9.216    0.000 GASolver_3.py:140(mutation)
 52581996    6.665    0.000    6.665    0.000 GASolver_3.py:112(calc_cost_pair)
   170448    0.244    0.000    6.624    0.000 GASolver_3.py:99(align_seq)
   170448    0.346    0.000    6.014    0.000 GASolver_3.py:101(<listcomp>)
   511344    2.544    0.000    5.669    0.000 GASolver_3.py:121(format_seq)
    28800    0.011    0.000    4.693    0.000 GASolver_3.py:40(<genexpr>)
    24000    0.051    0.000    4.682    0.000 GASolver_3.py:131(cross_over)
    96000    0.205    0.000    1.685    0.000 GASolver_3.py:154(<listcomp>)
     4950    0.021    0.000    1.592    0.000 GASolver_3.py:50(get_lower_evaluation)
      533    0.008    0.000    1.503    0.003 DPSolver_numba.py:11(solve)
   288000    0.392    0.000    1.409    0.000 GASolver_3.py:157(move_single)
      533    1.225    0.002    1.225    0.002 DPSolver_numba.py:17(solve_speedup)
    48000    0.105    0.000    0.711    0.000 GASolver_3.py:142(<listcomp>)
   144000    0.157    0.000    0.572    0.000 GASolver_3.py:145(mutation_single)
       48    0.001    0.000    0.527    0.011 GASolver_3.py:21(<listcomp>)
     2400    0.006    0.000    0.526    0.000 GASolver_3.py:93(init_indv)
        1    0.000    0.000    0.502    0.502 DPSolver_numba.py:1(<module>)
    96000    0.028    0.000    0.334    0.000 GASolver_3.py:133(<genexpr>)
    72000    0.092    0.000    0.307    0.000 GASolver_3.py:136(cross_over_single)
   511344    0.171    0.000    0.240    0.000 GASolver_3.py:100(<lambda>)
     9600    0.022    0.000    0.111    0.000 GASolver_3.py:96(<genexpr>)
    14850    0.009    0.000    0.048    0.000 BaseSolver.py:118(__getitem__)
    15383    0.023    0.000    0.036    0.000 BaseSolver.py:111(__calc_hash)
        1    0.000    0.000    0.031    0.031 DPSolver_numba.py:10(DPSolver_2_numba)
   225792    0.021    0.000    0.021    0.000 GASolver_3.py:27(<genexpr>)
      533    0.003    0.000    0.010    0.000 DPSolver.py:8(__init__)
     4950    0.006    0.000    0.009    0.000 GASolver_3.py:11(__init__)
     5483    0.003    0.000    0.003    0.000 BaseSolver.py:11(__init__)
      533    0.001    0.000    0.003    0.000 BaseSolver.py:125(__setitem__)
       48    0.000    0.000    0.002    0.000 GASolver_3.py:82(align_seq)
    14850    0.002    0.000    0.002    0.000 GASolver_3.py:64(<lambda>)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 DPSolver.py:1(<module>)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:34(__init__)
        1    0.000    0.000    0.000    0.000 GASolver_3.py:85(Individual)
        1    0.000    0.000    0.000    0.000 GASolver_3.py:10(GASolver_3)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:10(BaseSolver)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:33(Tester)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:108(__init__)
        1    0.000    0.000    0.000    0.000 DPSolver.py:7(DPSolver_2)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:107(SpeedupHashBin)
        1    0.000    0.000    0.000    0.000 BaseSolver.py:4(FakeFile)
```

