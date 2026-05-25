from utils.load import ALPHABET, load, fwords_arr, fcounts_arr
from utils.pattern import pattern, score
import numpy as np
from multiprocessing import Pool
from tqdm import tqdm
import os

L = 5

# Variables globales pour les workers
_words_arr = None
_counts_arr = None

def init_worker(words_arr, counts_arr):
    global _words_arr, _counts_arr
    _words_arr = words_arr
    _counts_arr = counts_arr

def score_one(t_idx):
    T = _words_arr[t_idx]
    s = score(_words_arr, _counts_arr, T)
    return t_idx, s

if __name__ == "__main__":
    words = load("wordle", L)
    words_arr = fwords_arr(words)
    counts_arr = fcounts_arr(words)
    n = len(words_arr)

    n_processes = os.cpu_count() // 2
    chunksize = 100

    with Pool(processes=n_processes,
              initializer=init_worker,
              initargs=(words_arr, counts_arr)) as pool:
        results = list(tqdm(
            pool.imap_unordered(score_one, range(n), chunksize=chunksize),
            total=n
        ))

    # Sort by score ascending
    results.sort(key=lambda x: x[1])

    # Build parallel lists
    sorted_words = [words[idx] for idx, _ in results]
    sorted_scores = [s for _, s in results]

    # Show top 20
    print("Top 20 best words:")
    for w, s in zip(sorted_words[:20], sorted_scores[:20]):
        print(f"  {w}: {s:.2f}")

    print(f"\nBest: {sorted_words[0]} (score {sorted_scores[0]:.2f})")
    print(f"Worst: {sorted_words[-1]} (score {sorted_scores[-1]:.2f})")