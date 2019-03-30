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
    parser.add_argument('--n_dims', '-d',
                        help='The number of dimensions',
                        required=False, nargs='?',
                        default=1, type=int)
    parser.add_argument('--j_z', '-j',
                        help='The J constant',
                        required=False, nargs='?',
                        default=1, type=float)
    parser.add_argument('--h_const',
                        help='The h constant',
                        required=False, nargs='?',
                        default=1, type=float)

    return parser