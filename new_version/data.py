import json

class Data:
    def __init__(self, path):
        self.data = read_input(path)
        self.m = max(self.data) + 1


def read_input(path):
    """Utility function that reads a file and returns its json content.
    Args:
        path (string): the path of the file.
    Returns:
        The content of the file, parsed as json.
    """
    with open(path) as f:
        data = json.load(f)
        return data
    return []
