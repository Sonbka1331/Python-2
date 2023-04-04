WORDS_PATH = "/usr/share/dict/words"


def my_t9(message: int):
    if '1' in str(message):
        return '1 is not in use'
    codac = {
        '2': ['a', 'b', 'c'],
        '3': ['d', 'e', 'f'],
        '4': ['g', 'h', 'i'],
        '5': ['j', 'k', 'l'],
        '6': ['m', 'n', 'o'],
        '7': ['p', 'q', 'r', 's'],
        '8': ['t', 'u', 'v'],
        '9': ['w', 'x', 'y', 'z']
    }
    words = get_words(len(str(message)), codac[str(message)[0]])
    n = 1
    for number in str(message)[1:]:
        new_words = []
        for word in words:
            if word[n] in codac[number]:
                new_words.append(word)
        words = new_words
        n += 1
    if words == []:
        return "None variants"
    return f"Variants: {', '.join(words)}"


def get_words(words_len = int, first_words = list):
    words = []
    with open(WORDS_PATH, 'r') as all_words:
        for word in all_words:
            if(len(word) == (words_len + 1)) and (word[0] in first_words) : words.append(word.replace("\n", ""))
    return words


if __name__ == '__main__':
    message = 798466
    variants = my_t9(message)
    print(variants)
