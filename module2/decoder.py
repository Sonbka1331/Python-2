"""Decrypt encryoted message"""
import sys


def decrypt(string: str):
    """Decoder function"""
    while ".." in string:
        edited_string = ""
        string = string.split("..", 1)
        for block in string[:-1]:
            edited_string += block[:-1]
        edited_string += string[-1]
        string = edited_string
    string = "".join(string.split("."))
    print(f"Decrypted message: {string}")
    return string


if __name__ == "__main__":
    decrypt(sys.stdin.readline())
