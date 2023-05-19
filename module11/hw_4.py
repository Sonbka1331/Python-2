import threading
import queue
import random
import time


class Producer(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        print("Producer: Running")
        for i in range(10):
            priority = random.randint(0, 9)
            task = f"Task(priority={priority})"
            self.queue.put((priority, task))
        print("Producer: Done")


class Consumer(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        print("Consumer: Running")
        while True:
            if not self.queue.empty():
                priority, task = self.queue.get()
                print(f">running {task}. sleep({random.random()})")
                time.sleep(random.random())  # Имитируем выполнение задачи
                self.queue.task_done()
            else:
                break
        print("Consumer: Done")


if __name__ == "__main__":
    task_queue = queue.PriorityQueue()

    producer = Producer(task_queue)
    time.sleep(5)
    consumer = Consumer(task_queue)

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()
