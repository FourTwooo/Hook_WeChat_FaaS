import time


class DataStore:
    def __init__(self, maxsize=100):
        self.data = {}
        self.maxsize = maxsize

    def put(self, key, value):
        self.data[key] = value

    def get(self, key, timeout=3):
        end_time = time.time() + timeout
        while key not in self.data:
            remaining = end_time - time.time()
            if remaining <= 0.0:
                return None
        return self.data.pop(key)


if __name__ == '__main__':
    store = DataStore()
    for i in range(100):
        store.put(f"uid{i}", str(i))
    print(store.get("uid50"))