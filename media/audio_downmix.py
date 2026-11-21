import math

def center_gain(gain, priority):
    """中置优先。"""
    raise NotImplementedError("TODO: center_gain")

def lfe_gain(gain, attenuation):
    """LFE 衰减。"""
    raise NotImplementedError("TODO: lfe_gain")

def normalize_sum(channels):
    """下混归一。"""
    raise NotImplementedError("TODO: normalize_sum")

def matrix_for(metadata):
    """矩阵选择。"""
    raise NotImplementedError("TODO: matrix_for")

def channel_delay(samples, delay):
    """声道对齐。"""
    raise NotImplementedError("TODO: channel_delay")

def mono_mix(channels):
    """单声道混音。"""
    raise NotImplementedError("TODO: mono_mix")

def clamp(value, limit):
    """削波钳制。"""
    raise NotImplementedError("TODO: clamp")

def pre_normalize(value, target):
    """前置归一。"""
    raise NotImplementedError("TODO: pre_normalize")

def rebuild_on_switch(track, current):
    """换轨重建。"""
    raise NotImplementedError("TODO: rebuild_on_switch")

def peak(channels):
    """峰值。"""
    raise NotImplementedError("TODO: peak")

def rms(samples):
    """均方根。"""
    raise NotImplementedError("TODO: rms")

def crosstalk(left, right, ratio):
    """串音。"""
    raise NotImplementedError("TODO: crosstalk")

def downmix_key(seed, index):
    """下混键。"""
    raise NotImplementedError("TODO: downmix_key")

def channel_count(layout):
    """声道数。"""
    raise NotImplementedError("TODO: channel_count")

def is_mono(layout):
    """单声道判定。"""
    raise NotImplementedError("TODO: is_mono")
