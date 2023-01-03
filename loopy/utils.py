from datetime import timedelta
from playsound import playsound
import soundfile as sf
import numpy as np

PIANO_KEYS = ['A1', 'A#1', 'B1', 'C2']
for i in range(2, 9):
    PIANO_KEYS += [
        f'C#{i}', f'D{i}', f'D#{i}', f'E{i}',
        f'F{i}', f'F#{i}', f'G{i}', f'G#{i}',
        f'A{i}', f'A#{i}', f'B{i}', f'C{i+1}'
    ]
assert(len(PIANO_KEYS) == 88)


def piano_id2piano_key(piano_id: int):
    # 1-88 to A1-C9
    return PIANO_KEYS[piano_id-1]

def piano_key2piano_id(piano_key: str):
    # A1-C9 to 1-88
    return PIANO_KEYS.index(piano_key) + 1

def piano_key2midi_id(piano_key: str):
    # A1-C9 to 21-108
    return PIANO_KEYS.index(piano_key) + 21

def midi_id2piano_key(midi_id: int):
    # 21-108 to A1-C9
    return PIANO_KEYS[midi_id-21]

def midi_id2piano_id(piano_id: int):
    # 21-108 to 1-88
    return piano_id - 20

def piano_id2midi_id(midi_id: int):
    # 1-88 to 21-108
    return midi_id + 20

def sec2hhmmss(sec: float):
    return str(timedelta(seconds=sec))

def hhmmss2sec(hhmmss: str):
    # https://stackoverflow.com/questions/6402812/how-to-convert-an-hmmss-time-string-to-seconds-in-python
    return sum(float(x) * 60 ** i for i, x in enumerate(reversed(hhmmss.split(':'))))

def preview_wave(y: np.ndarray, sr: int = 44100):
    """
    Preview a waveform.

    Args:
        y (np.ndarray): the waveform to be previewed
        sr (int, optional): sample rate. Defaults to 44100.
    """
    tmp_addr = 'tmp.wav'
    sf.write(tmp_addr, y, sr)
    try:
        playsound(tmp_addr)
    except:
        print('Could not play with PyThon... Please preview it in the folder.')

def parse_sig(sig: str = '4/4'):
    """
    Parse the time signature.

    Args:
        sig (str, optional): the time signature to be parsed. Defaults to '4/4'.

    Returns:
        beats_per_bar (int): number of beats per bar.
        beat_value (float): the length of a beat in terms of notes.
    """
    beats_per_bar, n = [int(x) for x in sig.split('/')]
    beat_value = 1 / n
    return beats_per_bar, beat_value

def beat2index(pos_in_pattern: float, bpm: int = 128, sr: int = 44100):
    """
    Convert the position in a pattern (unit: beat) to the sample index in the waveform.

    Args:
        pos_in_pattern (float): the position in a pattern in terms of beat.
        bpm (int, optional): beats per minutes. Defaults to 128.
        sr (int, optional): sample rate. Defaults to 44100.

    Returns:
        index (int): the sample index in the waveform.
    """
    return int(pos_in_pattern * 60 * sr / bpm)

def add_y(target_y: np.ndarray, source_y: np.ndarray, st_index: int):
    """
    Add the source waveform to the target waveform from the start index of the target.
    This function modifies the target waveform in-place.
    Args:
        target_y (np.ndarray): the target waveform.
        source_y (np.ndarray): the source waveform.
        st_index (int): the start index.
    """
    source_len = source_y.shape[0]
    ed_index = min(st_index + source_len, target_y.shape[0])
    # print(st_index, ed_index)
    target_y[st_index:ed_index, :] += source_y