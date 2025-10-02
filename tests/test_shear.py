import math
from pystreng.codes.eurocodes.ec2.ch6.shear import VRdmax


def test_vrdmax_returns_float():
    val = VRdmax(250.0, 539.0, 20.0, 500.0, 500.0, math.pi / 4)
    assert isinstance(val, float)


def test_vrdmax_intermediates():
    res = VRdmax(250.0, 539.0, 20.0, 500.0, 500.0, math.pi / 4, include_intermediates=True)
    assert isinstance(res, dict)
    for key in ("z", "fcd", "v1", "value"):
        assert key in res
        assert isinstance(res[key], float)
