import math
from typing import Dict, Union


def VRdmax(
    bw: float,
    d: float,
    fck: float,
    fyk: float,
    fywk: float,
    θ: float,
    αcw: float = 1.0,
    γc: float = 1.5,
    units: str = "N-mm-rad",
    include_intermediates: bool = False,
) -> Union[float, Dict[str, float]]:
    """Compute the maximum shear resistance V_Rd,max.

    The function computes the design shear resistance V_Rd,max. Inputs are expected in
    millimetres and N/mm² when `units` is 'N-mm-rad' (the default). If `units` is
    'kN-m-rad' then inputs are interpreted in kN/m units where appropriate and the
    returned `value` will be in kN.

    Args:
        bw: Smallest width of the cross-section in the tensile area [mm].
        d: Effective depth of the cross-section [mm].
        fck: Characteristic concrete strength [N/mm²].
        fyk: Characteristic yield strength of reinforcement [N/mm²].
        fywk: Characteristic yield strength of welded shear reinforcement [N/mm²].
        θ: Angle between the concrete compression strut and beam axis [rad].
        αcw: Coefficient accounting for the state of stress in the compression chord.
        γc: Partial safety factor for concrete (default 1.5).
        units: Unit system, one of 'N-mm-rad' (default) or 'kN-m-rad'.
        include_intermediates: If True, return a dict with intermediate values; otherwise return the numeric value.

    Returns:
        float or dict: If `include_intermediates` is False, returns the shear resistance
        as a float (units depend on the `units` argument). If True, returns a dict with
        keys 'value', 'z', 'fcd' and 'v1' containing intermediate values.

    Raises:
        ValueError: If an unsupported `units` string is provided.

    Notes:
        The expression used is:

        \\[
        V_{Rd,max} = \\frac{\\alpha_{cw} \\cdot b_w \\cdot z \\cdot \\nu_1 \\cdot f_{cd}}{\\cot\\theta + \\tan\\theta}
        \\]

    Example:
        >>> import numpy as np
        >>> VRdmax(250., 539., 20., 500., 500., np.pi/4)

    """
    if units not in ("N-mm-rad", "kN-m-rad"):
        raise ValueError(f"Unsupported units: {units!r}. Use 'N-mm-rad' or 'kN-m-rad'.")

    # Work in consistent base units (N-mm-rad) for intermediates
    bw_work = float(bw)
    d_work = float(d)
    fck_work = float(fck)
    fyk_work = float(fyk)
    fywk_work = float(fywk)

    if units == "kN-m-rad":
        # convert kN-m to N-mm where appropriate: 1 kN = 1000 N, 1 m = 1000 mm
        bw_work *= 1000.0
        d_work *= 1000.0
        fck_work *= 0.001
        fyk_work *= 0.001
        fywk_work *= 0.001

    z = 0.9 * d_work
    fcd = fck_work / γc

    if fywk_work < 0.8 * fyk_work:
        if fck_work <= 60:
            v1 = 0.6
        else:
            v1 = max(0.5, 0.9 - fck_work / 200.0)
    else:
        v1 = 0.6 * (1.0 - fck_work / 250.0)

    value = αcw * bw_work * z * v1 * fcd / (math.tan(θ) + 1.0 / math.tan(θ))

    if units == "kN-m-rad":
        # convert back to kN-m units for the returned value
        value *= 0.001

    intermediates = {"z": z, "fcd": fcd, "v1": v1, "value": value}

    if include_intermediates:
        return intermediates
    return intermediates["value"]