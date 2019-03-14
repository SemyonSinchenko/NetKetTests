import argparse


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o',
                        help='Output file prefix',
                        required=False, type=str,
                        nargs='?', default='test')
    parser.add_argument('--n_iter', '-i',
                        help='The number of iteration',
                        required=False, type=int,
                        nargs='?', default=1000)
    parser.add_argument('--spins', '-s',
                        help='The number of spins',
                        required=False, nargs='?',
                        default=40, type=int)
    parser.add_argument('--j-coupling', '-j',
                        help='Coupling constant of model',
                        required=False, type=float,
                        nargs='?', default=1.0)

    return parser