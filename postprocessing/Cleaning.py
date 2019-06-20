#%%
import pandas as pd
import pylab
import netket as nk
import numpy as np

#%%
res = pd.read_csv("/home/sem/OneDrive/Documents/Physics/Ising/results/results/IsingResultsTable.csv",
                  header=None,
                  names=[
                      "prefix", "n_spins",
                      "JZ", "h", "meanEnergy",
                      "stdEnergy", "meanEnergyVariance",
                      "stdEnergyVariance"
                  ])

#%%
naCols = res.isna().sum()
naCols = naCols[naCols > 0]

#%%
print(naCols)

#%%
res = res.drop_duplicates()

#%%
tmp_res = res[res["meanEnergy"].apply(lambda x: x != "None")]
tmp_res["meanEnergy"] = tmp_res["meanEnergy"].astype(float)

#%%

res.to_csv("cleanResultsIsingFirstWithNulls.csv", index=False)
tmp_res.to_csv("cleanResultsIsingFirst.csv", index=False)

#%%
g = nk.graph.Hypercube(length=6, n_dim=1, pbc=True)
space = nk.hilbert.Spin(graph=g, s=0.5, total_sz=0)

H_RANGE = np.linspace(2, 100, 30).tolist() + np.linspace(0, 1, 30).tolist()
N_SPINS = [4, 6, 8, 12, 14, 18, 24]
JZ_CONST = 1
H_CONST = [JZ_CONST * coef for coef in H_RANGE]

exact = [
    [
        h,
        nk.exact.lanczos_ed(nk.operator.Ising(hilbert=space, h=h, J=1), compute_eigenvectors=False).eigenvalues[0] / 6
    ] for h in H_CONST]

#%%
exact_arr = np.array(exact)

#%%

pylab.figure(figsize=(6, 4))
pylab.style.use("ggplot")

for i, spins in enumerate(tmp_res["n_spins"].unique()):
    _slice_ = tmp_res[tmp_res["n_spins"] == spins]
    pylab.scatter(_slice_["h"] / _slice_["JZ"],
                  -_slice_["meanEnergy"] / (_slice_["n_spins"] * _slice_["JZ"]), label="N spins = %d (fitted)" % spins,
                  alpha=0.7, s=6, marker='.')

pylab.scatter(exact_arr[:, 0], -exact_arr[:, 1], marker='x', alpha=0.7, s=6, label="Exact solution")
pylab.xlabel(r"$\frac{h}{J_z}$")
pylab.ylabel(r"$-\frac{E}{N\times{J_z}}$")
pylab.legend()
pylab.tight_layout()
pylab.savefig("DifferentNSpinsFull.png", dpi=300)
pylab.show()

#%%

pylab.figure(figsize=(6, 4))
pylab.style.use("ggplot")

for i, spins in enumerate(tmp_res["n_spins"].unique()):
    _slice_ = tmp_res[tmp_res["n_spins"] == spins]
    pylab.scatter(_slice_["h"] / _slice_["JZ"],
                  -_slice_["meanEnergy"] / (_slice_["n_spins"] * _slice_["JZ"]), label="N spins = %d (fitted)" % spins,
                  alpha=0.7, s=6, marker='.')

pylab.scatter(exact_arr[:, 0], -exact_arr[:, 1], marker='x', alpha=0.7, s=6, label="Exact solution")

pylab.xlabel(r"$\frac{h}{J_z}$")
pylab.ylabel(r"$-\frac{E}{N\times{J_z}}$")
pylab.legend()
pylab.xlim(0, 1)
pylab.ylim(0.7, 2)
pylab.tight_layout()
pylab.savefig("DifferentNSpinsLow.png", dpi=300)
pylab.show()

#%%

#%%

pylab.figure(figsize=(6, 4))
pylab.style.use("ggplot")

for i, spins in enumerate(tmp_res["n_spins"].unique()):
    _slice_ = tmp_res[tmp_res["n_spins"] == spins]
    pylab.scatter(_slice_["h"] / _slice_["JZ"],
                  -_slice_["meanEnergy"] / (_slice_["n_spins"] * _slice_["JZ"]), label="N spins = %d (fitted)" % spins,
                  alpha=0.7, s=6, marker='.')

pylab.scatter(exact_arr[:, 0], -exact_arr[:, 1], marker='x', alpha=0.7, s=6, label="Exact solution")

pylab.xlabel(r"$\frac{h}{J_z}$")
pylab.ylabel(r"$-\frac{E}{N\times{J_z}}$")
pylab.legend()
pylab.xlim(0, 10)
pylab.ylim(0.7, 10)
pylab.tight_layout()
pylab.savefig("DifferentNSpinsLow2.png", dpi=300)
pylab.show()

#%%