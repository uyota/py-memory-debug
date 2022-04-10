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
