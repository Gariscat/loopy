from loopy import LoopyTrack, LoopySampleCore, LoopyPatternCore, LoopySample, LoopyPattern, LoopyChannel, LoopyPreset
from loopy.effect import *
from loopy.utils import *
from loopy import SAMPLE_DIR
import os
from typing import List
from copy import deepcopy


class LoopyStyle():
    def __init__(self) -> None:
        pass

    def compose(self,
        melody_notes: List[List],
        chord_notes: List[List],
    ) -> LoopyTrack:
        pass