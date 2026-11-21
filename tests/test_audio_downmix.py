import pytest
import math
from media import audio_downmix as mod

CASES = [
    ("center", 'm.center_gain(1, 1.5) == approx(1.5)'),
    ("lfe", 'm.lfe_gain(1, 0.5) == approx(0.5)'),
    ("norm", 'm.normalize_sum([1, 2, 3]) == 6'),
    ("matrix", 'm.matrix_for("lt_rt") == "lt_rt"'),
    ("delay", 'm.channel_delay(100, 2) == 98'),
    ("mono", 'm.mono_mix([1, 3]) == approx(2.0)'),
    ("clamp", 'm.clamp(2, 1) == 1'),
    ("pre", 'm.pre_normalize(10, 5) == approx(2.0)'),
    ("switch", 'm.rebuild_on_switch(2, 1) is True'),
    ("peak", 'm.peak([1, -3, 2]) == 3'),
    ("rms", 'm.rms([3, 4]) == approx(math.sqrt(12.5))'),
    ("cross", 'm.crosstalk(1, 2, 0.5) == approx(2.0)'),
    ("key", 'm.downmix_key(3, 2) == "3:2"'),
    ("count", 'm.channel_count("5.1") == 6'),
    ("mono_flag", 'm.is_mono("stereo") is False')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx, "math": math})
