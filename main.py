import argparse
from collections import defaultdict
from timeit import repeat

import pandas as pd
import psutil
from pymagnitude import *

VECTOR_ATTRS = ['query', '_vector_for_key_cached', '_out_of_vocab_vector_cached']


def clear_caches(vector):
    for attr in VECTOR_ATTRS:
        getattr(vector, attr)._cache.clear()


def log_cached(vector):
    data = defaultdict(list)
    cache_attrs = ['size', 'lookups', 'hits', 'misses', 'evictions']
    for attr in VECTOR_ATTRS:
        for cache_attr in cache_attrs:
            data[cache_attr].append(getattr(getattr(vector, attr)._cache, cache_attr))
    df = pd.DataFrame(data, index=VECTOR_ATTRS)
    print(df, '\n')


def log_stats(vector, words, reversed_words):
    print('### Query words ...')
    vector.query(words)
    log_cached(vector)

    print('### Query reversed data ...')
    vector.query(reversed_words)
    log_cached(vector)


def run_benchmark(vector, words, reversed_words):
    clear_caches(vector)
    vector.query(words)
    vector.query(reversed_words)


def main():
    pid = os.getpid()
    ps = psutil.Process(pid)
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', required=True)
    parser.add_argument('-m', '--mode', choices=['stats', 'benchmark'], default='stats')
    parser.add_argument('-n', '--benchmark-runs', type=int, default=10)
    parser.add_argument('-l', '--limit', type=int, default=0)
    parser.add_argument('--magnitude-model', default='glove/medium/glove.twitter.27B.25d')
    parser.add_argument('--language', default='en')
    args = parser.parse_args()

    words = open(args.input_file, 'r', encoding='utf8').readlines()
    if args.limit:
        words = words[:args.limit]
    words = [w.strip() for w in words]
    reversed_words = list(reversed(words))
    vector = Magnitude(path=MagnitudeUtils.download_model(args.magnitude_model, log=True),
                       language=args.language,
                       lazy_loading=2400000)

    if args.mode == 'stats':
        log_stats(vector, words, reversed_words)
    elif args.mode == 'benchmark':
        times = repeat(lambda: run_benchmark(vector, words, reversed_words), repeat=args.benchmark_runs, number=1)
        print(pd.DataFrame(dict(time=times)).describe(percentiles=[.25, .5, .75, .9, .99]))
    print(ps.cpu_times())
    print(ps.memory_info())
    try:
        print(ps.io_counters())
    except:
        pass


if __name__ == '__main__':
    main()
