from loopy import LoopyTrack, LoopySampleCore, LoopyPatternCore, LoopySample, LoopyPattern, LoopyChannel
from loopy.effect import *
from loopy.utils import *
from loopy import SAMPLE_DIR
import os
from typing import List

### CHANNELS
DEFAULT_CHANNELS = dict()
DEFAULT_CHANNELS['drop_kick'] = LoopyChannel(
    name='drop_kick',
    effects=[LoopyBalance(db=-6.0)]
)
DEFAULT_CHANNELS['drop_clap']  = LoopyChannel(
    name='drop_clap',
    effects=[LoopyHighpass(freq=500), LoopyBalance(db=-20.0)]
)
DEFAULT_CHANNELS['drop_hat']  = LoopyChannel(
    name='drop_hat',
    effects=[LoopyHighpass(freq=1000), LoopyBalance(db=-24.0)]
)
DEFAULT_CHANNELS['drop_amb'] = LoopyChannel(
    name='drop_amb',
    effects=[LoopyHighpass(freq=500), LoopyBalance(db=-24.0)]
)

def add_kick(
    track: LoopyTrack,
    num_bars: int = 16,
    source_path: str = 'OXO Progressive House Essential Drums\\OXO - Kick\\Progressive House Essential - Kick 02.wav',
    sig: str = '4/4',
    channel: LoopyChannel = DEFAULT_CHANNELS['drop_kick'],
    blank_every: int = 8,
):
    beats_per_bar, _ = parse_sig(sig)
    core = LoopySampleCore(os.path.join(SAMPLE_DIR, source_path))
    for global_pos in range(num_bars):
        if (global_pos + 1) % blank_every == 0:  # blank convention every 8 bars
            continue
        for local_pos in range(beats_per_bar):
            track.add_sample(
                sample_type=core,
                global_pos=global_pos,
                local_pos=local_pos,
                channel=channel
            )


def add_clap(
    track: LoopyTrack,
    num_bars: int = 16,
    source_path: str = 'OXO Progressive House Essential Drums\\OXO - Claps\\Progressive House Essential - Drop Claps 02.wav',
    sig: str = '4/4',
    channel: LoopyChannel = DEFAULT_CHANNELS['drop_clap'],
    blank_every: int = 8,
):
    beats_per_bar, _ = parse_sig(sig)
    core = LoopySampleCore(os.path.join(SAMPLE_DIR, source_path), truncate=4)
    for global_pos in range(num_bars):
        if (global_pos + 1) % blank_every == 0:  # blank convention every 8 bars
            continue
        track.add_sample(
            sample_type=core,
            global_pos=global_pos,
            local_pos=0,
            channel=channel
        )
   
def add_hat(
    track: LoopyTrack,
    num_bars: int = 16,
    source_path: str = 'OXO Progressive House Essential Drums\\OXO - Cymbals\\Progressive House Essential - Hi-hat Loop 02.wav',
    sig: str = '4/4',
    channel: LoopyChannel = DEFAULT_CHANNELS['drop_hat'],
    blank_every: int = 8,
):
    beats_per_bar, _ = parse_sig(sig)
    core = LoopySampleCore(os.path.join(SAMPLE_DIR, source_path), truncate=4)
    for global_pos in range(num_bars):
        if (global_pos + 1) % blank_every == 0:  # blank convention every 8 bars
            continue
        track.add_sample(
            sample_type=core,
            global_pos=global_pos,
            local_pos=0,
            channel=channel
        )
### SAMPLES

def prog_house(
    melody_line: List[int],
    chord_line: List[int],
    style: str = 'Tobu',
    name: str = 'exp',
    bpm: int = 128,
) -> LoopyTrack:
    melody_notes = note_seq_parser(melody_line)
    chord_notes, bass_notes = chord_seq_parser(chord_line)
    track = LoopyTrack(name=name, bpm=bpm, length='00:15')

    if style == 'Tobu':
        lead_names = ['Forever', 'Stars', 'SweetDivine', 'Blue']
        chord_names = ['Massive', 'Supersaws']
        bass_names = ['Home', 'Perfect']
        sub_names = ['SUBBASS']
    """    
    elif style == 'MatisseSadko':
        lead_names = ['Forever', 'Stars', 'SweetDivine', 'Blue']
        chord_names = ['Massive', 'Supersaws']
        bass_names = ['Home', 'Perfect']
        sub_names = ['SUBBASS']
    elif style == 'Dubvision':
        lead_names = ['Forever', 'Stars', 'SweetDivine', 'Blue']
        chord_names = ['Massive', 'Supersaws']
        bass_names = ['Home', 'Perfect']
        sub_names = ['SUBBASS']
    elif style == 'MartinGarrix':
        lead_names = ['Forever', 'Stars', 'SweetDivine', 'Blue']
        chord_names = ['Massive', 'Supersaws']
        bass_names = ['Home', 'Perfect']
        sub_names = ['SUBBASS']
    """