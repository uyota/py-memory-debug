# Python Sparse Memory Usage Debugging

## Garbage Collection

Python uses garbage collections.
Therefore, all unused resources are freed and recycled automatically
as an object is no longer referenced from anywhere.

## Python Interpreter

Python is a interpreter language.
Python reads your program and evaluates and executes each line.
Python interpreter decides when to allocate memory from
or deallocate back to the operating system.

Python also implements its own memory allocator rather than
operating system default to improve general memory usage.

### Python Interpreter Memory Usage v.s. Your Program Memory Usage

There are 2 levels of memory usages: one at Python interpreter level
and your program level.

A Python program usually allocates more memory than you expect as
Python interpreter keeps extra memory for efficiency.

Most of memory profile tools and/or libraries can help to observe
your Python program memory usage.
They can profile where memory is allocated and/or
what is allocating and few other things.

Few tools also intensionally monitor system memory usage.

Operating systems manage memory by much larger sizes compare
to Python objects.  Therefore, Python implements its own memory allocator
to manage smaller allocations efficiently.
In other words, Python interpreter splits a large memory portion into
small pieces to allocate for Python programs to use.

If both program memory usage and Python interpreter's system memory
usage patterns are similar and their difference is small, your
program is using good amount of system memory.

### Estimate Memory Usage

Use profiling tools to get basic memory usage pattern and estimate your
program memory usages for a given dataset.

Estimate both peak memory usage and normal usage.

If memory usage is high but as expected, you need to look into
improving internal data structures and storage to reduce memory usage.

### Low Memory Profiler, Excessive System Memory Usage and Sparse Memory Usage

If profilers tell your program uses memory as low as you estimated but
the operating system may reports your program is using significantly a lot more,
your program created sparse memory usage.

Python interpreter deallocates memory back to the operating system
if all of memory portions within a pagesize is no longer used.
If even a single byte is used on a page, Python interpreter cannot releases
back such to the operation system.

#### Data-Structures to Generator/Co-Routine

Python dict is a very useful and yet powerful data structure provided natively.
List and set are also useful and well used.

Passing a data structure between functions and processing each element
at a time is a very common programming practice.
It is easy to read, write, and follow such programs especially
you need to run multiple data conversions/translations.
On the other hand, passing a large data set from a function to a function and
processing multiple steps tend to make holes on Python interpreter's memory.

If there is a large gap between Python interpreter memory usage and
that of your program's, suspect such sparse memory usage.
Try doubling, tripling, and quadrupling data set and observe if both
Python interpreter memory usage and your program's are proportional to
each other, that's a Python of sparse memory usage.

This happens when a function iterates all elements and modifies each.
A chain of data conversions are such examples.
Both old and new values need to be kept in memory during operation.
When modified data structure is passed onto next conversion,
memory tends to be already fragmented such that next conversion cannot reuse
released memory and results taking more from the operating system.

Convert passing a data structure to Generator.
That allows a function to process one data element at a time instead of a bulk.
This avoid large peak memory usage and reuse same memory segment more often.

##### Case Study

I had written a data caching program.  It used database as a data storage,
converted into Python native types, kept data in dict, and created few lookup
tables for faster access.

Its normal memory usage was expected about 1GB at normal and 2GB at peak.
However, its normal memory usage stayed over 10GB and 20GB at peak.
After investigating with memory profiling tools, the program
memory usage was about 1GB with 2GB at peak.
The estimate was very accurate; however, the system reported 10 times more.
The problem was a large data set was passed over multiple steps
and each step modified some part of data.
The end result after multiple operation was many sparsed memory usage.

Each operation needed the same size as input data as work memory.
Although only few pieces of memory were used over these working memory,
as they were in use, the Python interpreter couldn't release the memory
back to the operating system.

I was able to spot TTL cache was one of 1GB memory user.
After removing extra TTL cache, it immediately released 1GB of memory.
In order to reduce the large work memory, I needed to adjust the code
to process one record at a time by using co-routine instead of passing dict
over multiple function calls.
This change allowed Python interpreter to use small work memory and thus
resulted 7GB of memory usage reduction.

Unfortunately, the 3rd party database library was only able to return
a full dataset.  I had to give up on this library's large work memory.

The end result was 2GB steady memory usage with peak at 4GB at cache refresh.


## Check List

1. Check your program doesn't create a cyclic dependency or properly breaks
down cyclic when destroyed.
1. Check the difference between Python interpreter memory usage and
your program usage.
    1. If difference is unreasonably large or usage pattern is
significantly difference, look for spikes.
