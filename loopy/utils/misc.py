


def hhmmss2sec(hhmmss: str):
    # https://stackoverflow.com/questions/6402812/how-to-convert-an-hmmss-time-string-to-seconds-in-python
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(hhmmss.split(':'))))