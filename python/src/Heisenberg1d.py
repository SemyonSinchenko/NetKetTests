import netket as nk
import numpy as np
import matplotlib.pyplot as plt


class Heisenberg1d(object):
    def __init__(self, n_spins, J):
        """
        Create the model.
        :param n_spins: the number of spins
        :param J: coupling constant
        """

        self.n_spins = n_spins
        self.J = J

        self.get_graph()
        self.get_hilbert_space()
        self.get_hamiltonian()
        self.get_machine()
        self.get_sampler()
        self.get_optimizer()

    def get_graph(self):
        """
        Create the NetKet graph object.
        Like in the original paper:
            * 1d chain
            * 40 spins
        :return: None
        """

        self.graph = nk.graph.Hypercube(length=40, n_dim=1, pbc=True)

    def get_hilbert_space(self):
        """
        Create the Hilbert space for our model.
        Like in the original paper:
            * spins +-0.5
        :return: None
        """

        assert (self.graph != None), 'At first you need to define graph!'
        self.hilbert = nk.hilbert.Spin(graph=self.graph, s=0.5)

    def get_hamiltonian(self):
        """
        Create the Hesenberg1d hamiltonian operator
        :return: None
        """

        assert (self.hilbert != None), 'At first you need to define Hilbert space!'
        self.hamiltonian = nk.operator.Heisenberg(hilbert=self.hilbert)

    def get_machine(self):
        """
        Create the RBM.
        Like in the original paper:
            * alpha = 4
        :return: None
        """

        assert (self.hilbert != None), 'At first you need to define Hilbert space!'
        self.machine = nk.machine.RbmSpin(hilbert=self.hilbert, alpha=4)
        self.machine.init_random_parameters(seed=42, sigma=0.05)

    def get_sampler(self):
        """
        Create the MCMC sampler
        :return: None
        """

        assert (self.graph != None), 'At first you need to define graph!'
        assert (self.machine != None), 'At first you need to define machine!'

        self.sampler = nk.sampler.MetropolisExchangePt(
            machine=self.machine,
            graph=self.graph,
            d_max=1,
            n_replicas=12
        )

    def get_optimizer(self):
        """
        Create optimizer
        :return: None
        """

        self.opt = nk.optimizer.Momentum(learning_rate=1e-2, beta=0.9)

    def fit(self, output, n_iter):
        """
        Fit the model.
        :param output: output-file prefix
        :param n_iter: the number of iterations
        :return: None
        """

        self.vc = nk.variational.Vmc(
            hamiltonian=self.hamiltonian,
            sampler=self.sampler,
            optimizer=self.opt,
            n_samples=1000,
            use_iterative=True
        )

        self.vc.run(output_prefix=output, n_iter=1000, save_params_every=10)