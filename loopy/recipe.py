from loopy import LoopyTrack, LoopySampleCore, LoopyPatternCore, LoopySample, LoopyPattern, LoopyChannel, LoopyPreset
from loopy.effect import *
from loopy.utils import *
from loopy import SAMPLE_DIR
import os
from typing import List, Tuple
from copy import deepcopy


class LoopyStyle():
    def __init__(self) -> None:
        self._sound_sheet = {
            'lead': [],
            'chord': [],
            'bass': [],
            'sub': [],
            'kick': [],
            'top': [],  # claps, hats, etc.
            'fx': [],
        }
        self._inst_channel_sheet = {
            'lead': [],
            'chord': [],
            'bass': [],
            'sub': [],
        }
        self._artist_name = None
        self._song_name = None

    def compose(self,
        name: str,
        lead_notes: List[Tuple],
        chord_notes: List[Tuple],
        bass_notes: List[Tuple],
        sub_notes: List[Tuple],
        bpm: int = 128,
        sig: str = '4/4',
        length: str = '00:15',
        preview: bool = False,
    ) -> LoopyTrack:
        track = LoopyTrack(name=name, bpm=bpm, sig=sig, length=length)

        beats_per_bar, beat_value = parse_sig(sig)
        num_beats = hhmmss2sec(length) * bpm / 60
        num_bars = int(num_beats / beats_per_bar)

        def add_kick(track: LoopyTrack, style_info: Dict,):
            core = LoopySampleCore(os.path.join(SAMPLE_DIR, style_info['source_path']))
            channel = LoopyChannel(
                name=style_info['source_path'],
                effects=[LoopyBalance(style_info['balance'])]
            )
            for global_pos in range(num_bars):
                if (global_pos + 1) % style_info['blank_every'] == 0:  # blank convention every 8 bars
                    continue
                for local_pos in range(beats_per_bar):
                    track.add_sample(
                        sample_type=core,
                        global_pos=global_pos,
                        local_pos=local_pos,
                        channel=channel
                    )

        def add_top(track: LoopyTrack, style_info: Dict,):
            core = LoopySampleCore(os.path.join(SAMPLE_DIR, style_info['source_path']), truncate=4)  # 4 beats as a whole
            channel = LoopyChannel(
                name=style_info['source_path'],
                effects=[LoopyHighpass(style_info['highpass']), LoopyBalance(style_info['balance'])]
            )
            for global_pos in range(num_bars):
                if (global_pos + 1) % style_info['blank_every'] == 0:  # blank convention every 8 bars
                    continue
                track.add_sample(
                    sample_type=core,
                    global_pos=global_pos,
                    local_pos=0,
                    channel=channel
                )

        def add_fx(track: LoopyTrack, style_info: Dict,):
            core = LoopySampleCore(os.path.join(SAMPLE_DIR, style_info['source_path']), truncate=4)
            channel = LoopyChannel(
                name=style_info['source_path'],
                effects=[
                    LoopyLowpass(style_info['lowpass']),
                    LoopyHighpass(style_info['highpass']),
                    LoopyBalance(style_info['balance'])
                ]
            )
            track.add_sample(
                sample_type=core,
                global_pos=style_info['global_pos'],
                local_pos=style_info['local_pos'],
                channel=channel
            )

        for style_info in self._sound_sheet['kick']:
            add_kick(track, style_info)
        for style_info in self._sound_sheet['top']:
            add_top(track, style_info)
        for style_info in self._sound_sheet['fx']:
            add_fx(track, style_info)

        cores = {}
        cores['lead'] = LoopyPatternCore(num_bars)
        cores['chord'] = LoopyPatternCore(num_bars)
        cores['bass'] = LoopyPatternCore(num_bars)
        cores['sub'] = LoopyPatternCore(num_bars)
        
        for i, info in enumerate(self._sound_sheet['lead']):
            generator = LoopyPreset(
                source_path=info['source_path'],
                name=info['name'] if info.get('name') else f'LEAD-{i}',
                balance_db=info['pre_balance']
            )
            delta = info.get('octave_shift')
            if delta != 0:
                lead_notes = [(octave_shift(x, delta), y, z) for x, y, z in lead_notes]
            cores['lead'].add_notes(lead_notes, generator)

        for i, info in enumerate(self._sound_sheet['chord']):
            generator = LoopyPreset(
                source_path=info['source_path'],
                name=info['name'] if info.get('name') else f'CHORD-{i}',
                balance_db=info['pre_balance']
            )
            cores['chord'].add_notes(chord_notes, generator)

        for i, info in enumerate(self._sound_sheet['bass']):
            generator = LoopyPreset(
                source_path=info['source_path'],
                name=info['name'] if info.get('name') else f'BASS-{i}',
                balance_db=info['pre_balance']
            )
            delta = info.get('octave_shift')
            if delta != 0:
                bass_notes = [(octave_shift(x, delta), y, z) for x, y, z in bass_notes]
            cores['bass'].add_notes(bass_notes, generator)

        for i, info in enumerate(self._sound_sheet['sub_bass']):
            generator = LoopyPreset(
                source_path=info['source_path'],
                name=info['name'] if info.get('name') else f'SUB-{i}',
                balance_db=info['pre_balance']
            )
            cores['sub'].add_notes(sub_notes, generator)

        channels = {}
        for part in ('lead', 'chord', 'bass', 'sub'):
            channels[part] = LoopyChannel(name=part.upper())
            for effect_info in self._inst_channel_sheet[part]:
                channels[part].add_effect(dict2fx(effect_info))

            track.add_pattern(cores[part], 0, 0, channels[part])
        
        if preview:
            preview_wave(track.render())

        return track




class LoopyStyle1(LoopyStyle):
    def __init__(self) -> None:
        super().__init__()
        self._artist_name = ('Martin Garrix', 'Justin Mylo')
        self._song_name = 'Find You'
        self.stylize()

    def stylize(self):
        pass


class LoopyStyle2(LoopyStyle):
    def __init__(self) -> None:
        super().__init__()
        self._artist_name = ('Tobu')
        self._song_name = 'Life'
        self.stylize()

    def stylize(self):
        pass