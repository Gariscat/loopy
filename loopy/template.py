from loopy import LoopyTrack, LoopySampleCore, LoopyPatternCore, LoopySample, LoopyPattern, LoopyChannel
from loopy.effect import *
from loopy.utils import DEFAULT_SR, parse_sig
from loopy import SAMPLE_DIR
import os

### CHANNELS

kick_channel = LoopyChannel(
    name='kick',
    effects=[LoopyBalance(mag=-6.0)]
)
clap_channel = LoopyChannel(
    name='clap',
    effects=[LoopyHighpass(freq=500), LoopyBalance(mag=-12.0)]
)
ambience_channel = LoopyChannel(
    name='ambience',
    effects=[LoopyHighpass(freq=500), LoopyBalance(mag=-18.0)]
)

### SAMPLES

def add_kick(
    track: LoopyTrack,
    num_bars: int = 16,
    source_path: str = 'OXO Progressive House Essential Drums\\OXO - Kick\\Progressive House Essential - Kick 02.wav',
    sig: str = '4/4',
    channel: LoopyChannel = kick_channel,
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
    source_path: str = 'OXO Progressive House Essential Drums\\OXO - Claps\\Progressive House Essential - Claps 06.wav',
    sig: str = '4/4',
    channel: LoopyChannel = clap_channel,
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
    
    
