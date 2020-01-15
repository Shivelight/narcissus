import os


def get_resource_path(file, path):
    return os.path.join(os.path.dirname(file), path)
