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


random.seed(2711694897)
for i in trange(0, 1024):
    scale_root = random.choice(['C', 'D', 'E'])
    track = generate_track(
        name=str(i),
        seed=i,
        style=LoopyStyle1(),
        melody_rep_bars=1,
        scale_root=scale_root,
        preview=False,
        muted_parts=['lead', 'bass', 'sub']
    )
    track.save_audio(save_name=f'{i}', target_dir='../renders')
    track.save_json('../data')
    track.get_mel(st_bar=0, ed_bar=8, save_dir='../data')
    track.print_melody()