"""
Creates function of an input, transmitted and reflected wave
for a wave psasing from one material into another, described
with variables x, y, k_1, k_2, and omega.

Constants B and C are solved for (unit wave, so no const. A)
using sympy to get them in terms of k_1 and k_2. This gives
the final function y_sym.

To plot the function, the function y_numpy, which supports
numpy arrays as an input, can be used. This is imported by
GUI.py to generate the plot.
"""
# pylint: disable=invalid-name, no-member

import sympy
from sympy import Eq


x, t, k_1, k_2, omega, B, C = sympy.symbols("x t k_1 k_2 omega B C")

## x < 0
y_1 = sympy.cos(k_1*x - omega*t) + C*sympy.cos(k_1*x + omega*t)

## x >= 0
y_2 = B*sympy.cos(k_2*x - omega*t)

answers = sympy.solve([Eq(y_1.subs({x:0}), y_2.subs({x:0})),
                       Eq(y_1.diff(x).subs({x:0}), y_2.diff(x).subs({x:0}))], [B, C])

y_sym = sympy.Piecewise((y_1.subs(answers), x<0), (y_2.subs(answers), x>=0))

y_numpy = sympy.lambdify([x, t, k_1, k_2, omega], y_sym, "numpy")
