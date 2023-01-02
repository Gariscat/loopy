from datetime import timedelta
from playsound import playsound
import soundfile as sf
import numpy as np

def sec2hhmmss(sec: float):
    return str(timedelta(seconds=sec))

def hhmmss2sec(hhmmss: str):
    # https://stackoverflow.com/questions/6402812/how-to-convert-an-hmmss-time-string-to-seconds-in-python
    return sum(float(x) * 60 ** i for i, x in enumerate(reversed(hhmmss.split(':'))))

def preview_wave(y: np.ndarray, sr: int):
    tmp_addr = 'tmp.wav'
    sf.write(tmp_addr, y, sr)
    try:
        playsound(tmp_addr)
    except:
        print('Could not play with PyThon... Please preview it in the folder.')

def parse_sig(sig: str = '4/4'):
    beats_per_bar, n = [int(x) for x in sig.split('/')]
    beat_value = 1 / n
    return beats_per_bar, beat_value

def beat2index(pos_in_pattern: float, bpm: int = 128, sr: int = 44100):
    return int(pos_in_pattern * 60 * sr / bpm)
