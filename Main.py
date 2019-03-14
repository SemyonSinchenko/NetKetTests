from python.src.Heisenberg1d import Heisenberg1d
from python.src.Argparser import get_parser

if __name__ == '__main__':
    parser = get_parser()
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
    model = Heisenberg1d(n_spins=40, J=1)
    model.fit(args.output, args.n_iter)