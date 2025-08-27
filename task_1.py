import time
import random
import threading
from dataclasses import dataclass, field
from datetime import datetime
from itertools import count
from queue import Queue, Empty

"""
Simulating receiving and processing requests using queue.Queue.

- generate_request(): creates a new request and adds it to the queue
- process_request(): if the queue is not empty — retrieves and "processes" one request
- main loop: constantly generates and processes requests
"""

@dataclass
class Request:
    id: int
    created_at: datetime = field(default_factory=datetime.now)
    payload: dict = field(default_factory=dict)

    def __str__(self) -> str:
        return f"Request(id={self.id}, created_at={self.created_at:%H:%M:%S}, payload={self.payload})"


request_queue: Queue[Request] = Queue()
_id_counter = count(start=1)


def generate_request():
    """
    Creates one new request and adds it to the queue.
    """
    rid = next(_id_counter)
    req = Request(
        id=rid,
        payload={
            "priority": random.choice(["low", "normal", "high"]),
            "source": random.choice(["web", "mobile", "email"]),
        },
    )
    request_queue.put(req)
    print(f"ADDED: {req}")


def process_request():
    """
    If the queue is not empty, it retrieves one request and "processes" it.
    Otherwise, it reports that the queue is empty.
    """
    try:
        req: Request = request_queue.get_nowait()
    except Empty:
        print("The queue is empty - there is nothing to process.")
        return

    print(f"Processing started: {req}")
    time.sleep(random.uniform(0.3, 1.0))
    print(f"Processing completed: Request(id={req.id})")
    request_queue.task_done()


def producer_loop(stop_event: threading.Event, gen_interval_range=(0.2, 0.8)):
    """
    Loop generator: periodically adds 0..N applications.
    """
    while not stop_event.is_set():
        n_new = random.choices([0, 1, 2], weights=[0.2, 0.6, 0.2], k=1)[0]
        for _ in range(n_new):
            generate_request()
        time.sleep(random.uniform(*gen_interval_range))


def consumer_loop(stop_event: threading.Event, proc_interval_range=(0.2, 0.5)):
    """
    Consumer loop: periodically attempts to process a single request.
    """
    while not stop_event.is_set():
        process_request()
        time.sleep(random.uniform(*proc_interval_range))


def main(threaded: bool = True):
    """
    If threaded=True — separate producer/consumer threads .
    If threaded=False — one main loop that generates and processes alternately.
    Stop: Ctrl+C
    """
    print("Start simulation. Press Ctrl+C to stop.\n")

    if threaded:
        stop_event = threading.Event()
        producer = threading.Thread(target=producer_loop, args=(stop_event,), daemon=True)
        consumer = threading.Thread(target=consumer_loop, args=(stop_event,), daemon=True)
        producer.start()
        consumer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStop signal received, terminating...")
            stop_event.set()
            producer.join(timeout=2)
            consumer.join(timeout=2)
    else:
        try:
            while True:
                generate_request()
                process_request()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStop signal received, terminating...")

    if not request_queue.empty():
        print(f"Remaining in the queue: {request_queue.qsize()}")
    print("Done")


if __name__ == "__main__":
    main(threaded=True)
