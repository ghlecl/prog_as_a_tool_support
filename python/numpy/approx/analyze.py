# -*- coding: utf-8 -*-

# 2016 - Ghyslain Leclerc (ghleclerc@gmail.com)

#===============================================================================
if __name__ == '__main__':
   #from math import floor
   import sys
   import os.path
   from math import floor
   import numpy as np

   # read data
   files = []
   if len( sys.argv ) == 1:
      print( 'You have to provide at least one file name to analyse.' )
   else:
      for cur_arg in sys.argv[1:]: # sys.argv[0] == program name, so must skip
         if os.path.exists( cur_arg ):
            files.append( cur_arg )
         else:
            print( 'Argument ' + cur_arg + ' is not a valid file or does not exist.  Will be ignored.' )

   for cur_file in files:
      # Read file content
      data = np.genfromtxt( cur_file, skip_header=2 )
      
      # Find approximate axis dose
      axis_idx = np.argmin( np.abs(data[:,0]) )
      axis_dose = data[axis_idx][1]
      
      # Find (and apply) position shift based on position of 50% doses
      half_axis_dose = axis_dose / 2.0
      posi_50_ascend = np.interp( half_axis_dose, data[:axis_idx,1], data[:axis_idx,0] )
      posi_50_descend = np.interp( half_axis_dose, data[:axis_idx:-1,1], data[:axis_idx:-1,0] )
      width = posi_50_descend - posi_50_ascend
      data[:,0] -= posi_50_descend - ( width / 2.0 )

      # Create new position arrays for the left and right halves of the profile
      min_dim = floor( min( abs(data[0][0]), abs(data[len( data ) - 1][0]) ) * 10.0 ) / 10.0
      sym_calc_limit = round( 0.80 * min_dim )
      step = 0.1
      nb_of_steps = round( sym_calc_limit / step )
      lt_half_pos = np.linspace( -step, -sym_calc_limit, nb_of_steps )
      rt_half_pos = np.linspace( step, sym_calc_limit, nb_of_steps )

      # Interpolate the doses and calculate the symmetry
      lt_half_doses = np.interp( lt_half_pos, data[:,0], data[:,1] )
      rt_half_doses = np.interp( rt_half_pos, data[:,0], data[:,1] )
      sym = np.max( np.abs( lt_half_doses - rt_half_doses ) )/axis_dose * 100.0 # stop above 80% to avoid shoulders
      
      # Output the results
      print( "(" + os.path.basename( cur_file ) + ")\tsymétrie: " +
                                          "{sym:.2f}".format( sym=sym ) )
