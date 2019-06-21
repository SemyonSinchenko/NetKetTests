#%%
import pandas as pd
import pylab
import netket as nk
import numpy as np

#%%
res_pb_true = pd.read_csv("/home/sem/OneDrive/Documents/Physics/Ising/results/results/IsingResultsTablePB_True.csv",
                  header=None,
                  names=[
                      "prefix", "n_spins",
                      "JZ", "h", "meanEnergy",
                      "stdEnergy", "meanEnergyVariance",
                      "stdEnergyVariance"
                  ])

res_pb_false = pd.read_csv("/home/sem/OneDrive/Documents/Physics/Ising/results/results/IsingResultsTablePB_False.csv",
                  header=None,
                  names=[
                      "prefix", "n_spins",
                      "JZ", "h", "meanEnergy",
                      "stdEnergy", "meanEnergyVariance",
                      "stdEnergyVariance"
                  ])

res_pb_true["pb"] = np.ones(res_pb_true.shape[0])
res_pb_false["pb"] = np.zeros(res_pb_false.shape[0])

res = pd.concat([res_pb_true, res_pb_false])
print(res.shape)

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
g = nk.graph.Hypercube(length=6, n_dim=1, pbc=True)
space = nk.hilbert.Spin(graph=g, s=0.5, total_sz=0)

H_RANGE = np.linspace(0, 15, 200).tolist()
N_SPINS = [4, 6, 8, 12, 14]
JZ_CONST = 1
H_CONST = [JZ_CONST * coef for coef in H_RANGE]

exact_pb_true = [
    [
        h,
        nk.exact.lanczos_ed(nk.operator.Ising(hilbert=space, h=h, J=1), compute_eigenvectors=False).eigenvalues[0] / 6
    ] for h in H_CONST]

g = nk.graph.Hypercube(length=6, n_dim=1, pbc=False)
space = nk.hilbert.Spin(graph=g, s=0.5, total_sz=0)

exact_pb_false = [
    [
        h,
        nk.exact.lanczos_ed(nk.operator.Ising(hilbert=space, h=h, J=1), compute_eigenvectors=False).eigenvalues[0] / 6
    ] for h in H_CONST]

#%%
exact_arr_pb_true = np.array(exact_pb_true)
exact_arr_pb_false = np.array(exact_pb_false)

#%%

pylab.figure(figsize=(10, 6))
pylab.style.use("ggplot")

for i, spins in enumerate(tmp_res["n_spins"].unique()):
    _slice_0 = tmp_res[(tmp_res["n_spins"] == spins) & (tmp_res["pb"] == 1)]
    pylab.scatter(_slice_0["h"] / _slice_0["JZ"],
                  -_slice_0["meanEnergy"] / (_slice_0["n_spins"] * _slice_0["JZ"]),
                  label="N spins = %d (fitted), PBC=True" % spins,
                  alpha=0.7, s=7, marker='o')

    _slice_1 = tmp_res[(tmp_res["n_spins"] == spins) & (tmp_res["pb"] == 0)]
    pylab.scatter(_slice_1["h"] / _slice_1["JZ"],
                  -_slice_1["meanEnergy"] / (_slice_1["n_spins"] * _slice_1["JZ"]),
                  label="N spins = %d (fitted), PBC=False" % spins,
                  alpha=0.7, s=7, marker='x')

pylab.scatter(exact_arr_pb_true[:, 0], -exact_arr_pb_true[:, 1], marker='^', alpha=0.7, s=7, label="Exact solution (PBC=True)")
pylab.scatter(exact_arr_pb_false[:, 0], -exact_arr_pb_false[:, 1], marker='^', alpha=0.7, s=7, label="Exact solution (PBC=False)")
pylab.xlabel(r"$\frac{h}{J_z}$")
pylab.ylabel(r"$-\frac{E}{N\times{J_z}}$")
pylab.legend()
pylab.tight_layout()
pylab.savefig("DifferentNSpinsFull.png", dpi=300)
pylab.show()

#%%

pylab.figure(figsize=(10, 6))
pylab.style.use("ggplot")

for i, spins in enumerate(tmp_res["n_spins"].unique()):
    _slice_0 = tmp_res[(tmp_res["n_spins"] == spins) & (tmp_res["pb"] == 1)]
    pylab.scatter(_slice_0["h"] / _slice_0["JZ"],
                  -_slice_0["meanEnergy"] / (_slice_0["n_spins"] * _slice_0["JZ"]),
                  label="N spins = %d (fitted), PBC=True" % spins,
                  alpha=0.7, s=7, marker='o')

    _slice_1 = tmp_res[(tmp_res["n_spins"] == spins) & (tmp_res["pb"] == 0)]
    pylab.scatter(_slice_1["h"] / _slice_1["JZ"],
                  -_slice_1["meanEnergy"] / (_slice_1["n_spins"] * _slice_1["JZ"]),
                  label="N spins = %d (fitted), PBC=False" % spins,
                  alpha=0.7, s=7, marker='x')

pylab.scatter(exact_arr_pb_true[:, 0], -exact_arr_pb_true[:, 1], marker='^', alpha=0.7, s=7, label="Exact solution (PBC=True)")
pylab.scatter(exact_arr_pb_false[:, 0], -exact_arr_pb_false[:, 1], marker='^', alpha=0.7, s=7, label="Exact solution (PBC=False)")
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

pylab.figure(figsize=(10, 6))
pylab.style.use("ggplot")

for i, spins in enumerate(tmp_res["n_spins"].unique()):
    _slice_0 = tmp_res[(tmp_res["n_spins"] == spins) & (tmp_res["pb"] == 1)]
    pylab.scatter(_slice_0["h"] / _slice_0["JZ"],
                  -_slice_0["meanEnergy"] / (_slice_0["n_spins"] * _slice_0["JZ"]),
                  label="N spins = %d (fitted), PBC=True" % spins,
                  alpha=0.7, s=7, marker='o')

    _slice_1 = tmp_res[(tmp_res["n_spins"] == spins) & (tmp_res["pb"] == 0)]
    pylab.scatter(_slice_1["h"] / _slice_1["JZ"],
                  -_slice_1["meanEnergy"] / (_slice_1["n_spins"] * _slice_1["JZ"]),
                  label="N spins = %d (fitted), PBC=False" % spins,
                  alpha=0.7, s=7, marker='x')

pylab.scatter(exact_arr_pb_true[:, 0], -exact_arr_pb_true[:, 1], marker='^', alpha=0.7, s=7, label="Exact solution (PBC=True)")
pylab.scatter(exact_arr_pb_false[:, 0], -exact_arr_pb_false[:, 1], marker='^', alpha=0.7, s=7, label="Exact solution (PBC=False)")
pylab.xlabel(r"$\frac{h}{J_z}$")
pylab.ylabel(r"$-\frac{E}{N\times{J_z}}$")
pylab.legend()
pylab.xlim(0, 10)
pylab.ylim(0.7, 10)
pylab.tight_layout()
pylab.savefig("DifferentNSpinsLow2.png", dpi=300)
pylab.show()

#%%