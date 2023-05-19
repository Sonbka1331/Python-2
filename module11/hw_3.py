import random
import threading
import time
import logging

TOTAL_TICKETS = 10
SEATS = 10

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Seller(threading.Thread):
    def __init__(self, semaphore, director_event):
        super().__init__()
        self.sem = semaphore
        self.director_event = director_event
        self.tickets_sold = 0
        logger.info('Seller started work')

    def run(self):
        global TOTAL_TICKETS
        is_running = True
        while is_running:
            self.random_sleep()
            with self.sem:
                if TOTAL_TICKETS <= 0:
                    break
                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                logger.info(f'{self.getName()} sold one; {TOTAL_TICKETS} left')
                if TOTAL_TICKETS == 1:
                    self.director_event.set()
            if TOTAL_TICKETS <= 0:
                break

        logger.info(
            f'Seller {self.getName()} sold {self.tickets_sold} tickets')

    def random_sleep(self):
        time.sleep(random.randint(0, 1))


class Director(threading.Thread):
    def __init__(self, semaphore, director_event):
        super().__init__()
        self.sem = semaphore
        self.director_event = director_event
        logger.info('Director started work')

    def run(self):
        while True:
            self.director_event.wait()
            self.director_event.clear()
            with self.sem:
                global TOTAL_TICKETS
                if TOTAL_TICKETS <= SEATS - 3:
                    tickets_to_add = SEATS - TOTAL_TICKETS
                    TOTAL_TICKETS += tickets_to_add
                    logger.info(
                        f'Director added {tickets_to_add} tickets; {TOTAL_TICKETS} total tickets')
                    if TOTAL_TICKETS == SEATS:
                        break


def main():
    semaphore = threading.Semaphore()
    director_event = threading.Event()
    sellers = []
    director = Director(semaphore, director_event)

    for _ in range(3):
        seller = Seller(semaphore, director_event)
        seller.start()
        sellers.append(seller)

    director.start()

    for seller in sellers:
        seller.join()

    director.join()


if __name__ == '__main__':
    main()
