#%%
import pandas as pd
import matplotlib.pyplot as plt


#%%
res = pd.read_csv("IsingResults.csv",
                  header=None,
                  names=[
                      "prefix", "n_spins",
                      "JZ", "h", "meanEnergy",
                      "stdEnergy", "meanEnergyVariance",
                      "stdEnergyVariance"
                  ])

#%%
res = res.drop_duplicates()

#%%
tmp_res = res[res["meanEnergy"].apply(lambda x: x != "None")]
tmp_res["meanEnergy"] = tmp_res["meanEnergy"].astype(float)
plt.plot(tmp_res["h"] / tmp_res["JZ"], -tmp_res["meanEnergy"] / (tmp_res["n_spins"] * tmp_res["JZ"]), ".-")
plt.xlabel("h / JZ")
plt.ylabel("E / (n_spins * JZ)")
plt.show()

#%%

res.to_csv("cleanResultsIsingFirstWithNulls.csv", index=False)
tmp_res.to_csv("cleanResultsIsingFirst.csv", index=False)

#%%

plt.plot(tmp_res["h"] / tmp_res["JZ"], -tmp_res["meanEnergy"] / (tmp_res["n_spins"] * tmp_res["JZ"]), ".-")
plt.xlabel("h / JZ")
plt.ylabel("E / (n_spins * JZ)")
plt.xlim(0, 10)
plt.ylim(0, 10)
plt.show()

#%%