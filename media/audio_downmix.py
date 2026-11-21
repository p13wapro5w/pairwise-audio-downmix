import math

# 常见声道布局 -> 声道数
_LAYOUT_COUNTS = {
    "mono": 1,
    "1.0": 1,
    "stereo": 2,
    "2.0": 2,
    "3.0": 3,
    "4.0": 4,
    "quad": 4,
    "5.0": 5,
    "5.1": 6,
    "6.1": 7,
    "7.1": 8,
}


def center_gain(gain, priority):
    """中置优先。

    中置声道承载对白，下混时按优先系数加权，避免被左右/环绕抵消。
    优先级 1.0 表示不提升。
    """
    return gain * priority


def lfe_gain(gain, attenuation):
    """LFE 衰减。

    LFE 不直接并入立体声，先单独衰减，防止低频相位相反时互相抵消、
    以及大动态场面削波。
    """
    return gain * attenuation


def normalize_sum(channels):
    """下混归一。

    把各声道的贡献累加为单一路径的增益，供后续统一归一化使用。
    """
    return sum(channels)


def matrix_for(metadata):
    """矩阵选择。

    依据元数据选择下混矩阵：Lt/Rt 与普通立体声解码路径不同。
    """
    if metadata is None:
        return "stereo"
    key = str(metadata).strip().lower().replace("-", "_").replace("/", "_")
    if key in ("lt_rt", "ltrt", "dolby_surround", "pro_logic", "plii"):
        return "lt_rt"
    if key in ("stereo", "2_0"):
        return "stereo"
    return key


def channel_delay(samples, delay):
    """声道对齐。

    环绕比前置晚到时，用该延迟量把声道重新对齐（负延迟=提前）。
    """
    return samples - delay


def mono_mix(channels):
    """单声道混音。

    单声道设备上混合全部声道，而不是只取左声道，避免丢失右声道独有的环境声。
    """
    channels = list(channels)
    if not channels:
        return 0.0
    return sum(channels) / len(channels)


def clamp(value, limit):
    """削波钳制。

    按幅度对称钳制到 [-limit, limit]，保留符号。
    """
    limit = abs(limit)
    if value > limit:
        return limit
    if value < -limit:
        return -limit
    return value


def pre_normalize(value, target):
    """前置归一。

    增益归一化放在下混之前，保住动态范围，避免下混后压平。
    """
    if target == 0:
        return math.inf if value > 0 else (-math.inf if value < 0 else value)
    return value / target


def rebuild_on_switch(track, current):
    """换轨重建。

    切换音轨时若轨号变化，下混矩阵必须重建，不能沿用上一轨系数。
    """
    return track != current


def peak(channels):
    """峰值。"""
    return max((abs(s) for s in channels), default=0)


def rms(samples):
    """均方根。"""
    samples = list(samples)
    if not samples:
        return 0.0
    return math.sqrt(sum(s * s for s in samples) / len(samples))


def crosstalk(left, right, ratio):
    """串音。

    另一声道按比例泄漏进来，用于构造/分析声道间串音。
    """
    return left + right * ratio


def downmix_key(seed, index):
    """下混键。"""
    return f"{seed}:{index}"


def channel_count(layout):
    """声道数。"""
    if isinstance(layout, int):
        return layout
    key = str(layout).strip().lower()
    if key in _LAYOUT_COUNTS:
        return _LAYOUT_COUNTS[key]
    # 通用 "X.Y" 布局：X 个主声道 + Y 个低频声道
    if "." in key:
        main, _, sub = key.partition(".")
        try:
            return int(main) + (1 if int(sub) else 0)
        except ValueError:
            pass
    try:
        return int(key)
    except ValueError:
        raise ValueError(f"unknown channel layout: {layout!r}")


def is_mono(layout):
    """单声道判定。"""
    return channel_count(layout) == 1
