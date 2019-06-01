#%%
import pandas as pd
import pylab


#%%
res = pd.read_csv("IsingResultsFull.csv",
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

pylab.figure(figsize=(6, 4))
pylab.style.use("ggplot")

for i, spins in enumerate(tmp_res["n_spins"].unique()):
    _slice_ = tmp_res[tmp_res["n_spins"] == spins]
    pylab.scatter(_slice_["h"] / _slice_["JZ"],
                  -_slice_["meanEnergy"] / (_slice_["n_spins"] * _slice_["JZ"]), label="N spins = %d" % spins,
                  alpha=0.7, s=6)

pylab.xlabel(r"$\frac{h}{J_z}$")
pylab.ylabel(r"$-\frac{E}{N\times{J_z}}$")
pylab.xlim(0, 12)
pylab.ylim(0, 12)
pylab.legend()
pylab.tight_layout()
pylab.savefig("DifferentNSpins.png", dpi=300)
pylab.show()

#%%