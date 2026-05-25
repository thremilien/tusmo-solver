from utils.load import ALPHABET, load, fwords_arr, fcounts_arr
from utils.pattern import pattern, score
import numpy as np

L = 8
words = load(L)
words_arr = fwords_arr(words)
counts_arr = fcounts_arr(words)

best_score = np.inf
best_word = None
for i, T in enumerate(words_arr):
    score_T = score(words_arr, counts_arr, T) 

    if score_T < best_score:
        best_score = score_T
        best_word = words[i]

    print(i)

print(best_score)
print(best_word)