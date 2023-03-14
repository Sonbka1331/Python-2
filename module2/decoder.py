import sys


def decrypt():
    data = sys.stdin.readline()
    new_data = ""
    data = data.split("..")
    for block in data:
        new_data += block[:-1]
    data = ''.join(new_data.split("."))
    print(f"Decrypted message: {data}")


if __name__ == "__main__":
    decrypt()
