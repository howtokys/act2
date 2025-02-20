from concurrent.futures import ThreadPoolExecutor
import pickle
import threading
import time
import random
from typing import List, Optional

OBJ_BACKLOG = 2000
NUM_OF_PRODUCER = 7
NUM_OF_CONSUMER = 3

added = 0
removed = 0
lengths: List[int] = []

class Queue:
    def __init__(self, max_items: int) -> None:
        self.items: List[Reading] = []
        self.current_items: int = 0
        self.max_items: int = max_items
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)
    
    def add(self, reading: 'Reading') -> None:
        with self.not_full:
            while self.current_items >= self.max_items:
                self.not_full.wait()
            self.items.append(reading)
            self.current_items += 1
            global added
            added += 1
            self.not_empty.notify()
    
    def remove(self, idx: int) -> Optional['Reading']:
        with self.not_empty:
            start_time = time.time()
            while self.current_items == 0:
                if time.time() - start_time > 5:
                    return None
                self.not_empty.wait(timeout=5)
            reading = self.items.pop(idx)
            self.current_items -= 1
            global removed
            removed += 1
            self.not_full.notify()
            return reading

class Reading:
    def __init__(self, code: str, value: int, timestamp: float) -> None:
        self.code: str = code
        self.value: int = value
        self.timestamp: float = timestamp
    
    def __str__(self) -> str:
        return f"Code: {self.code}, Value: {self.value}, Timestamp: {self.timestamp}"

MAX_ITEMS_IN_QUEUE = 100
queue = Queue(MAX_ITEMS_IN_QUEUE)

def producer(num_of_prods: int) -> None:
    for _ in range(num_of_prods):
        code_str = "asQWEfXCVweRqljoOIOIJMEscbvd"
        code = code_str[random.randint(0, len(code_str) - 1)] + str(random.randint(1, 100))
        value = random.randint(1, 100)
        timestamp = time.time()
        r = Reading(code, value, timestamp)
        queue.add(r)

def consumer(file: str) -> None:
    with open(file, "wb") as f:
        lst: List[Reading] = []
        while True:
            reading = queue.remove(0)
            if reading is None:
                break
            lst.append(reading)
            if removed >= OBJ_BACKLOG:
                break
        pickle.dump(lst, f)
        lengths.append(len(lst))

def main() -> None:
    work_per_thread = OBJ_BACKLOG // NUM_OF_PRODUCER
    work_remaining = OBJ_BACKLOG - (work_per_thread * NUM_OF_PRODUCER)

    with ThreadPoolExecutor() as exe:
        for i in range(NUM_OF_PRODUCER):
            if i == NUM_OF_PRODUCER - 1:
                exe.submit(producer, work_per_thread + work_remaining)
            else:
                exe.submit(producer, work_per_thread)

        for j in range(NUM_OF_CONSUMER):
            file_name = f"inventory{j + 1}.pickle"
            exe.submit(consumer, file_name)

if __name__ == "__main__":
    main()
    print(f"Total: added: {added}, removed: {removed}")
    print(lengths, sum(lengths))