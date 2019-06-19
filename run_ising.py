from python.src.Ising import Ising
from python.src.Report import save_results
import numpy as np

# PARAMS
H_RANGE = np.linspace(2, 100, 30).tolist() + np.linspace(0, 1, 30).tolist()
N_SPINS = [4, 6, 8, 12, 14, 18, 24]
JZ_CONST = 1
H_CONST = [JZ_CONST * coef for coef in H_RANGE]

if __name__ == "__main__":
    for spins in N_SPINS:
        num_rounds = max(spins * 20, 150)
        for h in H_CONST:
            model = Ising(n_spins=spins, J=JZ_CONST, h=h)
            model.fit("output", num_rounds)
            obs = model.get_observable()
            save_results("output",
                         prefix="ising",
                         params=[spins, JZ_CONST, h],
                         outfile="/mountV/volume/IsingResultsTable.csv",
                         outfolder="/mountV/volume/DetailedResults",
                         observable=obs)
