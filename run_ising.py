from python.src.Ising import Ising
from python.src.Report import save_results
import numpy as np

# PARAMS
H_RANGE = np.linspace(2, 300, 40).tolist() + np.linspace(0, 1, 20).tolist()
N_SPINS = [4, 6, 8, 10, 12, 14, 16, 18]
JZ_CONST = 1
H_CONST = [JZ_CONST * coef for coef in H_RANGE]

if __name__ == "__main__":
    for spins in N_SPINS:
        for h in H_CONST:
            model = Ising(n_spins=spins, J=JZ_CONST, h=h)
            model.fit("output", 1500)
            exact = model.get_exact()
            obs = model.get_observable()
            save_results("output",
                         prefix="ising",
                         exact=exact,
                         params=[spins, JZ_CONST, h],
                         outfile="IsingResultsFull.csv",
                         outfolder="IsingRun",
                         observable=obs)
