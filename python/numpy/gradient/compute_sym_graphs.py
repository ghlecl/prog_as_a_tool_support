# -*- coding: utf-8 -*-

# 2016 - Louis Archambault (larchamb@gmail.com)

#===============================================================================
import numpy as np
import sys
import os.path

def smooth(x:'1D',wlength:int):
   """ A simple rolling average smoothing of x over a window of wlength elements """
   w=np.ones(wlength)
   xr = x.reshape((len(x),))
   sx = np.convolve(w/w.sum(),xr,mode='same') # output length will be the same as len(x)
   return sx
#-------------------------------------------------------------------------------

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
	x_ori = p[:,0].copy()
	grad = np.gradient(p[:,1]) # extremum of derivative should correspond to the 50% intensity
	mx = np.argmax(grad)
	mn = np.argmin(grad)
	offst = (p[mn,0] + p[mx,0])/2
	width = np.abs(p[mx,0] - p[mn,0])
	p[:,0] -= offst
	x_recntr = p[:,0].copy()
	p[:,1] *= (100/np.interp(0,p[:,0],p[:,1])) # norm by central axis
	y_ori = p[:,1].copy() # original but renormed
	p[:,1] = smooth(y_ori, 5)
	y_smooth = p[:,1].copy()
	nb_sample = 500
	smpl = np.linspace(0,0.8*width,nb_sample)
	d_r = np.interp(smpl,p[:,0],p[:,1])
	d_l = np.interp(-smpl,p[:,0],p[:,1])
	sym = np.max(np.abs(d_r - d_l))
	print( "(" + os.path.basename( cur_file ) + ")\tsymétrie: " +
													"{sym:.2f}".format( sym=sym ) )

	import pylab as plt

	plt.plot(x_ori,y_ori,label='Brut')
	plt.plot(x_recntr,y_ori,label='Recentré')
	plt.plot(x_recntr,y_smooth,label='Lissé')
	plt.xlabel('Position (cm)')
	plt.ylabel('Dose relative')
	xlim = width*1.5/2
	plt.xlim([-xlim,xlim])
	plt.legend(loc='lower center')
	plt.show()

