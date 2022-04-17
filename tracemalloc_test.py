import tracemalloc


tracemalloc.start()


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

snapshot = tracemalloc.take_snapshot()

top_stats = snapshot.statistics("lineno")

print("[ Top 10 ]")
for stat in top_stats[:10]:
    print(stat)
