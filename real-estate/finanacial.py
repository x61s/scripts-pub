#!/bin/python3

import numpy_financial as npf

dr = 0.01
values = [-80000, 5000, 5000, 5000, 80000]
npv = npf.npv(dr, values)
print('NPV:', npv)

irr = npf.irr(values)
print('IRR:', irr)
