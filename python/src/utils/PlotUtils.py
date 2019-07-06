import pylab
import pandas as pd
import numpy as np

class PlotUtils(object):
    def __init__(self):
        pass

    @staticmethod
    def getLargeScalePlot(slice: pd.DataFrame, exact: np.array, label:str):
        """

        :param slice:
        :param exact:
        :param label
        :return:
        """

        f = pylab.figure(figsize=(10, 6))
        ax = pylab.axes()

        for i, spins in enumerate(slice["n_spins"].unique()):
            slice_ = slice.query("n_spins == %d" % spins)
            ax.scatter(slice_["h"] / slice["JZ"],
                       -slice["meanEnergy"] / (slice["n_spins"] * slice["JZ"]),
                       label="N spins = %d (fitted)" % spins,
                       alpha=0.9, s=8, marker='o')

        ax.scatter(exact[:, 0], -exact[:, 1], marker='^', alpha=0.9, s=8,
                      label="Exact solution")
        ax.set_xlabel(r"$\frac{h}{J_z}$")
        ax.set_ylabel(r"$-\frac{E}{N\times{J_z}}$")
        ax.set_xlim(-0.1)
        ax.set_title(label)
        ax.legend()
        ax.grid()
        f.tight_layout()

        return f

    @staticmethod
    def getMediumScalePlot(slice: pd.DataFrame, exact: np.array, label:str):
        """

        :param slice:
        :param exact:
        :param label
        :return:
        """

        f = pylab.figure(figsize=(10, 6))
        ax = pylab.axes()

        for i, spins in enumerate(slice["n_spins"].unique()):
            slice_ = slice.query("n_spins == %d" % spins)
            ax.scatter(slice_["h"] / slice["JZ"],
                       -slice["meanEnergy"] / (slice["n_spins"] * slice["JZ"]),
                       label="N spins = %d (fitted)" % spins,
                       alpha=0.9, s=8, marker='o')

        ax.scatter(exact[:, 0], -exact[:, 1], marker='^', alpha=0.9, s=8,
                  label="Exact solution")
        ax.set_xlabel(r"$\frac{h}{J_z}$")
        ax.set_ylabel(r"$-\frac{E}{N\times{J_z}}$")
        ax.set_title(label)
        ax.legend()
        ax.set_xlim(-0.1, 10)
        ax.set_ylim(0.7, 10)
        ax.grid()
        f.tight_layout()

        return f

    @staticmethod
    def getLowScalePlot(slice: pd.DataFrame, exact: np.array, label:str):
        """

        :param slice:
        :param exact:
        :param label
        :return:
        """

        f = pylab.figure(figsize=(10, 6))
        ax = pylab.axes()

        for i, spins in enumerate(slice["n_spins"].unique()):
            slice_ = slice.query("n_spins == %d" % spins)
            ax.scatter(slice_["h"] / slice["JZ"],
                      -slice["meanEnergy"] / (slice["n_spins"] * slice["JZ"]),
                      label="N spins = %d (fitted)" % spins,
                      alpha=0.9, s=8, marker='o')

        ax.scatter(exact[:, 0], -exact[:, 1], marker='^', alpha=0.9, s=8,
                  label="Exact solution")
        ax.set_xlabel(r"$\frac{h}{J_z}$")
        ax.set_ylabel(r"$-\frac{E}{N\times{J_z}}$")
        ax.set_title(label)
        ax.legend()
        ax.set_xlim(-0.1, 2.5)
        ax.set_ylim(0.7, 3)
        ax.grid()
        f.tight_layout()

        return f