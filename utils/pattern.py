import numpy as np

def pattern(words_arr, counts_arr, T):
    n = words_arr.shape[0]
    L = words_arr.shape[1]
    
    exact = (words_arr == T)

    consumed = np.zeros((n, 26))
    for j in range(L):
        consumed[:, T[j]] += exact[:, j]
    available = counts_arr - consumed
    stock = available[:, T]

    rank = np.zeros((n, L))
    for l in range(26):
        mask = (T == l)
        rank_l = mask & ~exact
        rank_l = np.cumsum(rank_l, axis = 1)
        rank[:, mask] = rank_l[:, mask]
    
    present = (~exact & (rank <= stock))

    pattern_arr = 2*exact + present
    power = 3**(np.arange(0, L))
    
    return pattern_arr @ power

def score(words_arr, counts_arr, T):
    n = words_arr.shape[0]
    L = words_arr.shape[1]

    pattern_T = pattern(words_arr, counts_arr, T)
    counts = np.bincount(pattern_T, minlength=3**L)
    
    return (counts.astype(np.int64)**2).sum()/n