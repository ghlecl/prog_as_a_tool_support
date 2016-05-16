# -*- coding: utf-8 -*-

# 2016 - Louis Archambault (larchamb@gmail.com)

import numpy as np
p = np.genfromtxt( "../data/Ph06ProfOuv10x10Longi_10.pin",skip_header=2)
grad = np.gradient(p[:,1]) # extremum of derivative should correspond to the 50% intensity
mx = np.argmax(grad)
mn = np.argmin(grad)
offst = (p[mn,0] + p[mx,0])/2
p[:,0] -= offst
p[:,1] *= (100/np.interp(0,p[:,0],p[:,1])) # norm by central axis
smpl_r = np.arange(0.2,10.2,0.2)
d_r = np.interp(smpl_r,p[:,0],p[:,1])
smpl_l = np.arange(-0.2,-10.2,-0.2)
d_l = np.interp(smpl_l,p[:,0],p[:,1])
sym = np.max(np.abs(d_r - d_l)[d_r >= 90.]) # stop above 80% to avoid shoulders
print(sym)
