#include <array>
#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <cmath> // std::abs
#include <algorithm>
#include <stdexcept>


// typedefs for convenience
using DataPt = std::array<double, 2>;
using Dist = std::vector< DataPt >;

// enum for the option to search from one end of the dist or the other
enum class From
{
   FRONT,
   END
};

//------------------------------------------------------------------------------
std::ostream& operator<<( std::ostream& stream, DataPt const& data_pt )
{
   return stream << data_pt[0] << "\t" << data_pt[1];
}



//------------------------------------------------------------------------------
Dist read_file( std::string file_name )
{
   std::ifstream the_file( file_name.c_str() );

   if( !the_file.is_open() )
   {
      return Dist();
   }

   Dist cur_dist;
   cur_dist.reserve( 1000 );

   
   std::string dummy{};
   std::getline( the_file, dummy ); // header line 1
   std::getline( the_file, dummy ); // header line 2

   DataPt pt_reader;
   while( !the_file.eof() )
   {
      the_file >> pt_reader[0] >> pt_reader[1];
      cur_dist.push_back( pt_reader );
   }

   the_file.close();

   return cur_dist;
}



//------------------------------------------------------------------------------
double lin_interpol( double new_x, double x1, double x2, double y1, double y2 )
{
   if( std::abs( new_x - x1 ) < 0.0000001 ) { return y1; }
   
   if( std::abs( new_x - x2 ) < 0.0000001 ) { return y2; }

   auto m = ( y2 - y1 ) / ( x2 - x1 );
   auto b = y1 - ( m * x1 );
   return ( new_x * m ) + b;
}



//------------------------------------------------------------------------------
double lin_interpol( double new_x, DataPt const& p1, DataPt const& p2 )
{
   return lin_interpol( new_x, p1[0], p2[0], p1[1], p2[1] );
}



//------------------------------------------------------------------------------
DataPt pt_at_x_val( Dist const& dist, double position )
{
   using std::begin;
   using std::end;

   auto search_val = DataPt{ position, 0.0 };
   auto pos = std::lower_bound( begin( dist ), end( dist ), search_val,
                       []( DataPt const& lt, DataPt const& rt )
                       { return lt[0] < rt[0]; }
              );

   if( pos == end( dist ) )
   {
      throw std::runtime_error( "value not in distribution" );
   }

   if( pos == begin( dist ) )
   {
      if( std::abs( (*pos)[0] - position ) < 0.000001 ) { pos = begin( dist ) + 1; }
   }
   return DataPt{ position, lin_interpol( position, *(pos - 1), *pos ) };
}




//------------------------------------------------------------------------------
DataPt pt_at_y_val_frwrd( Dist const& dist, double value )
{
   using std::begin;
   using std::end;

   auto search_val = DataPt{ 0.0, value };
   auto pos = std::lower_bound( begin( dist ), end( dist ), search_val,
                       []( DataPt const& lt, DataPt const& rt )
                       { return lt[1] < rt[1]; }
              );

   if( pos == end( dist ) )
   {
      throw std::runtime_error( "value not in distribution" );
   }

   if( pos == begin( dist ) )
   {
      if( std::abs( (*pos)[1] - value ) < 0.000001 ) { pos = begin( dist ) + 1; }
   }
   auto tmp_pt_1 = DataPt{ (*(pos-1))[1], (*(pos-1))[0] };
   auto tmp_pt_2 = DataPt{ (*pos)[1], (*pos)[0] };
   return DataPt{ lin_interpol( value, tmp_pt_1, tmp_pt_2 ), value };
}



//------------------------------------------------------------------------------
DataPt pt_at_y_val_bckwrd( Dist const& dist, double value )
{
   using std::rbegin;
   using std::rend;

   auto search_val = DataPt{ 0.0, value };
   auto pos = std::lower_bound( rbegin( dist ), rend( dist ), search_val,
                       []( DataPt const& lt, DataPt const& rt )
                       { return lt[1] < rt[1]; }
              );

   if( pos == rend( dist ) )
   {
      throw std::runtime_error( "value not in distribution" );
   }

   if( pos == rbegin( dist ) )
   {
      if( std::abs( (*pos)[1] - value ) < 0.000001 ) { pos = rbegin( dist ) + 1; }
   }
   auto tmp_pt_1 = DataPt{ (*(pos-1))[1], (*(pos-1))[0] };
   auto tmp_pt_2 = DataPt{ (*pos)[1], (*pos)[0] };
   return DataPt{ lin_interpol( value, tmp_pt_1, tmp_pt_2 ), value };
}



//------------------------------------------------------------------------------
DataPt pt_at_y_val( Dist const& dist, double value, From start = From::FRONT )
{
   if( start == From::FRONT )
   {
      return pt_at_y_val_frwrd( dist, value );
   }
   else if( start == From::END )
   {
      return pt_at_y_val_bckwrd( dist, value );
   }
}

// DataPt pt_at_y_val_ascend( Dist const& dist, double pos )
// {}

// DataPt pt_at_y_val_descend( Dist const& dist, double pos )
// {}


//==============================================================================
int main( int argc, char* argv[] )
{
   using std::begin;
   using std::end;

   if( argc < 2 )
   {
      std::cout << "You have to provide at least one file name to analyse.\n";
      return 0;
   }
   
   for( int arg_idx( 1 ); arg_idx != argc; ++arg_idx )
   {
      auto data = read_file( argv[arg_idx] );
      std::string file_name( argv[arg_idx] );
#ifdef _MSC_VER
      auto pos = file_name.begin() + file_name.find_last_of( '\\' );
#else
      auto pos = file_name.begin() + file_name.find_last_of( '/' );
#endif
      if( pos != file_name.end() )
      {
         file_name.erase( file_name.begin(), pos + 1 );
      }
      if( data.empty() )
      {
         std::cout << "Argument " << file_name <<
               " is not a valid file or does not exist.  Will be ignored.\n";
         continue;
      }

      
      // Calculate and apply shift
      auto orig_dose_at_zero = pt_at_x_val( data, 0.0 )[1];
      auto posi_50_ascend = pt_at_y_val( data, 0.5 * orig_dose_at_zero )[0];
      auto posi_50_descend = pt_at_y_val( data, 0.5 * orig_dose_at_zero, From::END )[0];
      auto width = posi_50_descend - posi_50_ascend;
      auto shift = posi_50_descend - ( width / 2.0 );

      for( auto& pt : data ) { pt[0] -= shift; } // axis is now at 0
      auto new_dose_at_zero = pt_at_x_val( data, 0.0 )[1];
      

      // Interpolate to fixed positions
      double min_size_dim = std::floor(
               std::min( std::abs( data.front()[0] ), std::abs( data.back()[0] ) ) * 10.0 ) / 10.0;
      double step = 0.1;
      auto half_nb_of_steps = static_cast<int>( min_size_dim / step );
      
      Dist neg_new_data;
      neg_new_data.reserve( half_nb_of_steps );
      for( int step_idx(1); step_idx != half_nb_of_steps; ++step_idx )
      {
         neg_new_data.push_back( pt_at_x_val( data, ( -step_idx * step ) ) );
      }
      
      Dist pos_new_data;
      pos_new_data.reserve( half_nb_of_steps );
      for( int step_idx(1); step_idx != half_nb_of_steps; ++step_idx )
      {
         pos_new_data.push_back( pt_at_x_val( data, ( step_idx * step ) ) );
      }


      // Calculate symmetry
      double symmetry = 0.0;
      for( int pt_idx( 0 ); pt_idx != neg_new_data.size(); ++pt_idx )
      {
         auto abs_diff = std::abs( neg_new_data[pt_idx][1] - pos_new_data[pt_idx][1] );
         symmetry = std::max( symmetry, abs_diff / new_dose_at_zero * 100.0 );
      }

      std::cout << '(' << file_name << ')' << '\t' << "symétrie: ";
      std::cout.precision( 2 );
      std::cout.setf( std::ios::fixed, std:: ios::floatfield );
      std::cout << symmetry << '\n';
      
   }

   return 0;
}
