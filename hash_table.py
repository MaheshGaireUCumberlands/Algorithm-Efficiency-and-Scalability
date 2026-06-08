import random


class HashTableChaining:
    """Hash table with chaining and simple universal-style hashing.

    This implementation stores key-value pairs in Python lists (chains).
    It maintains a load factor and resizes (rehashes) when the table becomes
    too full or too empty.
    """

    def __init__(self, initial_capacity=8):
        # number of buckets (m) and number of stored items (n)
        self._m = max(8, initial_capacity)
        self._n = 0
        # initialize empty chains
        self._table = [[] for _ in range(self._m)]
        # parameters for a simple universal-style hash map: h(k) = ((a*k + b) mod p) mod m
        self._p = 2 ** 31 - 1  # large prime
        self._a = random.randrange(1, self._p)
        self._b = random.randrange(0, self._p)

    def _hash(self, key):
        """Compute bucket index for a key.

        Uses Python's built-in `hash()` to obtain an integer then applies a
        linear map modulo a large prime to reduce adversarial collisions.
        """
        k = hash(key)
        if k < 0:
            k = -k
        return ((self._a * k + self._b) % self._p) % self._m

    def insert(self, key, value):
        """Insert or update a key-value pair.

        If the key already exists in the corresponding chain, update the value.
        Otherwise append a new (key, value) tuple and increment the size.
        """
        idx = self._hash(key)
        bucket = self._table[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                # update existing key
                bucket[i] = (key, value)
                return
        # insert new key
        bucket.append((key, value))
        self._n += 1
        # maintain load factor by resizing when table gets too full
        if self.load_factor() > 1.5:
            self._resize(self._m * 2)

    def search(self, key):
        """Return the value for `key` if present, otherwise `None`.

        We compute the bucket index and scan the chain linearly.
        """
        idx = self._hash(key)
        bucket = self._table[idx]
        for k, v in bucket:
            if k == key:
                return v
        return None

    def delete(self, key):
        """Remove `key` from the table if present and return True; else False.

        After deletion we may shrink the table to avoid very low load factors.
        """
        idx = self._hash(key)
        bucket = self._table[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._n -= 1
                # shrink table if too empty (but keep minimum capacity)
                if self._m > 8 and self.load_factor() < 0.4:
                    self._resize(max(8, self._m // 2))
                return True
        return False

    def load_factor(self):
        """Return current load factor alpha = n / m."""
        return self._n / self._m

    def _resize(self, new_m):
        """Resize the underlying table to `new_m` buckets and rehash all items.

        Resizing reselects the hash parameters `a` and `b` to avoid clustering
        from prior choices.
        """
        old_items = []
        for bucket in self._table:
            for k, v in bucket:
                old_items.append((k, v))
        self._m = new_m
        self._table = [[] for _ in range(self._m)]
        self._n = 0
        # re-randomize hashing parameters on resize
        self._a = random.randrange(1, self._p)
        self._b = random.randrange(0, self._p)
        for k, v in old_items:
            self.insert(k, v)

    def __len__(self):
        """Return number of stored entries."""
        return self._n


if __name__ == '__main__':
    # small manual smoke test when file executed directly
    ht = HashTableChaining()
    ht.insert('a', 1)
    ht.insert('b', 2)
    print('search a =>', ht.search('a'))
    ht.delete('a')
    print('search a after delete =>', ht.search('a'))
