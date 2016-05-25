# -*- coding: utf-8 -*-

# 2016 - Louis Archambault (larchamb@gmail.com)

#===============================================================================
import numpy as np
import sys
import os.path

# read data
files = []
for cur_arg in sys.argv[1:]:
	try:
		assert os.path.exists( cur_arg ), cur_arg
		files.append( cur_arg )
	except AssertionError as err:
		print('Argument ' + err.args[0] + ' is not a valid file or does not exist.  Will be ignored.')
assert len(files) > 0, 'No valid files provided'

for cur_file in files:
	p = np.genfromtxt( cur_file, skip_header=2 )
	grad = np.gradient(p[:,1]) # extremum of derivative should correspond to the 50% intensity
	mx = np.argmax(grad)
	mn = np.argmin(grad)
	offst = (p[mn,0] + p[mx,0])/2
	width = np.abs(p[mx,0] - p[mn,0])
	p[:,0] -= offst
	p[:,1] *= (100/np.interp(0,p[:,0],p[:,1])) # norm by central axis
	nb_sample = 1000
	smpl = np.linspace(0,0.8*width,nb_sample)
	d_r = np.interp(smpl,p[:,0],p[:,1])
	d_l = np.interp(-smpl,p[:,0],p[:,1])
	sym = np.max(np.abs(d_r - d_l))
	print( "(" + os.path.basename( cur_file ) + ")\tsymétrie: " +
													"{sym:.2f}".format( sym=sym ) )
