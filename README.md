# Python Memory Debugging

## Memory Profilers

1. [sys.getsizeof](#sysgetsizeof)

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
