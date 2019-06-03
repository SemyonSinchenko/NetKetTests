import json
import os
import pathlib
import scipy.stats as sp
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.style.use("ggplot")

def generate_report(input_file, outdir="plots"):
    iters = []
    energy_mean = []
    energy_sigma = []
    variance_mean = []
    variance_sigma = []

    with open(input_file) as f:
        data = json.load(f)

        for iteration in data["Output"]:
            iters.append(iteration["Iteration"])
            energy_mean.append(iteration["Energy"]["Mean"])
            energy_sigma.append(iteration["Energy"]["Sigma"])
            variance_mean.append(iteration["EnergyVariance"]["Mean"])
            variance_sigma.append(iteration["EnergyVariance"]["Sigma"])

    p95 = sp.distributions.norm().ppf(0.975)

    results_df = pd.DataFrame(
        dict(
            iter=iters,
            e=energy_mean,
            e_std=energy_sigma,
            e_err95=[e * p95 for e in energy_sigma],
            e_var=variance_mean,
            e_var_std=variance_sigma,
            e_var_err95=[e * p95 for e in variance_sigma]
        )
    )

    results_df.to_csv("Results.csv", index=False)

    # Create plots
    f, ax = plt.subplots(nrows=1, ncols=2, figsize=(16, 5))
    ax[0].errorbar(
        results_df["iter"],
        results_df["e"],
        yerr=results_df["e_err95"],
        color="red"
    )
    ax[0].set_xlabel("Iteration")
    ax[0].set_ylabel("Energy")
    ax[0].set_title("Energy by iterations")

    ax[1].errorbar(
        results_df["iter"],
        results_df["e_var"],
        yerr=results_df["e_var_err95"],
        color="red"
    )
    ax[1].set_xlabel("Iteration")
    ax[1].set_ylabel("Variance")
    ax[1].set_title("Variance of energy by iterations")

    f.tight_layout()

    f.savefig(os.path.join(outdir, "results.png"), dpi=300)
    plt.close(f)


def save_results(input_file, prefix, num_iter, exact, params=[], outfile="results.txt", outfolder="ising"):
    """
    Save results to csv file.
    :param input_file: file with result of computations
    :param prefix: name of model or row
    :param num_iter: number of iteration (if greater than one)
    :param exact: exact diagonalization results
    :param params: params of model or row
    :param outfile: csv with result (will be open in append mode)
    :param outfolder: folder prefix
    :return: None
    """
    iters = []
    energy_mean = []
    energy_sigma = []
    variance_mean = []
    variance_sigma = []

    with open(input_file) as f:
        data = json.load(f)

        for iteration in data["Output"]:
            iters.append(iteration["Iteration"])
            energy_mean.append(iteration["Energy"]["Mean"])
            energy_sigma.append(iteration["Energy"]["Sigma"])
            variance_mean.append(iteration["EnergyVariance"]["Mean"])
            variance_sigma.append(iteration["EnergyVariance"]["Sigma"])

    p95 = sp.distributions.norm().ppf(0.975)

    results_df = pd.DataFrame(
        dict(
            iter=iters,
            e=energy_mean,
            e_std=energy_sigma,
            e_err95=[e * p95 for e in energy_sigma],
            e_var=variance_mean,
            e_var_std=variance_sigma,
            e_var_err95=[e * p95 for e in variance_sigma],
            exact=np.ones(len(iters), dtype=np.float64) * exact
        )
    )

    outfolder_name = "Run_"
    for s in params:
        outfolder_name += str(s) + "_"
    outfolder_name += "_folder"

    prefix_path = os.path.join(outfolder, outfolder_name)
    pathlib.Path(prefix_path).mkdir(parents=True, exist_ok=True)
    results_df.to_csv(os.path.join(prefix_path, "Data_iter_{}.csv".format(num_iter)), index=False)
    # Create plots
    f, ax = plt.subplots(nrows=1, ncols=2, figsize=(16, 5))
    ax[0].errorbar(
        results_df["iter"],
        results_df["e"],
        yerr=results_df["e_err95"],
        label="Learning curve",
        color="red"
    )
    ax[0].plot(results_df["iter"], results_df["exact"], "--", label="Exact diagonalization")
    ax[0].set_xlabel("Iteration")
    ax[0].set_ylabel("Energy")
    ax[0].set_title("Energy by iterations")
    ax[0].legend()

    ax[1].errorbar(
        results_df["iter"],
        results_df["e_var"],
        yerr=results_df["e_var_err95"],
        color="red"
    )
    ax[1].set_xlabel("Iteration")
    ax[1].set_ylabel("Variance")
    ax[1].set_title("Variance of energy by iterations")

    f.tight_layout()

    f.savefig(os.path.join(prefix_path, "FittingCurve_iter_{}.png".format(num_iter)), dpi=200)
    plt.close(f)

    res_string = prefix + ","
    for s in params:
        res_string += str(s) + ","
    res_string += str(energy_mean[-1]) + ","
    res_string += str(energy_sigma[-1]) + ","
    res_string += str(variance_mean[-1]) + ","
    res_string += str(variance_sigma[-1]) + ","
    res_string += str(exact) + "\n"

    with open(outfile, "a+") as f:
        f.write(res_string)