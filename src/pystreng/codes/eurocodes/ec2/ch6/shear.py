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
        ```python
        import math
        result = VRdmax(250., 539., 20., 500., 500., math.pi/4)
        print(result)  # 150000.0
        ```

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


def VRdc(
    CRdc: float,
    Asl: float,
    fck: float,
    σcp: float,
    bw: float,
    d: float,
    units: str = 'N-mm'
) -> Dict[str, float]:
    """Compute the design value for the shear resistance V_Rd,c.

    Units are 'N-mm', unless specified otherwise. Alternative options are: 'kN-m'

    Example:
        ```python
        vrdc = VRdc(CRdc=0.12,
                    Asl=308,
                    fck=20.,
                    σcp=0.66667,
                    bw=250.,
                    d=539.,
                    units='N-mm')
        ```

    Args:
        CRdc: 0.18/γc coefficient.
        Asl: Area of the tensile reinforcement [mm²].
        fck: Characteristic concrete strength [N/mm²].
        σcp: Concrete compressive stress σ_cp=N_Ed/A_c < 0.2f_cd [N/mm²].
        bw: Smallest width of the cross-section in the tensile area [mm].
        d: Effective depth of the cross-section [mm].
        units: Unit system, one of 'N-mm' (default) or 'kN-m'.

    Returns:
        Dictionary containing intermediate values and the final result in [N], 
        unless specified otherwise. Intermediate results are always 'N-mm'.

    Notes:
        The expressions used are:

        \\[
        V_{Rd,c} = \\max \\left\\{\\begin{matrix}
        [C_{Rd,c} \\cdot k \\cdot(100\\cdot \\rho_l\\cdot f_{ck})^{1/3} + k_1 \\cdot \\sigma_{cp}] \\cdot b_w \\cdot d \\\\
        (v_{min} + k_1 \\cdot \\sigma_{cp}) \\cdot b_w \\cdot d
        \\end{matrix}\\right.
        \\]

        where:

        - \\(k=1 + \\sqrt{\\frac{200}{d}} \\leq 2.0\\)
        - \\(\\rho_l=\\frac{A_{sl}}{b_w \\cdot d} \\leq 0.02\\)
        - \\(k_1 = 0.15\\)

    """
    _VRdc = {}

    if units == 'N-mm':
        pass
    elif units == 'kN-m':
        Asl = Asl * 10 ** 6
        fck *= 0.001
        σcp *= 0.001
        bw *= 1000
        d *= 1000
    else:
        pass

    ρl = min(Asl / (bw * d), 0.02)
    k = min(1 + (200.0 / d) ** 0.5, 2.0)
    vmin = 0.035 * k ** 1.5 * fck ** 0.5
    k1 = 0.15

    VRdc1 = (CRdc * k * math.pow((100 * ρl * fck), (1 / 3)) + k1 * σcp) * bw * d
    VRdc2 = (vmin + k1 * σcp) * bw * d

    _VRdc['ρl'] = ρl
    _VRdc['k'] = k
    _VRdc['vmin'] = vmin
    _VRdc['k1'] = k1
    _VRdc['VRdc1'] = VRdc1
    _VRdc['VRdc2'] = VRdc2
    _VRdc['value'] = max(VRdc1, VRdc2)

    if units == 'N-mm':
        pass
    elif units == 'kN-m':
        _VRdc['value'] *= 0.001
    else:
        pass

    return _VRdc