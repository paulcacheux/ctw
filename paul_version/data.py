class Data:
    def __init__(self, path):
        self.data = read_input(path)
        self.m = max(self.data) + 1


def read_input(path):
    res = []
    with open(path) as f:
        for line in f:
            for c in line:
                if c.isdigit():
                    res.append(int(c))
    return res
