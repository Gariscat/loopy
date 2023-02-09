from loopy import LoopyTrack, LoopySampleCore, LoopyPatternCore, LoopySample, LoopyPattern, LoopyChannel, LoopyPreset
from loopy.effect import *
from loopy.utils import *
from loopy import SAMPLE_DIR
import os
from typing import List
from copy import deepcopy

### CHANNELS
DEFAULT_CHANNELS = dict()
DEFAULT_CHANNELS['drop_kick'] = LoopyChannel(
    name='drop_kick',
    effects=[LoopyBalance(db=-6.0)]
)
DEFAULT_CHANNELS['drop_clap']  = LoopyChannel(
    name='drop_clap',
    effects=[LoopyHighpass(freq=500), LoopyBalance(db=-21.0)]
)
DEFAULT_CHANNELS['drop_hat']  = LoopyChannel(
    name='drop_hat',
    effects=[LoopyHighpass(freq=1000), LoopyBalance(db=-21.0)]
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
    preview: bool = False,
    chord_sync: bool = False,
    scale_root: str = 'C',
    scale_type: str = 'maj',
    root_area: str = '4',
    decor_map: dict = None,
) -> LoopyTrack:

    if style == 'Tobu':
        lead_names = ['Dream', 'Stars', 'Blue', 'SweetDivine',]
        chord_names = ['Massive', 'Supersaws', 'Diamond', 'FarAway']
        bass_names = ['Home', 'Perfect']
        sub_names = ['SUBBASS']
        balance = {'lead': -7, 'chord': -14, 'bass': -3, 'sub': -3}
        reverb = {'wet': 0.5, 'dry': 0.4}
        if decor_map is None:
            decor_map = {
                6: [10],
                4: [11],
                5: [],
                1: [2],
            }
    elif style == 'Dubvision':
        lead_names = ['Follow', 'Forever', 'Stars', 'SweetDivine', 'Supersaw',]
        chord_names = ['Diamond', 'SummerNights', 'Social']
        bass_names = ['Home', 'Dark']
        sub_names = ['SUBBASS']
        balance = {'lead': -10, 'chord': -16, 'bass': -4, 'sub': -6}
        reverb = {'wet': 1.0, 'dry': 0.4}
        if decor_map is None:
            decor_map={
                4: [11],
                5: [9],
                6: [10],
                1: [2],
                2: [5],
                3: [8],
            }
    assert len(melody_line) == len(chord_line)
    melody_notes = note_seq_parser(melody_line)
    chord_notes, bass_notes = chord_seq_parser(
        chord_line,
        melody_line if chord_sync else None,
        scale_root=scale_root,
        scale_type=scale_type,
        root_area=root_area,
        
    )
    sub_notes = [(octave_shift(k, -1), _, __) for k, _, __ in bass_notes]
    
    track = LoopyTrack(name=name, bpm=bpm, length='00:15')

    
    """
    elif style == 'MatisseSadko':
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

    ld_core = LoopyPatternCore(num_bars=8)
    ch_core = LoopyPatternCore(num_bars=8)
    bs_core = LoopyPatternCore(num_bars=8)
    sb_core = LoopyPatternCore(num_bars=8)
    

    for i, lead_name in enumerate(lead_names):
        generator = LoopyPreset(
            source_path=find_preset(f'Ultrasonic-LD-{lead_name}.wav'),
            name=f'LEAD-{i}',
        )
        ld_core.add_notes(melody_notes, generator)

    for i, chord_name in enumerate(chord_names):
        generator = LoopyPreset(
            source_path=find_preset(f'Ultrasonic-PD-{chord_name}.wav'),
            name=f'CHORD-{i}',
        )
        ch_core.add_notes(chord_notes, generator)

    for i, bass_name in enumerate(bass_names):
        generator = LoopyPreset(
            source_path=find_preset(f'Ultrasonic-BS-{bass_name}.wav'),
            name=f'BASS-{i}',
        )
        bs_core.add_notes(bass_notes, generator)

    for i, sub_name in enumerate(sub_names):
        generator = LoopyPreset(
            source_path=find_preset(f'Ultrasonic-BS-{sub_name}.wav'),
            name=f'SUB-{i}',
        )
        sb_core.add_notes(sub_notes, generator)
    

    lead_channel = LoopyChannel(
        name='LEAD',
        effects=[
            LoopyHighpass(300),
            LoopyBalance(balance['lead']),
            LoopySidechain(attain=1/2, interp_order=2, mag=0.7),
            LoopyReverb(wet_level=reverb['wet'], dry_level=reverb['dry']),
        ]
    )

    chord_channel = LoopyChannel(
        name='CHORD',
        effects=[
            LoopyHighpass(200),
            LoopyBalance(balance['chord']),
            LoopySidechain(attain=1/2, interp_order=2, mag=0.9),
            LoopyReverb(wet_level=0.2),
        ]
    )

    bass_channel = LoopyChannel(
        name='BASS',
        effects=[
            LoopyHighpass(200),
            LoopyLowpass(5000),
            LoopyBalance(balance['bass']),
            LoopySidechain(attain=1/2, interp_order=2, mag=1),
        ]
    )

    sub_channel = LoopyChannel(
        name='SUB',
        effects=[
            LoopyHighpass(30),
            LoopyLowpass(100),
            LoopyBalance(balance['sub']),
            LoopySidechain(attain=1/2, interp_order=2, mag=1),
        ]
    )
    cores = (ld_core, ch_core, bs_core, sb_core)
    channels = (lead_channel, chord_channel, bass_channel, sub_channel)
    """
    track.add_pattern(ch_core, 0, 0, chord_channel)
    """
    for core, channel in zip(cores, channels):
        track.add_pattern(core, 0, 0, channel)
    
    add_kick(track=track, num_bars=8)
    add_clap(track=track, num_bars=8)
    add_hat(track=track, num_bars=8)

    if preview:
        preview_wave(track.render())

    return track