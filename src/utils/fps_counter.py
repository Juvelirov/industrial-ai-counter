import time


class FPSCounter:
    def __init__(self, buffer_size=15):
        self.buffer = []
        self.buffer_size = buffer_size
        self.prev_tick = time.perf_counter()

    def update(self):
        now = time.perf_counter()
        diff = now - self.prev_tick
        self.prev_tick = now

        if diff > 0:
            self.buffer.append(1.0 / diff)

        if len(self.buffer) > self.buffer_size:
            self.buffer.pop(0)

        return int(sum(self.buffer) / len(self.buffer)) if self.buffer else 0

    def reset(self):
        self.buffer.clear()
        self.prev_tick = time.perf_counter()