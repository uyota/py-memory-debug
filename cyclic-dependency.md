# Python Cyclic Dependency

## Garbage Collection

Python uses garbage collections.
Therefore, all unused resources are freed and recycled automatically
as an object is no longer referenced from anywhere.

## Cyclic Dependency

The catch is if objects create a cyclic reference, you need to break
it so that these objects lose references.

In other words, there are 2 objects that reference each other.
If these 2 objects are not referenced from any other code, they cane be freed.
However, because these two objects reference each other, Python always
find one reference - Python doesn't yet detect and collect a group of objects.

## Check the Code

This is one reason that your Python program don't refer but Python
interpreter cannot release memory.

Python libraries doesn't have objects that creates cyclic dependency.
So, it is most likely your code.  Check class member variables and how
or if they create a cyclic reference.
