from python.src.Ising import Ising
from python.src.Report import generate_report, save_results
from python.src.ArgparserH import get_parser

if __name__ == '__main__':
    parser = get_parser()
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
    model = Ising(n_spins=args.spins, J=args.j_z, h=args.h_const)
    model.fit(args.output, args.n_iter)

    #generate_report(args.output + '.log')
    save_results(args.output + '.log',
                 params=[args.spins, args.j_z, args.h_const],
                 prefix="ising", outfile="IsingResults.csv")