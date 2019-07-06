#%%
import pandas as pd
import netket as nk
import numpy as np
from python.src.utils import PlotUtils

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

f = PlotUtils.PlotUtils.getLargeScalePlot(tmp_res.query("pb == 1"), exact_arr_pb_true, "PBC, large scale")
f.savefig("PBC_largeScalePlot.png", dpi=300)

f = PlotUtils.PlotUtils.getMediumScalePlot(tmp_res.query("pb == 1"), exact_arr_pb_true, "PBC, medium scale")
f.savefig("PBC_mediumScalePlot.png", dpi=300)

f = PlotUtils.PlotUtils.getLowScalePlot(tmp_res.query("pb == 1"), exact_arr_pb_true, "PBC, low scale")
f.savefig("PBC_lowScalePlot.png", dpi=300)

#%%

f = PlotUtils.PlotUtils.getLargeScalePlot(tmp_res.query("pb == 0"), exact_arr_pb_false, "No PBC, large scale")
f.savefig("noPBC_largeScalePlot.png", dpi=300)

f = PlotUtils.PlotUtils.getMediumScalePlot(tmp_res.query("pb == 0"), exact_arr_pb_false, "No PBC, medium scale")
f.savefig("noPBC_mediumScalePlot.png", dpi=300)

f = PlotUtils.PlotUtils.getLowScalePlot(tmp_res.query("pb == 0"), exact_arr_pb_false, "No PBC, low scale")
f.savefig("noPBC_lowScalePlot.png", dpi=300)