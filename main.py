import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=str, default='./inputs',
                        help='Path to the folder with input images.')
    parser.add_argument('--output', type=str, default='./output',
                        help='Path to the folder where dataset will be stored.')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    print('Settings are: ', args)

