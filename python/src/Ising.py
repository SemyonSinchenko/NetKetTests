import netket as nk

class Ising(object):
    def __init__(self, n_spins, J, h):
        """
        Create the model.
        :param n_spins: the number of spins
        :param J: JZ in the model
        :param h: h in the model
        """

        self.n_spins = n_spins
        self.h = h
        self.j = J

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

        self.graph = nk.graph.Hypercube(length=self.n_spins, n_dim=1, pbc=True)

    def get_hilbert_space(self):
        """
        Create the Hilbert space for our model.
        Like in the original paper:
            * spins +-0.5
        :return: None
        """

        assert (self.graph != None), 'At first you need to define graph!'
        self.hilbert = nk.hilbert.Spin(graph=self.graph, s=1, total_sz=0)

    def get_hamiltonian(self):
        """
        Create the Ising hamiltonian operator
        :return: None
        """

        assert (self.hilbert != None), 'At first you need to define Hilbert space!'
        self.hamiltonian = nk.operator.Ising(hilbert=self.hilbert, h=self.h, J=self.j)

    def get_machine(self):
        """
        Create the RBM.
        Like in the original paper:
            * alpha = 4
        :return: None
        """

        assert (self.hilbert != None), 'At first you need to define Hilbert space!'
        if self.n_spins > 10:
            self.machine = nk.machine.RbmSpin(hilbert=self.hilbert, alpha=2)
        else:
            self.machine = nk.machine.RbmSpin(hilbert=self.hilbert, n_hidden=20)
        self.machine.init_random_parameters(sigma=0.01)

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
            n_replicas=8
        )

    def get_optimizer(self):
        """
        Create optimizer
        :return: None
        """

        self.opt = nk.optimizer.Momentum(learning_rate=0.0005, beta=0.9)

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
            n_samples=700,
            use_iterative=True
        )

        self.vc.run(output_prefix=output, n_iter=n_iter, save_params_every=10)

    def get_exact(self):
        """
        Get exact ground-state energy.
        :return: exact_energy
        """

        exact = nk.exact.lanczos_ed(self.hamiltonian, first_n=1, compute_eigenvectors=False)
        return exact.eigenvalues[0]

    def get_observable(self):
        """
        Get observable values of operator.
        :return:
        """
        return self.vc.get_observable_stats()
