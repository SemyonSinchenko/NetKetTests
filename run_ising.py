from python.src.Ising import Ising
from python.src.Report import save_results
import numpy as np

# PARAMS
H_RANGE = list(range(2, 100, 5)) + np.linspace(0.001, 1, 20).tolist()
N_SPINS = [4, 6, 8, 10, 12, 14, 16, 18]
JZ_CONST = 1
H_CONST = [JZ_CONST * coef for coef in H_RANGE]

if __name__ == "__main__":
    for spins in N_SPINS:
        for h in H_CONST:
            exact = -1
            for i in range(2):
                model = Ising(n_spins=spins, J=JZ_CONST, h=h)
                model.fit("output", 400)
                if i==0:
                    exact = model.get_exact()
                save_results("output" + '.log',
                             prefix="ising",
                             num_iter=i,
                             exact=exact,
                             params=[spins, JZ_CONST, h],
                             outfile="IsingResultsFull.csv", outfolder="IsingRun")
