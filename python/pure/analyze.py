# -*- coding: utf-8 -*-

# 2016 - Ghyslain Leclerc (ghleclerc@gmail.com)

from lib import *

#===============================================================================
if __name__ == '__main__':
   from math import floor
   import sys
   import os.path

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
      data = read_file( cur_file )

      # estimate axis dose
      axis_dose_idx = data.index( min( data, key=lambda pt : abs( pt[0] ) ) )
      axis_dose = data[axis_dose_idx][1]
      
      
      # get position of each 50% and determine shift from 0 and apply
            # READABILITY NOTE : ad == short form of axis dose, for brivety
      half_ad = axis_dose / 2.0
      posi_50_ascend = x_val_from_y( data, half_ad )
      posi_50_descend = x_val_from_y( data, half_ad, From.end )
      width = posi_50_descend - posi_50_ascend

      shift = posi_50_descend - ( width / 2.0 )
      data = [ [ cur[0] - shift, cur[1] ] for cur in data ]
      

      # calculate new position array for symmetry calculation
      min_size_dim = floor( min( abs(data[0][0]), abs(data[len( data ) - 1][0]) ) * 10.0 ) / 10.0
      step = 0.1
      nb_of_steps = round( min_size_dim / step ) * 2 + 1
      new_pos = [ round( step * idx - min_size_dim, 1 ) for idx in range( nb_of_steps ) ]
      
      # interpolate dose for every new position
      new_doses = []
      for idx in range( 0, len( new_pos ) ):
         new_doses.append( round(
                     y_val_from_x( data, new_pos[idx] ), 3 )
         )
      new_data = list( map( lambda x,y : [x,y], new_pos, new_doses ) )

      # calculate symmetry
      low_80_percent_idx = lower_bound( new_data, -0.4 * width, predicate= lambda x, y : x[0] < y )
      center = floor( len( new_data ) / 2 )
      lt_half = new_data[low_80_percent_idx:center]
      rt_half = reversed( new_data[center + 1:len(new_data) - low_80_percent_idx] )

      diffs = [ abs( pair[0][1] - pair[1][1] ) for pair in zip( lt_half, rt_half ) ]
      symmetry = max( diffs ) / axis_dose * 100.0

      
      print( "(" + os.path.basename( cur_file ) + ")\tsymétrie: " +
                                          "{sym:.2f}".format( sym=symmetry ) )
      
