from __future__ import absolute_import

from .differentiation import forward_difference, backward_difference, central_difference, \
    approximate_derivative_finite
from .integration import trapezoidal_rule, simpsons_rule, composite_simpsons_rule, \
    composite_trapezoidal
from .polynomial import horner_eval, lagrange_interpolate, neville, divided_differences
from .roots import newtonraph, bisection, secant