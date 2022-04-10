# Python Memory Debugging

## Memory Profilers

1. [resource.getrusage](#resourcesgetrusage)
1. [sys.getsizeof](#sysgetsizeof)

### Python/OS Environment:
* FreeBSD 13.1-RELEASE
* Python 3.8.12
* `black` formatter

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
