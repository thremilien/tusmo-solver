import numpy as np

ALPHABET = set(chr(i) for i in range(65, 65+26))

#### Load the data ####
def load(L, file_path="./words_fr/fr_full.txt"):
    with open(file_path, "r") as file:
        words = file.read()
        words = words.split("[")[1].split("]")[0]
        words = [word.replace("\"", "").strip() for word in words.split(",")]
        words = list(filter(lambda x : len(x) == L, words))
        words = list(filter(ffilter, words))
    
    return words

def ffilter(word):
    for letter in word:
        if letter not in ALPHABET:
            return False
    return True

#### Preproces useful data structures ####
def fwords_arr(words):
    n = len(words)
    L = len(words[0])

    words_arr = np.empty((n, L), dtype=int)
    for i, word in enumerate(words):
        for j, letter in enumerate(word):
            words_arr[i, j] = ord(letter) - 65
    
    return words_arr

def fcounts_arr(words):
    n = len(words)
    L = len(words[0])

    counts_arr = np.zeros((n, 26), dtype=int)
    for i, word in enumerate(words):
        for j, letter in enumerate(word):
            counts_arr[i, ord(letter)-65] += 1

    return counts_arr