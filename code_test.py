#!/usr/bin/env python3

#for testing sys eqn solving

import numpy
from sympy.solvers.solveset import linsolve
import sympy

Lm = 0.065

#declare sym vars
Fjy = sympy.Symbol('Fjy')
Fjx = sympy.Symbol('Fjx')
T0 = sympy.Symbol('T0')

angle = 90
delt_angle = 10
arm_wght = 1
arm_pos = 0.5
dumbb_wght = 5
dumbb_pos = 1
g = 9.8


eqn_y =  numpy.cos(numpy.deg2rad(angle - delt_angle)) * T0 - arm_wght * g - dumbb_wght * g - Fjy
eqn_x = Fjx - numpy.sin(numpy.deg2rad(angle - delt_angle)) * T0
eqn_m = numpy.sin(numpy.deg2rad(delt_angle)) * Lm * T0 - arm_wght * g * arm_pos * numpy.sin(numpy.deg2rad(angle)) - g * dumbb_wght * dumbb_pos * numpy.sin(numpy.deg2rad(angle))

print('complex')
print(eqn_y)
print(eqn_x)
print(eqn_m)
output = sympy.solve([eqn_y, eqn_x, eqn_m], (Fjx, Fjy, T0))
print(output)



eqn_y = numpy.sin(numpy.deg2rad(10)) * T0 - Fjy - arm_wght * g - dumbb_wght * g
eqn_x = - numpy.cos(10) * T0 + Fjx
eqn_m = - dumbb_wght * g * dumbb_pos - arm_wght * arm_pos * g * arm_wght + numpy.sin(numpy.deg2rad(10)) * Lm

output = sympy.solve([eqn_y, eqn_x, eqn_m], (Fjx, Fjy, T0))
print('simple')
print(output)





