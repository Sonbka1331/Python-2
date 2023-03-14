import sys


def get_size():
    data = sys.stdin.readlines()[1:]

    files_count = len(data)

    files_size = 0

    not_included_files = 0

    error_message = ""

    if files_count == 0:
        print("Error. Files not found.")

    for line in data:
        try:
            size_value = int(line.split()[4])
            files_size += size_value
        except Exception:
            error_message += f"Unable to determine {line.split()[-1]} size\n"
            not_included_files += 1

    average_file_size = files_size // (files_count - not_included_files)

    if average_file_size > 1000000:
        average_file_size = f"{average_file_size / 1000000} MiB"
    elif average_file_size > 1000:
        average_file_size = f"{average_file_size / 1000} KiB"
    else:
        average_file_size = f"{average_file_size} B"

    print(f"Average file size: {average_file_size}")
    if error_message != "":
        print(f"Error message:\n{error_message}")


if __name__ == '__main__':
    get_size()
