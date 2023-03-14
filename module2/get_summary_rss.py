
FILEPATH = "output_file.txt"


def calculate():
    with open(FILEPATH, "r") as file:
        for line in file.readlines()[1:]:
            columns = line.split()
            rss_value = int(columns[5])
            if rss_value < 1000:
                columns[5] = f"{rss_value} B"
            elif rss_value > 1000000:
                rss_value = rss_value / 1000000
                columns[5] = f"{rss_value} MiB"
            elif rss_value >= 1000:
                rss_value = rss_value / 1000
                columns[5] = f"{rss_value} KiB"
            print("".join(columns))


if __name__ == '__main__':
    calculate()
