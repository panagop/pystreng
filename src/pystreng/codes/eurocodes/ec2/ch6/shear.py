import math
from dataclasses import dataclass
from typing import Dict, Union

@dataclass(frozen=True)
class VRdmaxResult:
    # Inputs
    bw: float
    d: float
    fck: float
    fyk: float
    fywk: float
    θ: float
    αcw: float
    γc: float
    units: str
    # Outputs
    value: float
    z: float
    fcd: float
    v1: float
    tanθ: float
    cotθ: float

    def to_latex(self, show_inputs: bool = True, with_steps: bool = True, decimals: int = 3) -> str:
        """Return a LaTeX string for V_Rd,max formula and results."""
        def q(x: float) -> str:
            return f"{x:.{decimals}f}"
        V_unit = "N" if self.units == "N-mm-rad" else "kN"
        L_unit = "mm" if self.units == "N-mm-rad" else "m"
        f_unit = "N/mm^2"

        inputs = (
            "$$" +
            rf"\begin{{array}}{{l l}}"
            rf"b_w = {q(self.bw)}~\mathrm{{{L_unit}}} & d = {q(self.d)}~\mathrm{{{L_unit}}} \\ "
            rf"f_{{ck}} = {q(self.fck)}~\mathrm{{{f_unit}}} & f_{{yk}} = {q(self.fyk)}~\mathrm{{{f_unit}}} \\ "
            rf"f_{{ywk}} = {q(self.fywk)}~\mathrm{{{f_unit}}} & \theta = {q(self.θ)}~\mathrm{{rad}} \\ "
            rf"\alpha_{{cw}} = {q(self.αcw)} & \gamma_c = {q(self.γc)}"
            r"\end{array}$$" 
        ) if show_inputs else ""

        
        # Optional intermediate values
        inter = (
            "$$" +
            rf"\begin{{array}}{{l l}}"
            rf"z = {q(self.z)}~\mathrm{{{L_unit}}} & "
            rf"f_{{cd}} = {q(self.fcd)}~\mathrm{{{f_unit}}} \\ "
            rf"\nu_1 = {q(self.v1)} & "
            rf"\tan\theta = {q(self.tanθ)},~\cot\theta = {q(self.cotθ)}"
            r"\end{array}$$" 
        ) if with_steps else ""

        # Core expression
        expr = (
            r"\begin{align}"
            r"V_{Rd,\max} &= \frac{\alpha_{cw} \cdot b_w \cdot z \cdot \nu_1 \cdot f_{cd}}{\cot\theta + \tan\theta}\\[3pt]"
            rf"&= {q(self.value)}~\text{{{V_unit}}}"
            r"\end{align}"
        )
        return "\n".join([x for x in [inputs, inter, expr] if x])


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
) -> float | VRdmaxResult:
    """Compute the maximum shear resistance V_Rd,max according to Eurocode 2.

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
        raise ValueError("units must be 'N-mm-rad' or 'kN-m-rad'")

    # Normalize units
    sL = 1000.0 if units == "kN-m-rad" else 1.0
    sF = 0.001 if units == "kN-m-rad" else 1.0
    bw_, d_ = bw * sL, d * sL
    fck_, fyk_, fywk_ = fck * sF, fyk * sF, fywk * sF

    # Core calculations
    z = 0.9 * d_
    fcd = fck_ / γc
    v1 = (0.6 if fywk_ < 0.8 * fyk_ else 0.6 * (1 - fck_ / 250.0))
    tanθ, cotθ = math.tan(θ), 1 / math.tan(θ)
    value = αcw * bw_ * z * v1 * fcd / (tanθ + cotθ)
    if units == "kN-m-rad":
        value *= 0.001

    res = VRdmaxResult(bw, d, fck, fyk, fywk, θ, αcw, γc, units, value, z, fcd, v1, tanθ, cotθ)
    return res if include_intermediates else res.value


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