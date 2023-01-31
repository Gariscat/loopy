from datetime import timedelta
from playsound import playsound
import soundfile as sf
import numpy as np
from typing import List, Tuple, Dict

DEFAULT_SR = 44100
# https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies
PIANO_KEYS = ['A0', 'A#0', 'B0', 'C0']
for i in range(1, 8):
    PIANO_KEYS += [
        f'C#{i}', f'D{i}', f'D#{i}', f'E{i}',
        f'F{i}', f'F#{i}', f'G{i}', f'G#{i}',
        f'A{i}', f'A#{i}', f'B{i}', f'C{i+1}'
    ]
assert(len(PIANO_KEYS) == 88)
# https://music.stackexchange.com/questions/23146/why-do-major-keys-contain-minor-chords
SCALE2CHORD_TYPES = {
    'maj': ['maj', 'min', 'min', 'maj', 'maj', 'min', 'dim',],
    'min': ['min', 'dim', 'maj', 'min', 'min', 'maj', 'maj',]
}
CHORD2POS = {
    'maj': (0, 4, 7),
    'min': (0, 3, 7),
    'dim': (0, 3, 6),
    'aug': (0, 4, 8),
}
SCALE2STEPS = {
    'maj': (0, 2, 4, 5, 7, 9, 11),
    'min': (0, 2, 3, 5, 7, 8, 10)
}

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

def preview_wave(y: np.ndarray, sr: int = DEFAULT_SR):
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

def beat2index(pos_in_pattern: float, bpm: int = 128, sr: int = DEFAULT_SR):
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
    target_y[st_index:ed_index, :] += source_y[:ed_index-st_index, :]


def get_chord_notes(
    chord_id: int,  # 1, 2, 3, 4, 5, 6, 7
    scale_root: str = 'C',
    scale_type: str = 'maj',
    root_area: str = '4',  # C3, D3, E3......
    del_second: bool = False,
    decr_octave: bool = True,
    incr_octave: bool = False,
    decor_notes: List[int] = [],
):
    assert chord_id in tuple(range(1, 8))
    chord_type = SCALE2CHORD_TYPES[scale_type][chord_id-1]
    delta = piano_key2midi_id(scale_root+root_area) + SCALE2STEPS[scale_type][chord_id-1]
    midi_indices = (np.array(CHORD2POS[chord_type]) + delta).tolist()
    if del_second:
        midi_indices.pop(1)
    if decr_octave:
        midi_indices.insert(0, midi_indices[0]-12)
    if incr_octave:
        midi_indices.insert(-1, midi_indices[0]+12)
    for decor_note in decor_notes:
        midi_indices.append(midi_indices[0]+decor_note)
        """if decor_note == '7':
            midi_indices.append(midi_indices[0]+10)
        elif decor_note == '4':
            midi_indices.append(midi_indices[0]+5)
        elif decor_note == '2':
            midi_indices.append(midi_indices[0]+2)
        """
    midi_indices.sort()
    ### print(midi_indices)
    notes = [midi_id2piano_key(id) for id in midi_indices]
    return notes


def note_seq_parser(
    note_seq: List[int],
    sig: str = '4/4',
    resolution: float = 1/16,
    max_value: float = 1/2,
    input_id_type: str = 'midi',
    rest_id: int = 0,
) -> List[Tuple[str, float, float]]:
    """
    Parse a sequence of integers into a sequence of notes.
    Assume the sequence starts in the beginning of a pattern.

    Args:
        note_seq (List[int]): the sequence of integers.
        sig (str, optional): signature. Defaults to '4/4'.
        resolution (float, optional): length of the shortest note (one integer). Defaults to 1/16.
        max_value (float, optional): maximum value of parsed note. Defaults to 1/2.
        input_id_type (str, optional): meaning of input integers (midi or piano). Defaults to 'midi'.
        rest_id (int, optional): the integer for rests. Defaults to 0.

    Returns:
        List[Tuple[str, float, float]]: a list of notes
    """
    _, beat_value = parse_sig(sig)

    assert input_id_type in ('midi', 'piano')
    convert_func = midi_id2piano_key if input_id_type == 'midi' else piano_id2piano_key
    
    score = []
    i, j, n = 0, 0, len(note_seq)
    while i < n:
        while j < n and note_seq[i] == note_seq[j] and j-i < max_value / resolution:
            j += 1
        if note_seq[i] == rest_id:
            i, j = i+1, i+1
            continue
        note_value = resolution * (j - i)
        pos_in_pattern = resolution * i / beat_value
        key_name = convert_func(note_seq[i])
        score += [(key_name, note_value, pos_in_pattern)]
        ### print(key_name, note_value.as_integer_ratio(), pos_in_pattern)
        i = j
    return score


def chord_seq_parser(
    chord_seq: List[int],
    note_seq: List[int] = None,
    sig: str = '4/4',
    resolution: float = 1/16,
    max_value: float = 1/2,
    rest_id: int = 0,
    scale_root: str = 'C',
    scale_type: str = 'maj',
    root_area: str = '4',  # C3, D3, E3......
    del_second: bool = False,
    decr_octave: bool = True,
    incr_octave: bool = False,
    decor_map: Dict[int, List[int]] = dict(),
) -> List[Tuple[str, float, float]]:
    """
    Parse a sequence of integers into a sequence of chords, conditioning on a melody.
    Assume the sequence starts in the beginning of a pattern.

    Args:
        chord_seq (List[int]): the sequence of integers for chords.
        note_seq (List[int], optional): the sequence of integers for melody.
        sig (str, optional): signature. Defaults to '4/4'.
        resolution (float, optional): length of the shortest note (one integer). Defaults to 1/16.
        max_value (float, optional): maximum value of parsed note. Defaults to 1/2.
        rest_id (int, optional): the integer for rests. Defaults to 0.
        decor_map (Dict[int, List[int]], optional): the mapping from chord index to the recipe of decoration notes. Defaults to None.
    Returns:
        List[Tuple[str, float, float]]: a list of chord notes
    """
    _, beat_value = parse_sig(sig)
    if note_seq is None:
        note_seq = [-1] * len(chord_seq)
    score = []
    i, j, n = 0, 0, len(chord_seq)
    while i < n:
        while j < n and chord_seq[i] == chord_seq[j] and j-i < max_value / resolution and note_seq[j] != rest_id:
            j += 1
        if note_seq[i] == rest_id:
            i, j = i+1, i+1
            continue
        print(i, j, chord_seq[i:j])
        note_value = resolution * (j - i)
        pos_in_pattern = resolution * i / beat_value
        decor_notes = decor_map[chord_seq[i]] if chord_seq[i] in decor_map.keys() else []
        key_names = get_chord_notes(
            chord_id=chord_seq[i],
            scale_root=scale_root,
            scale_type=scale_type,
            root_area=root_area,
            del_second=del_second,
            decr_octave=decr_octave,
            incr_octave=incr_octave,
            decor_notes=decor_notes,
        )
        for key_name in key_names:
            score += [(key_name, note_value, pos_in_pattern)]
        # key_name = convert_func(chord_seq[i])
        # score += [(key_name, note_value, pos_in_pattern)]
        ### print(key_name, note_value.as_integer_ratio(), pos_in_pattern)
        i = j
    return score


def pos2index(
    global_pos: int,
    local_pos: float,
    sr: int = DEFAULT_SR,
    sig: str = '4/4',
    bpm: int = 128,
):
    beats_per_bar, _ = parse_sig(sig)
    return int((global_pos * beats_per_bar + local_pos) * 60 * sr / bpm)
