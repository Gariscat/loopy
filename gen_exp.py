import matplotlib.pyplot as plt
import numpy as np
from loopy import LoopyTrack, LoopyPreset, LoopyPatternCore, PRESET_DIR, DEFAULT_SR, preview_notes, LoopySidechain, LoopyBalance
from loopy.utils import *
from loopy.rhythm import LoopyRhythm
import os
import librosa
from loopy.recipe import *
from tqdm import trange
import random

SCALE_ROOTS = ['B', 'C', 'C#', 'D', 'D#', 'E']
SEED = 431
random.seed(SEED)
for i in trange(0, 1):
    scale_root = random.choice(SCALE_ROOTS)
    track = generate_track(
        name=str(i),
        seed=i,
        style=LoopyStyle0(),
        melody_rep_bars=2,
        scale_root=scale_root,
        preview=False,
        muted_parts=['chord', 'bass', 'lead']
    )
    track.save_audio(save_name=f'{i}', target_dir='C:\\Users\\CA7AX\\LooPy\\renders')
    track.save_json('C:\\Users\\CA7AX\\LooPy\\data')
    track.get_mel(st_bar=0, ed_bar=8, save_dir='C:\\Users\\CA7AX\\LooPy\\data')
    track.print_melody()