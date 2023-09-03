from loopy import LoopyTrack, LoopySampleCore, LoopyPatternCore, LoopySample, LoopyPattern, LoopyChannel, LoopyPreset
from loopy.pattern import preview_notes
from loopy.effect import *
from loopy.utils import *
from loopy.rhythm import LoopyRhythm, trivial_accomp
from copy import deepcopy
import os
from typing import List, Tuple
import random
import matplotlib.pyplot as plt

class LoopyStyleBase():
    def __init__(self) -> None:
        self.sound_sheet = {
            'lead': [],
            'chord': [],
            'bass': [],
            'sub': [],
            'kick': [],
            'top': [],  # claps, hats, etc.
            'fx': [],
        }
        self.inst_channel_sheet = {
            'lead': [],
            'chord': [],
            'bass': [],
            'sub': [],
        }
        self._artist_name = None
        self._song_name = None


def compose(
    style: LoopyStyleBase,
    name: str,
    lead_notes: List[Tuple],
    chord_notes: List[Tuple],
    bass_notes: List[Tuple],
    sub_notes: List[Tuple],
    bpm: int = 128,
    sig: str = '4/4',
    length: str = '00:15',
    preview: bool = False,
    muted_parts: List[str] = None,
) -> LoopyTrack:
    track = LoopyTrack(name=name, bpm=bpm, sig=sig, length=length)
    """"""
    beats_per_bar, beat_value = parse_sig(sig)
    num_beats = hhmmss2sec(length) * bpm / 60
    num_bars = int(num_beats / beats_per_bar)

    def add_kick(track: LoopyTrack, style_info: Dict, ):
        core = LoopySampleCore(style_info['source_path'])
        channel = LoopyChannel(
            name=style_info['source_path'],
            effects=[LoopyBalance(style_info['gain'])]
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

    def add_top(track: LoopyTrack, style_info: Dict, ):
        core = LoopySampleCore(style_info['source_path'], truncate=4)  # 4 beats as a whole
        channel = LoopyChannel(
            name=style_info['source_path'],
            effects=[LoopyHighpass(style_info['highpass']), LoopyBalance(style_info['gain'])]
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

    def add_fx(track: LoopyTrack, style_info: Dict, ):
        if style_info['type'] == 'main-fill':
            channel = LoopyChannel(
                name='main-fill',
                effects=[LoopyHighpass(style_info['highpass']), LoopyBalance(style_info['gain'])]
            )
            for i in range(0, num_bars, style_info['every']):
                source_name = random.choice(os.listdir(style_info['dir']))
                source_path = os.path.join(style_info['dir'], source_name)
                core = LoopySampleCore(source_path, truncate=beats_per_bar)  # 4 beats as a whole
                track.add_sample(
                    sample_type=core,
                    global_pos=i+style_info['every']-1,
                    local_pos=0,
                    channel=channel
                )

        elif style_info['type'] == 'sub-fill':
            channel = LoopyChannel(
                name='sub-fill',
                effects=[
                    LoopyHighpass(style_info['highpass']),
                    LoopyBalance(style_info['gain']),
                    LoopyReverb(dry_level=style_info['dry'], wet_level=style_info['dry'])
                ]
            )
            f = lambda n:n&-n  # find the largest power of 2 that divides global_pos
            for global_pos in range(num_bars):
                _ = global_pos + 1
                if _ % f(_) == 0 and random.uniform(0, 1) > style_info['intensity'] * f(_):
                    continue
                source_name = random.choice(os.listdir(style_info['dir']))
                source_path = os.path.join(style_info['dir'], source_name)
                core = LoopySampleCore(source_path, truncate=beats_per_bar)  # 4 beats as a whole
                track.add_sample(
                    sample_type=core,
                    global_pos=global_pos,
                    local_pos=0,
                    channel=channel
                )

        elif style_info['type'] == 'downlifter':
            channel = LoopyChannel(
                name='downlifter',
                effects=[LoopyHighpass(style_info['highpass']), LoopyBalance(style_info['gain'])]
            )
            source_names = random.sample(os.listdir(style_info['dir']), style_info['num'])
            for i in range(0, num_bars, style_info['every']):
                for source_name in source_names:
                    source_path = os.path.join(style_info['dir'], source_name)
                    core = LoopySampleCore(source_path, truncate=beats_per_bar*style_info['every'])  # 4 beats as a whole
                    track.add_sample(
                        sample_type=core,
                        global_pos=i,
                        local_pos=0,
                        channel=channel
                    )
                
        elif style_info['type'] == 'loop':
            if style_info.get('part') != 'B':  # only add additional loops to part B of the drop
                return
            # print('here')
            channel = LoopyChannel(
                name='loop',
                effects=[LoopyHighpass(style_info['highpass']), LoopyBalance(style_info['gain'])]
            )
            source_names = random.sample(os.listdir(style_info['dir']), style_info['num'])
            for i in range(num_bars):
                for source_name in source_names:
                    source_path = os.path.join(style_info['dir'], source_name)
                    core = LoopySampleCore(source_path, truncate=beats_per_bar)  # 4 beats as a whole
                    track.add_sample(
                        sample_type=core,
                        global_pos=i,
                        local_pos=0,
                        channel=channel
                    )

    """"""
    for style_info in style.sound_sheet['kick']:
        if 'kick' in muted_parts:
            continue
        add_kick(track, style_info)
    for style_info in style.sound_sheet['top']:
        if 'top' in muted_parts:
            continue
        add_top(track, style_info)
    for style_info in style.sound_sheet['fx']:
        if 'fx' in muted_parts:
            continue
        add_fx(track, style_info)

    cores = {}
    cores['lead'] = LoopyPatternCore(num_bars)
    cores['chord'] = LoopyPatternCore(num_bars)
    cores['bass'] = LoopyPatternCore(num_bars)
    cores['sub'] = LoopyPatternCore(num_bars)


    for i, info in enumerate(style.sound_sheet['lead']):
        if info.get('mute'):
            continue
        generator = LoopyPreset(
            source_path=info['source_path'],
            name=info['name'] if info.get('name') else f'LEAD-{i}',
            balance_db=info['gain']
        )
        delta = info.get('octave_shift')
        notes = deepcopy(lead_notes)
        if delta is not None:
            notes = [(octave_shift(x, delta), y, z) for x, y, z in notes]
        cores['lead'].add_notes(notes, generator)

    for i, info in enumerate(style.sound_sheet['chord']):
        if info.get('mute'):
            continue
        generator = LoopyPreset(
            source_path=info['source_path'],
            name=info['name'] if info.get('name') else f'CHORD-{i}',
            balance_db=info['gain']
        )
        delta = info.get('octave_shift')
        notes = deepcopy(chord_notes)
        if delta is not None:
            notes = [(octave_shift(x, delta), y, z) for x, y, z in notes]
        cores['chord'].add_notes(notes, generator)

    for i, info in enumerate(style.sound_sheet['bass']):
        if info.get('mute'):
            continue
        generator = LoopyPreset(
            source_path=info['source_path'],
            name=info['name'] if info.get('name') else f'BASS-{i}',
            balance_db=info['gain']
        )
        delta = info.get('octave_shift')
        notes = deepcopy(bass_notes)
        if delta is not None:
            notes = [(octave_shift(x, delta), y, z) for x, y, z in notes]
        ### print(notes)
        ### print(info['source_path'], set([x for x,y,z in notes]))
        ### preview_notes(set([x for x,y,z in notes]), preset_name=info['source_path'])
        cores['bass'].add_notes(notes, generator)

    for i, info in enumerate(style.sound_sheet['sub']):
        if info.get('mute'):
            continue
        generator = LoopyPreset(
            source_path=info['source_path'],
            name=info['name'] if info.get('name') else f'SUB-{i}',
            balance_db=info['gain']
        )
        delta = info.get('octave_shift')
        notes = deepcopy(sub_notes)
        if delta is not None:
            notes = [(octave_shift(x, delta), y, z) for x, y, z in notes]
        cores['sub'].add_notes(notes, generator)
        """print(notes)
        preview_wave(cores['sub'].render())
        exit()"""

    channels = dict()
    for part in ('lead', 'chord', 'bass', 'sub'):
        if part in muted_parts:
            continue
        channels[part] = LoopyChannel(name=part.upper())
        for effect_info in style.inst_channel_sheet[part]:
            channels[part].add_effect(dict2fx(effect_info))
        track.add_pattern(cores[part], 0, 0, channels[part])
    
    if preview:
        preview_wave(track.render())

    return track


class LoopyStyle0(LoopyStyleBase):
    def __init__(self, intensity: float=0.5, part: str='B') -> None:
        super().__init__()
        self._artist_name = ('Martin Garrix', 'Sentinel')
        self._song_name = 'Hurricane'
        self.config = {
            'intensity': intensity,
            'part': part
        }
        self.stylize()

    def stylize(self):
        """----------------Instrument----------------"""
        """--------lead--------"""
        self.sound_sheet['lead'].append({
            'source_path': 'Heroes-LD07.wav',
            'gain': -9,
            'name': 'main',
            'mute': 0,
        })
        self.sound_sheet['lead'].append({
            'source_path': 'Heroes-LD06.wav',
            'gain': -15,
            'octave_shift': 0,
            'mute': 0,
        })
        self.sound_sheet['lead'].append({
            'source_path': 'Heroes-LD13.wav',
            'gain': -22,
            'octave_shift': 1,
            'mute': 0,
        })
        """--------chord--------"""
        self.sound_sheet['chord'].append({
            'source_path': 'Heroes-CH01.wav',
            'gain': -18,
        })
        self.sound_sheet['chord'].append({
            'source_path': 'Heroes-CH02.wav',
            'gain': -18,
        })
        self.sound_sheet['chord'].append({
            'source_path': 'Heroes-CH10.wav',
            'gain': -12,
        })
        """--------bass--------"""
        self.sound_sheet['bass'].append({
            'source_path': 'Heroes-BS08.wav',
            'gain': -18,
        })
        self.sound_sheet['bass'].append({
            'source_path': 'Heroes-BS10.wav',
            'gain': -21,
        })
        """--------sub--------"""
        self.sound_sheet['sub'].append({
            'source_path': 'Heroes-SB02.wav',
            'gain': -5.5,
            'octave_shift': -2
        })

        """----------------Drum&FX----------------"""
        """--------kick--------"""
        self.sound_sheet['kick'].append({
            'source_path': '(Martin Garrix)Ultrasonic - Sample Pack\\Ultrasonic - Kicks\\Ultrasonic - Kick 02.wav',
            'gain': -10,
            'blank_every': 8,
        })
        self.sound_sheet['kick'].append({
            'source_path': 'Splice Sounds - Sounds of KSHMR Vol.3\\KSHMR_Drums\\KSHMR_Kicks\\KSHMR_Top_Kicks\\KSHMR_Top_Kick_03.wav',
            'gain': -21,
            'blank_every': 8,
        })
        """--------top--------"""
        self.sound_sheet['top'].append({
            'source_path': 'OXO Progressive House Essential Drums\\OXO - Claps\\Progressive House Essential - Drop Claps 09.wav',
            'gain': -18,
            'blank_every': 8,
            'highpass': 500
        })
        self.sound_sheet['top'].append({
            'source_path': 'OXO Progressive House Essential Drums\\OXO - Cymbals\\Progressive House Essential - Hi-hat Loop 05.wav',
            'gain': -12,
            'blank_every': 8,
            'highpass': 500
        })
        """--------fx--------"""
        # put fills, transitions, etc. here
        self.sound_sheet['fx'].append({
            'type': 'main-fill',
            'dir': os.path.join(SAMPLE_DIR, 'main-fill'),
            'highpass': 250,
            'gain': -12,
            'every': 8,
        })
        self.sound_sheet['fx'].append({
            'type': 'sub-fill',
            'dir': os.path.join(SAMPLE_DIR, 'sub-fill'),
            'highpass': 500,
            'gain': -18,
            'dry': 0.7,
            'wet': 0.5,
            'intensity': self.config['intensity']
        })
        self.sound_sheet['fx'].append({
            'type': 'downlifter',
            'dir': os.path.join(SAMPLE_DIR, 'downlifter'),
            'highpass': 500,
            'gain': -21,
            'every': 4,
            'num': 3,
        })
        """self.sound_sheet['fx'].append({
            'type': 'loop',
            'part': self.config['part'],
            'dir': os.path.join(SAMPLE_DIR, 'loop'),
            'highpass': 500,
            'gain': -27,
            'num': 3,
        })"""
        """----------------Channel----------------"""
        """--------lead--------"""
        self.inst_channel_sheet['lead'] += [
            {'type': 'highpass', 'freq': 300},
            {'type': 'sidechain', 'attain': 0.3, 'interp_order': 1, 'mag': 0.4},
            {'type': 'reverb', 'dry_level': 0.75, 'wet_level': 0.8},
            {'type': 'delay', 'delay_seconds': 0.3, 'feedback': 0.5, 'mix': 0.15},
            {'type': "compressor", 'thres': -9, 'ratio': 18, 'attack': 0},
            {'type': 'balance', 'gain': 1.5},
            # {'type': 'limiter', 'thres': -6.0},
        ]
        self.inst_channel_sheet['chord'] += [
            {'type': 'highpass', 'freq': 280},
            {'type': 'lowpass', 'freq': 10000},
            {'type': 'compressor', 'thres': -15, 'ratio': 20, 'attack': 0},
            {'type': 'balance', 'gain': -3.0},
            {'type': 'sidechain', 'attain': 0.3, 'interp_order': 1, 'mag': 0.6},
        ]
        self.inst_channel_sheet['bass'] += [
            {'type': 'highpass', 'freq': 100},
            {'type': 'lowpass', 'freq': 5000},
            # {'type': 'balance', 'gain': 8.3},
            {'type': 'sidechain', 'attain': 0.3, 'interp_order': 1, 'mag': 0.8},
        ]
        self.inst_channel_sheet['sub'] += [
            {'type': 'highpass', 'freq': 35},
            {'type': 'lowpass', 'freq': 120},
            # {'type': 'compressor', 'thres': -11.3, 'ratio': 29, 'attack': 0, 'release': 200},
            # {'type': 'balance', 'gain': 4.5},
            {'type': 'sidechain', 'attain': 0.5, 'interp_order': 16, 'mag': 0.75},
        ]


class LoopyStyle1(LoopyStyleBase):
    def __init__(self, intensity: float=0.5, part: str='A') -> None:
        super().__init__()
        self._artist_name = ('Alesso')
        self._song_name = 'If I Lose Myself'
        self.config = {
            'intensity': intensity,
            'part': part
        }
        self.stylize()

    def stylize(self):
        """----------------Instrument----------------"""
        """--------lead--------"""
        self.sound_sheet['lead'].append({
            'source_path': 'Ultrasonic-LD-Dream.wav',
            'gain': -10.7,
            'octave_shift': 1,
            'mute': 0,
        })
        self.sound_sheet['lead'].append({
            'source_path': 'Ultrasonic-LD-Blue.wav',
            'gain': -11.3,
            'octave_shift': 1,
            'mute': 0,
        })
        self.sound_sheet['lead'].append({
            'source_path': 'Ultrasonic-LD-Forever.wav',
            'gain': -10.9,
            'name': 'main',
            'mute': 0,
        })
        self.sound_sheet['lead'].append({
            'source_path': 'Ultrasonic-LD-Forever.wav',
            'gain': -21.1,
            'octave_shift': 1,
            'mute': 0,
        })
        self.sound_sheet['lead'].append({
            'source_path': 'Ultrasonic-LD-Follow.wav',
            'gain': -20.1,
            'octave_shift': 0,
            'mute': 0,
        })
        self.sound_sheet['lead'].append({
            'source_path': 'Ultrasonic-LD-Follow.wav',
            'gain': -22.1,
            'octave_shift': 1,
            'mute': 0,
        })
        self.sound_sheet['lead'].append({
            'source_path': 'Ultrasonic-LD-SweetDivine.wav',
            'gain': -32.4,
            'octave_shift': 1,
            'mute': 0,
        })
        """--------chord--------"""
        self.sound_sheet['chord'].append({
            'source_path': 'Ultrasonic-PD-MG.wav',
            'gain': -15.8,
        })
        self.sound_sheet['chord'].append({
            'source_path': 'Ultrasonic-PD-Lonely.wav',
            'gain': -15.2,
        })
        self.sound_sheet['chord'].append({
            'source_path': 'Ultrasonic-PD-LoveMe.wav',
            'gain': -16.7,
        })
        """--------bass--------"""
        self.sound_sheet['bass'].append({
            'source_path': 'Ultrasonic-BS-Phone.wav',
            'gain': -13.3,
        })
        self.sound_sheet['bass'].append({
            'source_path': 'Ultrasonic-BS-Home.wav',
            'gain': -19.0,
        })
        """--------sub--------"""
        self.sound_sheet['sub'].append({
            'source_path': 'Ultrasonic-BS-SUBBASS.wav',
            'gain': -5.2,
        })

        """----------------Drum&FX----------------"""
        """--------kick--------"""
        self.sound_sheet['kick'].append({
            'source_path': '(Martin Garrix)Ultrasonic - Sample Pack\\Ultrasonic - Kicks\\Ultrasonic - Kick 02.wav',
            'gain': -9.8,
            'blank_every': 8,
        })
        self.sound_sheet['kick'].append({
            'source_path': 'Splice Sounds - Sounds of KSHMR Vol.3\\KSHMR_Drums\\KSHMR_Kicks\\KSHMR_Top_Kicks\\KSHMR_Top_Kick_03.wav',
            'gain': -21.1,
            'blank_every': 8,
        })
        """--------top--------"""
        self.sound_sheet['top'].append({
            'source_path': 'OXO Progressive House Essential Drums\\OXO - Claps\\Progressive House Essential - Drop Claps 09.wav',
            'gain': -32.3,
            'blank_every': 8,
            'highpass': 500
        })
        self.sound_sheet['top'].append({
            'source_path': 'OXO Progressive House Essential Drums\\OXO - Cymbals\\Progressive House Essential - Hi-hat Loop 04.wav',
            'gain': -28.4,
            'blank_every': 8,
            'highpass': 500
        })
        """--------fx--------"""
        # put fills, transitions, etc. here
        self.sound_sheet['fx'].append({
            'type': 'main-fill',
            'dir': os.path.join(SAMPLE_DIR, 'main-fill'),
            'highpass': 250,
            'gain': -12,
            'every': 8,
        })
        self.sound_sheet['fx'].append({
            'type': 'sub-fill',
            'dir': os.path.join(SAMPLE_DIR, 'sub-fill'),
            'highpass': 500,
            'gain': -16,
            'intensity': self.config['intensity']
        })
        self.sound_sheet['fx'].append({
            'type': 'downlifter',
            'dir': os.path.join(SAMPLE_DIR, 'downlifter'),
            'highpass': 500,
            'gain': -26,
            'every': 4,
            'num': 3,
        })
        """self.sound_sheet['fx'].append({
            'type': 'loop',
            'part': self.config['part'],
            'dir': os.path.join(SAMPLE_DIR, 'loop'),
            'highpass': 500,
            'gain': -27,
            'num': 3,
        })"""
        """----------------Channel----------------"""
        """--------lead--------"""
        self.inst_channel_sheet['lead'] += [
            {'type': 'highpass', 'freq': 300},
            {'type': 'sidechain', 'attain': 0.5, 'interp_order': 3, 'mag': 0.66},
            {'type': 'reverb', 'dry_level': 0.75, 'wet_level': 1},
            {'type': 'balance', 'gain': 2.0},
            {'type': 'limiter', 'thres': -6.0},
        ]
        self.inst_channel_sheet['chord'] += [
            {'type': 'highpass', 'freq': 250},
            {'type': 'lowpass', 'freq': 5000},
            {'type': 'compressor', 'thres': -15, 'ratio': 26, 'attack': 0, 'release': 200},
            {'type': 'balance', 'gain': -2.0},
            {'type': 'sidechain', 'attain': 0.5, 'interp_order': 3, 'mag': 0.75},
        ]
        self.inst_channel_sheet['bass'] += [
            {'type': 'highpass', 'freq': 100},
            {'type': 'lowpass', 'freq': 250},
            {'type': 'balance', 'gain': 8.3},
            {'type': 'sidechain', 'attain': 0.5, 'interp_order': 6, 'mag': 0.8},
        ]
        self.inst_channel_sheet['sub'] += [
            {'type': 'highpass', 'freq': 35},
            {'type': 'lowpass', 'freq': 100},
            {'type': 'compressor', 'thres': -11.3, 'ratio': 29, 'attack': 0, 'release': 200},
            {'type': 'balance', 'gain': 4.5},
            {'type': 'sidechain', 'attain': 0.5, 'interp_order': 9, 'mag': 1},
        ]

class LoopyStyle2(LoopyStyleBase):
    def __init__(self) -> None:
        super().__init__()
        self._artist_name = ('Tobu')
        self._song_name = 'Life'
        self.stylize()

    def stylize(self):
        pass


"""Generation begins!"""
def generate_track(
    name: str,
    style: LoopyStyleBase,
    bpm: int = 128,
    sig: str = '4/4',
    melody_rep_bars: int = 1,
    melody_root_area: str = '4',
    seed: int = 0,
    chord_prog: List[List] = None,
    scale_root: str = 'C',
    scale_type: str = 'maj',
    chord_root_area: str = '3',  # C3, D3, E3......
    del_second: bool = False,
    decr_octave: bool = True,
    incr_octave: bool = False,
    decor_map: Dict[int, List[int]] = dict(),
    chord_sync: bool = False,
    preview: bool = False,
    muted_parts: List[str] = None,
):
    np.random.seed(seed)
    random.seed(seed)
    if muted_parts is None:
        muted_parts = list()
    if chord_prog is None:
        chord_prog = random.choice(COMMON_CHORD_PROG)
    rhythm = LoopyRhythm(seed, rep_bars=melody_rep_bars)
    rhythm.generate_rhythm(mode='poisson', param={'lambda': 0.5})
    place_holders = rhythm.repeat(tot_bars=8)
    lead_notes = rhythm.trivial_melody_from_rhythm(
        place_holders=place_holders,
        seed=seed,
        scale_root=scale_root,
        scale_type=scale_type,
        root_area=melody_root_area,
    )
    chord_notes, bass_notes, sub_notes = trivial_accomp(
        sig=sig,
        place_holders=place_holders if chord_sync else [],
        chord_prog=chord_prog,
        scale_root=scale_root,
        scale_type=scale_type,
        root_area=chord_root_area,
        del_second=del_second,
        decr_octave=decr_octave,
        incr_octave=incr_octave,
        decor_map=decor_map,
    )

    """"""
    track = compose(
        style=style,
        name=name,
        lead_notes=lead_notes,
        chord_notes=chord_notes,
        bass_notes=bass_notes,
        sub_notes=sub_notes,
        bpm=bpm,
        sig=sig,
        length='00:15',
        preview=preview,
        muted_parts=muted_parts
    )

    return track
