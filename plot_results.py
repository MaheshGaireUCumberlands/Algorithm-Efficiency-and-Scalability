import csv
import matplotlib.pyplot as plt
from collections import defaultdict

def read_results(path='results.csv'):
    data = defaultdict(lambda: defaultdict(list))
    with open(path) as f:
        reader = csv.DictReader(f)
        for r in reader:
            n = int(r['n'])
            mode = r['mode']
            data[mode]['n'].append(n)
            data[mode]['randomized'].append(float(r['randomized']))
            data[mode]['deterministic'].append(float(r['deterministic']))
    return data

def plot(data, out_prefix='plots'):
    for mode, vals in data.items():
        ns = vals['n']
        r = vals['randomized']
        d = vals['deterministic']
        plt.figure()
        plt.plot(ns, r, marker='o', label='randomized')
        plt.plot(ns, d, marker='o', label='deterministic')
        plt.xlabel('n')
        plt.ylabel('time (s)')
        plt.title(f'Sorting time — {mode}')
        plt.legend()
        plt.grid(True)
        plt.savefig(f"{out_prefix}_{mode}.png")
        plt.close()

if __name__ == '__main__':
    data = read_results()
    plot(data)
