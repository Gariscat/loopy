


def hhmmss2sec(hhmmss: str):
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(hhmmss.split(':'))))