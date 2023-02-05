from loopy import LoopyTrack, LoopySampleCore, LoopyPatternCore, LoopySample, LoopyPattern, LoopyChannel, LoopyPreset
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
) -> LoopyTrack:
    assert len(melody_line) == len(chord_line)
    melody_notes = note_seq_parser(melody_line)
    chord_notes, bass_notes = chord_seq_parser(chord_line, melody_line if chord_sync else None)
    sub_notes = [(octave_shift(k, -1), _, __) for k, _, __ in bass_notes]
    
    track = LoopyTrack(name=name, bpm=bpm, length='00:15')

    if style == 'Tobu':
        lead_names = ['Forever', 'Stars', 'Blue']
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
            LoopyHighpass(500),
            LoopyBalance(-9.0),
            LoopySidechain(attain=1/2, interp_order=2, mag=0.5),
            LoopyReverb(wet_level=0.5),
        ]
    )

    chord_channel = LoopyChannel(
        name='CHORD',
        effects=[
            LoopyHighpass(200),
            LoopyBalance(-15.0),
            LoopySidechain(attain=1/2, interp_order=2, mag=0.9),
        ]
    )

    bass_channel = LoopyChannel(
        name='BASS',
        effects=[
            LoopyHighpass(200),
            LoopyLowpass(5000),
            LoopyBalance(-6.0),
            LoopySidechain(attain=1/2, interp_order=2, mag=0.9),
        ]
    )

    sub_channel = LoopyChannel(
        name='SUB',
        effects=[
            LoopyHighpass(30),
            LoopyLowpass(100),
            LoopyBalance(-9.0),
            LoopySidechain(attain=1/2, interp_order=2, mag=1),
        ]
    )

    track.add_pattern(ld_core, 0, 0, lead_channel)
    track.add_pattern(ch_core, 0, 0, chord_channel)
    track.add_pattern(bs_core, 0, 0, bass_channel)
    track.add_pattern(sb_core, 0, 0, sub_channel)

    add_kick(track=track, num_bars=8)
    add_clap(track=track, num_bars=8)
    add_hat(track=track, num_bars=8)

    if preview:
        preview_wave(track.render())

    return track