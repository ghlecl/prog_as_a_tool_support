# -*- coding: utf-8 -*-

# 2016 - Ghyslain Leclerc (ghleclerc@gmail.com)

#-------------------------------------------------------------------------------
def lin_interpol( new_x, x1, x2, y1, y2 ):
   if abs( new_x - x1 ) < 0.0000001:
      return y1
   
   if abs( new_x - x2 ) < 0.0000001:
      return y2

   m = ( y2 - y1 ) / ( x2 - x1 )
   b = y1 - ( m * x1 )
   return ( new_x * m ) + b



#-------------------------------------------------------------------------------
def lower_bound( arr, val, first : int = 0, last : int = None, 
                                       predicate = None ):
   """Return index of first element for which predicate is false.

      The predicate is a function which takes an element of the array and the
      value to search for and returns whether the current element is in order.

      Default predicate is lambda x, y : x < y, which is an appropriate default
      if the array elements are of the same type as the value to search for.

      Default bounds are [ 0, len(arr) [.
   """
   if last is None: last = len(arr)
   
   if predicate is None: predicate = lambda x, y : x < y

   pos = first
   while pos != last:
      if not predicate( arr[pos], val ):
         break
      pos += 1

   if pos != last:
      return pos
   else:  # Last is outside the range, so not found (a.k.a. None)
      return None



#-------------------------------------------------------------------------------
def reverse_lower_bound( arr, val, first : int = None, last : int = -1, 
                                       predicate = None ):
   """Return index of first element for which predicate is false, starting from
      the end of the array.

      The predicate is a function which takes an element of the array and the
      value to search for and returns whether the current element is in order.

      Default predicate is lambda x, y : x < y, which is an appropriate default
      if the array elements are of the same type as the value to search for.
      
      Default bounds are [ len(arr)-1, -1 [.
   """
   if first is None: first = len(arr) - 1
   
   if predicate is None: predicate = lambda x, y : x < y

   pos = first
   while pos != last:
      if not predicate( arr[pos], val ):
         break
      pos -= 1

   if pos >= 0:
      return pos
   else:  # Last is outside the range, so not found (a.k.a. None)
      return None



#-------------------------------------------------------------------------------
def y_val_from_x_ascend( data, x_val ):
   idx = lower_bound( data, x_val, predicate= lambda x, y : x[0] < y )
   
   if idx == None: # Check for edge cases
      if abs( data[0][0] - x_val ) < 0.000001:
         idx = 1
      elif abs( data[len(data)-1][0] - x_val ) < 0.000001:
         idx = len(data) - 1
   
   return lin_interpol( x_val, data[ idx - 1 ][0], data[ idx ][0],
                                    data[ idx - 1 ][1], data[ idx ][1]  )

def y_val_from_x_descend( data, x_val ):
   idx = reverse_lower_bound( data, x_val, predicate= lambda x, y : x[0] < y )
   
   if idx == None: # Check for edge cases
      if abs( data[0][0] - x_val ) < 0.000001:
         idx = 0
      elif abs( data[len(data)-1][0] - x_val ) < 0.000001:
         idx = len(data) - 2

   return lin_interpol( x_val, data[ idx + 1 ][0], data[ idx ][0],
                                    data[ idx + 1 ][1], data[ idx ][1]  )


def x_val_from_y_ascend( data, y_val ):
   idx = lower_bound( data, y_val, predicate= lambda x, y : x[1] < y )
   
   if idx == None: # Check for edge cases
      if abs( data[0][1] - y_val ) < 0.000001:
         idx = 1
      elif abs( data[len(data) -1][1] - y_val ) < 0.000001:
         idx = len(data) - 1

   return lin_interpol( y_val, data[ idx - 1 ][1], data[ idx ][1],
                                    data[ idx - 1 ][0], data[ idx ][0]  )

def x_val_from_y_descend( data, y_val ):
   idx = reverse_lower_bound( data, y_val, predicate= lambda x, y : x[1] < y )
   
   if idx == None: # Check for edge cases
      if abs( data[0][1] - y_val ) < 0.000001:
         idx = 0
      elif abs( data[len(data) -1][1] - y_val ) < 0.000001:
         idx = len(data) - 2
   
   return lin_interpol( y_val, data[ idx + 1 ][1], data[ idx ][1],
                                    data[ idx + 1 ][0], data[ idx ][0]  )



#-------------------------------------------------------------------------------
from enum import Enum

class From( Enum ):
   front = 1
   end = 2

def x_val_from_y( data, y_val, ascend = From.front ):
   x = None
   if ascend == From.front:
      x = x_val_from_y_ascend( data, y_val )
   elif ascend == From.end:
      x = x_val_from_y_descend( data, y_val )
   else:
      raise TypeError( 'ascend parameter must be a From enum' )
   return x
 

def y_val_from_x( data, x_val, ascend : bool = From.front ):
   y = None
   if ascend == From.front:
      y = y_val_from_x_ascend( data, x_val )
   elif ascend == From.end:
      y = y_val_from_x_descend( data, x_val )
   return y


#-------------------------------------------------------------------------------
def read_file( file_name : str ):
   data = []
   with open( file_name, 'r' ) as f:
      f.readline() # first header line
      f.readline() # second header line
      for line in f:
         vals = line.strip().split()
         data.append( [ float( vals[0].strip() ), float( vals[1].strip() ) ] )
   return data
