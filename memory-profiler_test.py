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
