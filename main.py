from utils.preprocess import build_patterns
from utils.load import load

from multiprocessing import Pool
from datetime import datetime
from functools import partial
from tqdm import tqdm
import numpy as np
import logging
import os

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(asctime)s > %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger(__name__)

L = 5
dataset = "wordle"
log.info(f"Words loaded")

# Load the words
words = load(dataset, L)
n = len(words)

# Load the patterns
try:
    patterns = np.load(f"./preprocessed/{dataset}.npy") # TODO for bigger file try to change nmap here
except:
    log.info(f"Patterns preprocessed file is not present, processing them...")
    build_patterns(dataset, L, save_path="./preprocessed/wordle.npy")
    patterns = np.load(f"./preprocessed/{dataset}.npy") # TODO for bigger file try to change nmap here
log.info(f"Patterns loaded")



###### Processing the scores ######
def score(T, S, d=1, reduction_factor=3, beam=15):
    order = np.argsort(patterns[T][S], kind="stable")
    offsets = np.concatenate(([0], np.cumsum(np.bincount(patterns[T][S], minlength=3**L))))

    total = 1.0
    for k in range(len(offsets)-1):
        subS = S[order[offsets[k]:offsets[k+1]]]

        if len(subS) <= 1 : cost = 0
        elif d == 1: cost = np.log(len(subS)) / np.log(reduction_factor) 
        else : 
            # Process the flat score for each word then choose the best ones
            flats = [(np.bincount(patterns[t][subS], minlength=3**L).astype(np.int64)**2).sum() for t in range(n)]
            cost = min([score(t, subS, d-1, reduction_factor, beam) for t in np.argsort(flats)[:beam]])

        total += (len(subS)/len(S))*cost

    return total

def _eval(T, d, reduction_factor, beam):
    return score(T, np.arange(n), d=d, reduction_factor=reduction_factor, beam=beam)

if __name__ == "__main__":
    worker1 = partial(_eval, d=1, reduction_factor=3, beam=np.inf)
    with Pool(os.cpu_count()-2) as pool:
        scores1 = np.array(list(tqdm(pool.imap(worker1, range(n), chunksize=2), total=n)))

    top50 = np.argsort(scores1)[:50]

    worker2 = partial(_eval, d=2, reduction_factor=3, beam=15)
    with Pool(os.cpu_count()-2) as pool:
        scores2 = np.array(list(tqdm(pool.imap(worker2, top50, chunksize=1), total=len(top50))))

    order = np.argsort(scores2)
    print("Top 20 (d=2):")
    for rank, j in enumerate(order[:20], 1):
        i = top50[j]
        print(f"{rank:2d}. {words[i]:8s} d1={scores1[i]:.4f} d2={scores2[j]:.4f}")

    np.save("./preprocessed/scores.npy", scores1)