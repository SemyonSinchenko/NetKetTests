from python.src.Ising import Ising
from python.src.Report import save_results
import numpy as np

# PARAMS
H_RANGE = np.linspace(0, 15, 200).tolist()
N_SPINS = [4, 6, 8, 12, 14]
JZ_CONST = 1
H_CONST = [JZ_CONST * coef for coef in H_RANGE]

if __name__ == "__main__":
    for pb in [True, False]:
        for spins in N_SPINS:
            num_rounds = max(spins * 20, 150)
            for h in H_CONST:
                model = Ising(n_spins=spins, J=JZ_CONST, h=h, pb=pb)
                model.fit("output", num_rounds)
                obs = model.get_observable()
                save_results("output",
                             prefix="ising",
                             params=[spins, JZ_CONST, h],
                             outfile="/mountV/volume/IsingResultsTablePB_{}.csv".format(pb),
                             outfolder="/mountV/volume/DetailedResultsPB_{}".format(pb),
                             observable=obs)
