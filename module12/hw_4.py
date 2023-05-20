import threading
import requests
import time


def get_timestamp():
    response = requests.get(
        'http://127.0.0.1:5000/timestamp/' + str(int(time.time())))
    return response.text


def log_to_file(timestamp):
    current_time = timestamp
    log_entry = f"{timestamp} {current_time}\n"
    with open('log.txt', 'a') as file:
        file.write(log_entry)


def worker():
    timestamp = get_timestamp()
    log_to_file(timestamp)
    time.sleep(20)


def main():
    threads = []
    for _ in range(10):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)
        time.sleep(1)

    for t in threads:
        t.join()

    with open('log.txt', 'r') as file:
        lines = file.readlines()
    lines.sort()
    with open('log.txt', 'w') as file:
        file.writelines(lines)


if __name__ == '__main__':
    main()
