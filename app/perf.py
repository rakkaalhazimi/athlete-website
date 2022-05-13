import time

class TimeValue:
    def __init__(self, value):
        self.value = value

    def update(self, value):
        self.value = value


class CodeTimer:
    def __init__(self, name=None):
        self.name = f"'{name}'" if name else ''
        self.elapsed = TimeValue(0)

    def __enter__(self):
        self.start = time.time()
        return self.elapsed

    def __exit__(self, exc_type, exc_value, traceback):
        # Calculate runtime
        took = (time.time() - self.start)

        # Save runtime
        self.elapsed.update(took)
        

if __name__ == "__main__":
    timer = CodeTimer()
    with timer as t:
        print("test")

    print(t.value)
