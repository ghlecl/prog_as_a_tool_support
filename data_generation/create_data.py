#! /usr/bin/env python
# -*- coding: utf-8 -*-

# 2016 - Ghyslain Leclerc (ghleclerc@gmail.com)

def read_file( file_name : str ):
   data = []
   with open( file_name, 'r' ) as f:
      f.readline() # first header line
      f.readline() # second header line
      for line in f:
         vals = line.strip().split()
         data.append( [ float( vals[0].strip() ), float( vals[1].strip() ) ] )
   return data


if __name__ == '__main__':
   from pprint import pprint
   from random import uniform
   from pathlib import Path
   
   answer = ''
   answer_valid = False
   print( '\n*** WARNING ***\n'
          'This will override the data used in the Microsoft Excel (TM) sheet.\n'
          'After regenerating the data, update the values in the spreadsheet '
          'to be able to \ncompare all techniques.\n' )
   while not answer_valid:
      answer = input( 'Must be run from data_generation folder.  Continue? (y/n)   ' )
      if answer == 'y' or answer == 'n':
         answer_valid = True
   
   if answer == 'n':
      exit()

   print( '' )

   # Path management before the loop, as this is constant
   orig_data_folder = Path.cwd() / "var_lengths"
   orig_files = list( orig_data_folder.glob( './*.pin' ) )
   orig_files = [ orig_data_folder.resolve() / cur_file for cur_file in orig_files ]
   new_files_folder = orig_data_folder.parents[1] / 'data'
   
   for cur_file in orig_files:
      # Read the field size to add noise only to the central 80%
      data = read_file( str( cur_file ) )
      f = cur_file.open( 'r' )
      fld_size_strg = f.readline()
      f.close()
      half_noise_range = 0.8 * float( fld_size_strg.strip().split()[0].strip() )

      # Generate shifted positions
      new_pos = []
      pos_offset = round( uniform( 0.06, 0.17 ), 2 )
      print( 'file : ', cur_file.name, '\t\tpos_offset : ', pos_offset )
      for pt in data:
         new_pos.append( pt[0] + pos_offset )

      # Add position noise in the center
      neg_offsetted_half_noise_range = -half_noise_range + pos_offset
      positive_offsetted_half_noise_range = half_noise_range + pos_offset
      # print( '  neg_offsetted_half_noise_range :' , neg_offsetted_half_noise_range )
      # print( '  positive_offsetted_half_noise_range :' , positive_offsetted_half_noise_range )
      # print( '  nb_of_pts :', len( new_pos ) )
      changed = 0
      for pos_idx in range( len( new_pos ) ):
         if ( neg_offsetted_half_noise_range > new_pos[pos_idx] or
              new_pos[pos_idx] > positive_offsetted_half_noise_range ):
            continue
         new_pos[pos_idx] = uniform( new_pos[pos_idx] - 0.015, new_pos[pos_idx] + 0.015 )
         changed += 1
      # print( '  changed_pts :', changed )
      print( '' )

      # Add dose noise in the center
      new_data = [ cur[1] for cur in data ]
      for pos_idx in range( len( new_pos ) ):
         if ( neg_offsetted_half_noise_range > new_pos[pos_idx] or
              new_pos[pos_idx] > positive_offsetted_half_noise_range ):
            continue
         new_data[pos_idx] = uniform( new_data[pos_idx] * 0.995, new_data[pos_idx] * 1.005 )
      
      new_pts = list( map( lambda x,y:[x,y], new_pos, new_data ) )
      
      new_file_name = new_files_folder / cur_file.name
      with new_file_name.open( 'w' ) as cur_f:
         with cur_file.open( 'r' ) as f:
            cur_f.write( f.readline() )
            cur_f.write( f.readline() )

         for cur_data in new_pts:
            cur_f.write( "{pos:.2f}\t{dose:.2f}\n".format( pos=cur_data[0], dose=cur_data[1]) )
