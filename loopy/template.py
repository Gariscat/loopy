from loopy import LoopyTrack, LoopySampleCore, LoopyPatternCore, LoopySample, LoopyPattern, LoopyChannel
from loopy.utils import DEFAULT_SR, parse_sig
from loopy import SAMPLE_DIR
import os

def add_kick(
    track: LoopyTrack,
    num_bars: int = 16,
    source_path: str = 'OXO Progressive House Essential Drums\\OXO - Kick\\Progressive House Essential - Kick 02.wav',
    sig: str = '4/4',
    channel: LoopyChannel = None,
    blank_period: int = 8,
):
    beats_per_bar, _ = parse_sig(sig)
    core = LoopySampleCore(os.path.join(SAMPLE_DIR, source_path))
    for global_pos in range(num_bars):
        if (global_pos + 1) % blank_period == 0:  # blank convention every 8 bars
            continue
        for local_pos in range(beats_per_bar):
            track.add_sample(
                sample_type=core,
                global_pos=global_pos,
                local_pos=local_pos,
                channel=channel
            )
    
    
