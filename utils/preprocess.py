import numpy as np
from multiprocessing import Pool
from tqdm import tqdm
from utils.load import load, fwords_arr, fcounts_arr
from utils.pattern import pattern

# module-level globals so forked workers inherit them
_words_arr = None
_counts_arr = None

def _init(words_arr, counts_arr):
    global _words_arr, _counts_arr
    _words_arr, _counts_arr = words_arr, counts_arr

def _compute_row(i):
    return pattern(_words_arr, _counts_arr, _words_arr[i])

def build_patterns(dataset, L, save_path=None, chunksize=64, progress=True):
    words = load(dataset, L)
    words_arr = fwords_arr(words)
    counts_arr = fcounts_arr(words)
    n = len(words_arr)

    patterns = np.empty((n, n), dtype=np.min_scalar_type(3**L-1))

    with Pool(initializer=_init, initargs=(words_arr, counts_arr)) as pool:
        it = pool.imap(_compute_row, range(n), chunksize=chunksize)
        if progress:
            it = tqdm(it, total=n)
        for i, row in enumerate(it):
            patterns[i] = row

    if save_path:
        np.save(save_path, patterns)
    return patterns

if __name__ == "__main__":
    build_patterns(save_path="./preprocessed/wordle.npy")