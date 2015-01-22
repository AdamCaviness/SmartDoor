import os
import sys
import json


def read_config():
    """ Reads your SmartDoor configuration from disk.
        :return: json configuration
    """

    executing_path = os.path.dirname(sys.argv[0])
    config_filename = os.path.join(executing_path, 'config.json')
    with open(config_filename) as conf:
        config = json.load(conf)
    return config

if __name__ == '__main__':
    # Being executed as a script
    read_config()