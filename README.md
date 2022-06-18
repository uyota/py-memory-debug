# Python Memory Debugging

Python programs run on Python interpreter and Python also uses garbage
collections.

Python releases memory as an object is no longer referenced.
Therefore, you don't really need to worry about memory leaks in general.

However, there are times when memory usage is significantly higher than
expected or memory usage keeps growing.   Then, you need to check
few ways to make memory leaks in Python and also need to investigate
where and how memory is used.

While investigating [memory profilers](#memory-profilers) will help
identifying and answering some of these questions.


## Case Study

1. [Cyclic Dependency](cyclic-dependency.md)
1. [Sparse Memory Usage](sparse-memory-usage.md)


## Memory Profilers

1. [Memray](#memray)
1. [guppy/heapy](#guppyheapy)
1. [memory-profiler](#memory-profiler)
1. [psutil](#psutil)
1. [tracemallloc](#tracemalloc)
1. [resource.getrusage](#resourcesgetrusage)
1. [sys.getsizeof](#sysgetsizeof)

### Python/OS Environment:
* FreeBSD 13.1-RELEASE
* Python 3.8.12
* `black` formatter

## [Memray](https://github.com/bloomberg/memray)

A profiler that runs and examines from the outside of a program.
The best choice among other techniques and easiest to use on Linux.
Framegrah provides very visual way to show memory usage brake down
among function calls.

###  Pros

1. Easy to use.
1. No need to change target code.
1. Framegraph gives quick and easy view of high memory users.
1. Can profile C/C++ code.
1. Interactive profileing, too.

###  Cons

1. Linux only.
1. Need to boot up http server to view results.

### [Installation](https://github.com/bloomberg/memray#installation)

``` bash
% python3 -m venv memray-venv
% source memray-venv/bin/activate
[memray-venv] % python3 -m pip install memray
```

### [How To Run](https://github.com/bloomberg/memray#usage)

```
% python3 -m memray run -o output.bin my_script.py arg1 arg2
% python3 -m memray run -o output.bin -m my_module arg1 arg2
```

### [How To Display](https://github.com/bloomberg/memray#usage)

```
% python3 -m memray flame-graph output.bin
```

![Flame-graph View](https://github.com/bloomberg/memray/blob/main/docs/_static/images/flamegraph_example.png?raw=true)

#### [Profile C/C++ Functions](https://github.com/bloomberg/memray#native-mode)

The memray supports profiling C/C++ functions. Use `--native` mode.

#### [Live Profiling](https://github.com/bloomberg/memray#native-mode)

The memray supports realtime progilig with `--live` mode.
You can see memory allocations by functions and by threads.


## [Guppy/Heapy](https://github.com/zhuyifei1999/guppy3/)

The heapy can report the amount of memory allocated by types.

Unlike other memory profiling tool, heapy becomes more useful when
a program defines it own types.


### Pros

1. Easy to use.

### Cons

1. Cannot find where and how memory is used.
1. Requires extra coding.

### Installation

``` bash
% python3 -m venv guppy-venv
% source guppy-venv/bin/activate
% pip install guppy3
```

### [Sample - guppy_test.py](./guppy_test.py)

```
from guppy import hpy

hp = hpy()
hp.setrelheap()


class MemEater:
    def __init__(self):
        self._dict = dict()
        self._all = ""

    def eat(self, n: int):
        for i in range(n):
            self._dict[i] = str(i)
        self._all = " ".join(self._dict.values())


e = MemEater()
e.eat(12345)

print(hp.heap())
print("*" * 80)
print("Heap Size:", hp.heap().size)
print("*" * 80)
print("Most Allocated:\n", hp.heap()[0])
```

#### [Sample Output - getsizeof_out.txt](./getsizeof_out.txt)

```
[guppy-venv] % python guppy_test.py
Partition of a set of 24546 objects. Total size = 859144 bytes.
 Index  Count   %     Size   % Cumulative  % Kind (class / dict of class)
     0  12345  50   359240  42    359240  42 str
     1      2   0   327856  38    687096  80 dict (no owner)
     2  12187  50   170620  20    857716 100 int
     3      1   0      536   0    858252 100 type
     4      1   0      332   0    858584 100 types.FrameType
     5      1   0      192   0    858776 100 dict of type
     6      2   0      136   0    858912 100 function
     7      2   0       64   0    858976 100 types.GetSetDescriptorType
     8      1   0       56   0    859032 100 dict of __main__.MemEater
     9      2   0       52   0    859084 100 tuple
<2 more rows. Type e.g. '_.more' to view.>
********************************************************************************
Heap Size: 859977
********************************************************************************
Most Allocated:
 Partition of a set of 12347 objects. Total size = 360052 bytes.
 Index  Count   %     Size   % Cumulative  % Kind (class / dict of class)
     0  12347 100   360052 100    360052 100 str
```

## [memory-profiler](https://github.com/pythonprofilers/memory_profiler)

The getsizeof function can report memory allocation line by line.


### Pros

1. Easy to use for small functions.

### Cons

1. Cannot get total use of memory.
1. Requires adding decorator.
1. May not be possible to add decorator to all functions.
1. Deallocations are not discounted.

### Installation

``` bash
% python3 -m venv mp-venv
% source mp-venv/bin/activate
% pip install memory_profiler
```

### [Sample - memory-profiler_test.py](./memory-profiler_test.py)

```
class MemEater:
    @profile
    def __init__(self):
        self._dict = dict()
        self._all = ""

    @profile
    def eat(self, n: int):
        for i in range(n):
            self._dict[i] = str(i)
        self._all = " ".join(self._dict.values())


e = MemEater()
e.eat(12345)
```

#### [Sample Output - memory-profiler_out.txt](./memory-profiler_out.txt)

```
[mp-venv] % python -m memory_profiler memory-profiler_test.py
Filename: memory-profiler_test.py

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
     2   13.973 MiB   13.973 MiB           1       @profile
     3                                             def __init__(self):
     4   13.973 MiB    0.000 MiB           1           self._dict = dict()
     5   13.973 MiB    0.000 MiB           1           self._all = ""


Filename: memory-profiler_test.py

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
     7   13.973 MiB   13.973 MiB           1       @profile
     8                                             def eat(self, n: int):
     9   15.023 MiB    0.188 MiB       12346           for i in range(n):
    10   15.023 MiB    0.863 MiB       12345               self._dict[i] = str(i)
    11   15.023 MiB    0.000 MiB           1           self._all = " ".join(self._dict.values())
```

## [psutil](https://psutil.readthedocs.io/en/latest/)

The psutil library functions can report process information from the operating system such as CPU usage, various types of memory usage, and others.

### Pros

1. Easy to use.
1. Find memory usage from operating system view.

### Cons

1. Cannot find where and how memory is used.
1. Does not include swapped out memory.
1. Similar to [resource.getrusage](#resourcesgetrusage).

### [Sample - psutil_test.py](./psutil_test.py)

```
import psutil


class MemEater:
    def __init__(self):
        self._dict = dict()
        self._all = ""

    def eat(self, n: int):
        for i in range(n):
            self._dict[i] = str(i)
        self._all = " ".join(self._dict.values())


e = MemEater()
e.eat(12345)

print(psutil.Process().memory_info())
print(psutil.Process().memory_info().rss)
# in bytes
```

#### [Sample Output - psutil_out.txt](./psutil_out.txt)

```
% python psutil_test.py
pmem(rss=10760192, vms=15769600, text=4096, data=4096, stack=131072)
10764288
```


## [tracemalloc](https://docs.python.org/3/library/tracemalloc.html)

The tracemalloc is capable of capturing memory allocations by line numbers.

### Pros

1. A part of standard library.
1. Easy to use.

### Cons

1. Cannot get total use of memory.
1. Requires extra coding.

### [Sample - tracemalloc_test.py](./tracemalloc_test.py)

```
     1	import tracemalloc
     2	
     3	
     4	tracemalloc.start()
     5	
     6	class MemEater:
     7	    def __init__(self):
     8	        self._dict = dict()
     9	        self._all = ""
    10	
    11	    def eat(self, n: int):
    12	        for i in range(n):
    13	            self._dict[i] = str(i)
    14	        self._all = " ".join(self._dict.values())
    15	
    16	
    17	e = MemEater()
    18	e.eat(12345)
    19	
    20	snapshot = tracemalloc.take_snapshot()
    21	
    22	top_stats = snapshot.statistics("lineno")
    23	
    24	print("[ Top 10 ]")
    25	for stat in top_stats[:10]:
    26	    print(stat)
```

#### [Sample Output - tracemalloc_out.txt](./tracemalloc_out.txt)

```
% python tracemalloc_test.py
[ Top 10 ]
tracemalloc_test.py:13: size=671 KiB, count=12346, average=56 B
tracemalloc_test.py:12: size=165 KiB, count=12088, average=14 B
tracemalloc_test.py:14: size=61.5 KiB, count=1, average=61.5 KiB
tracemalloc_test.py:6: size=1220 B, count=9, average=136 B
tracemalloc_test.py:11: size=156 B, count=2, average=78 B
tracemalloc_test.py:7: size=68 B, count=1, average=68 B
tracemalloc_test.py:8: size=56 B, count=2, average=28 B
tracemalloc_test.py:17: size=24 B, count=1, average=24 B
```

## [resources.getrusage](https://docs.python.org/3/library/resource.html#resource.getrusage)

The getrusage function can report process information from the operating system
such as CPU usage, various types of memory usage, and others.

The MAXRSS reports maximum resident set size.  This value is one of the
best choise to monitor for most cases.

### Pros

1. Can file memory allocation from the operating system view.
1. A part of standard library.
1. Easy to use.
1. Indicates actual physical memory usage.

### Cons

1. Cannot find where and how memory is used.
1. Does not include swapped out memory.

### [Sample - resource_test.py](./resource_test.py)

```
import resource

print(resource.getrusage(resource.RUSAGE_SELF))
print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
# in bytes


class MemEater:
    def __init__(self):
        self._dict = dict()
        self._all = ""

    def eat(self, n: int):
        for i in range(n):
            self._dict[i] = str(i)
        self._all = " ".join(self._dict.values())


e = MemEater()
e.eat(12345)

print(resource.getrusage(resource.RUSAGE_SELF))
print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
```

#### [Sample Output - resource_out.txt](./resource_out.txt)

```
% python resource_test.py
resource.struct_rusage(ru_utime=0.014362, ru_stime=0.007181, ru_maxrss=6092, ru_ixrss=12, ru_idrss=12, ru_isrss=384, ru_minflt=616, ru_majflt=0, ru_nswap=0, ru_inblock=0, ru_oublock=0, ru_msgsnd=0, ru_msgrcv=0, ru_nsignals=0, ru_nvcsw=1, ru_nivcsw=1)
6092
resource.struct_rusage(ru_utime=0.021367, ru_stime=0.0072039999999999995, ru_maxrss=6940, ru_ixrss=16, ru_idrss=16, ru_isrss=512, ru_minflt=916, ru_majflt=0, ru_nswap=0, ru_inblock=0, ru_oublock=0, ru_msgsnd=0, ru_msgrcv=0, ru_nsignals=0, ru_nvcsw=1, ru_nivcsw=1)
6940
```

## [sys.getsizeof](https://docs.python.org/3/library/sys.html#sys.getsizeof)

The getsizeof function can report the amount of memory that an object allocates itself.  The amount does not include indirect memory usage.  For example,
if a class has a str field, a reference to a str value is counted towards
the allocation but not the size of a str object itself.


### Pros

1. A part of standard library.
1. Easy to use.

### Cons

1. Cannot get total use of memory.
1. Requires extra coding.

### [Sample - getsizeof_test.py](./getsizeof_test.py)

```
import sys


class MemEater:
    def __init__(self):
        self._dict = dict()
        self._all = ""

    def eat(self, n: int):
        for i in range(n):
            self._dict[i] = str(i)
        self._all = " ".join(self._dict.values())


e = MemEater()
e.eat(12345)

print(sys.getsizeof(e))
# in bytes
```

#### [Sample Output - getsizeof_out.txt](./getsizeof_out.txt)

```
% python getsizeof_test.py
24
```
