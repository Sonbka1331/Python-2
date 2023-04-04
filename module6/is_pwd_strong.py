import re

WORDS_PATH = "/usr/share/dict/words"


def is_strong_password(password: str, words: list):
    words_pattern = '[a-z]+'
    pwd = re.findall(words_pattern, password.lower(), flags=re.IGNORECASE)
    for password_word in pwd:
        if password_word not in words:
            return False
    return True


def get_words():
    words = []
    with open(WORDS_PATH, 'r') as all_words:
        for word in all_words:
            if len(word) >= 4 : words.append(word.replace("\n", ""))
    return words


if __name__ == '__main__':
    words = get_words()
    password = 'tHe_mOsT_hArDeSt_PaSsWoRd_123'
    x = is_strong_password(password, words)
    print(x)
