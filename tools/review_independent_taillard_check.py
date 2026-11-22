"""Independent review checks for Şeref's PFSP model (does not import problem.py for computing)."""
import json, sys, hashlib
from pathlib import Path
ROOT = Path(sys.argv[1])

# 1) Taillard (1993) generator written from the paper's description:
#    Park-Miller minimal standard LCG, Schrage factorisation; p_ij = U[1,99];
#    generated machine by machine (outer loop machines, inner loop jobs).
def unif(state, lo, hi):
    a, m, q, r = 16807, 2147483647, 127773, 2836
    k = state // q
    state = a * (state % q) - k * r
    if state < 0:
        state += m
    return state, lo + int((state / m) * (hi - lo + 1))

def taillard(seed, n, mch):
    s = seed; d = [[0]*n for _ in range(mch)]
    for j in range(mch):
        for i in range(n):
            s, d[j][i] = unif(s, 1, 99)
    return [[d[j][i] for j in range(mch)] for i in range(n)]   # job-major

seeds = {"ta001": (873654221, 20, 5), "ta011": (587595453, 20, 10), "ta021": (479340445, 20, 20)}
ref = json.loads((ROOT/"data/taillard/reference_solutions.json").read_text())["instances"]

def read(name):
    lines = [l.split() for l in (ROOT/f"data/taillard/{name}.txt").read_text().splitlines() if l.strip()]
    return [[int(v) for v in row] for row in lines[1:]]

# 2) Makespan by explicit event simulation + overlap check (different from the DP loop).
def schedule(p, perm):
    n_m = len(p[0]); machine_free = [0]*n_m; ops = []
    for job in perm:
        t_job = 0
        for m in range(n_m):
            start = max(machine_free[m], t_job); end = start + p[job][m]
            ops.append((m, job, start, end)); machine_free[m] = end; t_job = end
    # no overlaps on a machine, job order preserved across machines
    for m in range(n_m):
        iv = sorted((s, e) for (mm, _, s, e) in ops if mm == m)
        assert all(iv[k][1] <= iv[k+1][0] for k in range(len(iv)-1))
    return max(e for *_, e in ops)

ok = True
for name, (seed, n, mch) in seeds.items():
    gen = taillard(seed, n, mch); file = read(name)
    same = gen == file
    h = hashlib.sha256((ROOT/f"data/taillard/{name}.txt").read_bytes()).hexdigest()
    perm = ref[name]["reference_permutation_0_based"]
    cmax = schedule(file, perm)
    print(f"{name}: kendi üretecim == dosya: {same}; seed metadata={ref[name]['seed']==seed}; "
          f"sha256 eşleşiyor={h==ref[name]['sha256']}; referans perm ile Cmax={cmax}, BKS={ref[name]['bks']}")
    ok &= same and cmax == ref[name]["bks"]

# 3) Known first row of ta001 machine 1 (OR-Library flowshop2.txt, as I remember it)
print("ta001 makine-1 ilk 5:", [read('ta001')[i][0] for i in range(5)])
print("GENEL:", "PASS" if ok else "FAIL")
