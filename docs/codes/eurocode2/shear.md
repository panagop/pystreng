# Shear module

This page documents the public symbols in the `pystreng.codes.eurocodes.ec2.ch6.shear` module.

::: pystreng.codes.eurocodes.ec2.ch6.shear
    options:
      members: true
      show_root_full_path: true
      members_order: source

## Examples

Simple call returning the numeric design shear resistance::

  >>> from pystreng.codes.eurocodes.ec2.ch6.shear import VRdmax
  >>> VRdmax(250.0, 539.0, 20.0, 500.0, 500.0, 0.78539816339)

Get intermediate values and the computed result::

  >>> VRdmax(250.0, 539.0, 20.0, 500.0, 500.0, 0.78539816339, include_intermediates=True)

## Formula

The expression used is:

$$
V_{Rd,\max} = \frac{\alpha_{cw} \; b_w \; z \; \nu_1 \; f_{cd}}{\cot\theta + \tan\theta}
$$

