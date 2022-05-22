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
