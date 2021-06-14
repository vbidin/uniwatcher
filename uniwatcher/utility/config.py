import collections
import yaml

from argparse import ArgumentParser


def parse_configuration():
    parser = ArgumentParser(description='Starts the Uniwatcher application.')
    parser.add_argument('-p',
                        '--path',
                        required=True,
                        help='path to the configuration file')
    path = parser.parse_args().path
    with open(path, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return convert_dict_to_tuple(data)


def convert_dict_to_tuple(data):
    for key, value in data.items():
        if isinstance(value, dict):
            data[key] = convert_dict_to_tuple(value)
    config = collections.namedtuple('Configuration', data)
    return config(**data)
