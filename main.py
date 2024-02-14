import argparse
from src.labeler import ImageLabeler
from src.walker import DefaultDirectoryWalker
from src.saver import DefaultSaver, TFIconSaver


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
    walker = DefaultDirectoryWalker(root=args.root, cache=False)
    saver = TFIconSaver(output=args.output)
    print('Paths are: ', walker.paths)
    labeler = ImageLabeler(saver=saver, directory_walker=walker)
    labeler.start()