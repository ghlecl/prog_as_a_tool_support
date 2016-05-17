# -*- coding: utf-8 -*-

# 2016 - Louis Archambault (larchamb@gmail.com)

#===============================================================================
if __name__ == '__main__':
   from math import floor
   import sys
   import os.path

   # read data
   files = []
   if len( sys.argv ) == 1:
      print( 'You have to provide at least one file name to analyse' )
   else:
      for cur_arg in sys.argv[1:]: # sys.argv[0] == program name, so must skip
         if os.path.exists( cur_arg ):
            files.append( cur_arg )
         else:
            print( 'Argument ' + cur_arg + ' is not a file or does not exist.  Will be ignored.' )

   for cur_file in files:
      import numpy as np
      p = np.genfromtxt( cur_file, skip_header=2 )
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
      print( "" )
      print( "(" + os.path.basename( cur_file ) + ")\tsymétrie: " +
                                          "{sym:.2f}".format( sym=sym ) )
