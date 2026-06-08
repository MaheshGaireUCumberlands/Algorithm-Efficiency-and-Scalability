import random

class HashTableChaining:
    def __init__(self, initial_capacity=8):
        self._m = max(8, initial_capacity)
        self._n = 0
        self._table = [[] for _ in range(self._m)]
        # choose prime for universal hashing
        self._p = 2**31 - 1
        self._a = random.randrange(1, self._p)
        self._b = random.randrange(0, self._p)

    def _hash(self, key):
        k = hash(key)
        if k < 0:
            k = -k
        return ((self._a * k + self._b) % self._p) % self._m

    def insert(self, key, value):
        idx = self._hash(key)
        bucket = self._table[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._n += 1
        if self.load_factor() > 1.5:
            self._resize(self._m * 2)

    def search(self, key):
        idx = self._hash(key)
        bucket = self._table[idx]
        for k, v in bucket:
            if k == key:
                return v
        return None

    def delete(self, key):
        idx = self._hash(key)
        bucket = self._table[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._n -= 1
                if self._m > 8 and self.load_factor() < 0.4:
                    self._resize(max(8, self._m // 2))
                return True
        return False

    def load_factor(self):
        return self._n / self._m

    def _resize(self, new_m):
        old_items = []
        for bucket in self._table:
            for k, v in bucket:
                old_items.append((k, v))
        self._m = new_m
        self._table = [[] for _ in range(self._m)]
        self._n = 0
        self._a = random.randrange(1, self._p)
        self._b = random.randrange(0, self._p)
        for k, v in old_items:
            self.insert(k, v)

    def __len__(self):
        return self._n

if __name__ == '__main__':
    ht = HashTableChaining()
    ht.insert('a', 1)
    ht.insert('b', 2)
    print('search a =>', ht.search('a'))
    ht.delete('a')
    print('search a after delete =>', ht.search('a'))
