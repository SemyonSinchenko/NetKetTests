from python.src.Heisenberg import Heisenberg
from python.src.Report import generate_report
from python.src.ArgparserH import get_parser

if __name__ == '__main__':
    parser = get_parser()
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
    model = Heisenberg(n_spins=args.spins, n_dims=args.n_dims)
    model.fit(args.output, args.n_iter)

    generate_report(args.output + '.log')