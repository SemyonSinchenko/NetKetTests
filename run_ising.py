from python.src.Ising import Ising
from python.src.Report import save_results
import numpy as np

# PARAMS
H_RANGE = list(range(2, 100)) + np.linspace(0.001, 1, 99).tolist()
N_SPINS = [4, 6, 10, 20, 40]
JZ_CONST = 1
H_CONST = [JZ_CONST * coef for coef in H_RANGE]

if __name__ == "__main__":
    for spins in N_SPINS:
        for h in H_CONST:
            model = Ising(n_spins=spins, J=JZ_CONST, h=h)
            model.fit("output", 400)
            save_results("output" + '.log',
                         params=[spins, JZ_CONST, h],
                         prefix="ising", outfile="IsingResultsFull.csv")
