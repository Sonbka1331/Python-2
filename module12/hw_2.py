import subprocess


def process_count(username: str) -> int:
    # Количество процессов, запущенных из-под текущего пользователя username
    command = f"ps -u {username} -o pid="
    output = subprocess.check_output(command, shell=True, encoding="utf-8")
    pids = output.strip().split("\n")
    return len(pids)


def total_memory_usage(root_pid: int) -> float:
    # Суммарное потребление памяти древа процессов с корнем root_pid в процентах
    command = f"ps -o %mem= --ppid {root_pid}"
    output = subprocess.check_output(command, shell=True, encoding="utf-8")
    memory_usages = output.strip().split("\n")
    total_memory = sum(float(mem.strip()) for mem in memory_usages)
    return total_memory


if __name__ == '__main__':

    # Пример использования
    username = "your_username"
    count = process_count(username)
    print(f"Количество процессов пользователя {username}: {count}")

    root_pid = 1  # Пример PID корневого процесса (обычно 1 - процесс init)
    memory_usage = total_memory_usage(root_pid)
    print(f"Суммарное потребление памяти древа процессов с корнем {root_pid}: {memory_usage}%")
