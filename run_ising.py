from python.src.Ising import Ising
from python.src.Report import save_results

# PARAMS
N_SPINS = [4, 6, 10, 20, 40, 80, 160, 320]
JZ_CONST = 1
H_CONST = [JZ_CONST * coef
           for coef in (list(range(1, 300)) + [x / 300 for x in range(1, 300)])]

if __name__ == "__main__":
    for spins in N_SPINS:
        for h in H_CONST:
            model = Ising(n_spins=spins, J=JZ_CONST, h=h)
            model.fit("output", max([spins * 12, 100]))
            save_results("output" + '.log',
                         params=[spins, JZ_CONST, h],
                         prefix="ising", outfile="IsingResultsFull.csv")
