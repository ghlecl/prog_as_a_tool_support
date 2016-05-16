
#Summary
This project is the code used in a presentation made at the CHU de Quebec - Université Laval
on using programming as a tool.

Some radiation therapy data is analyzed using a few techniques:

1. Microsoft Excel (TM)
2. Vanilla Python code
3. Numpy Python code
4. C++ code


##Data Generation
The data represents a dose profile in radiation therapy, i.e. a plot of dose as a function
of lateral position in a medical radiation beam.  Ignoring the file header, it consists of
two columns representing position (cm) and dose (%).

The original data I had available was not suitable for the presentation, since it had
already been analysed and modified for our purposes.  In reality, the data to be analyzed
has a variable number of entries and the step between the points varies.  Of course, real
data is not 100% symmetrical, since this is what the analysis is calculating.  Thus, I have
created suitable data for the presentation.  This has been done mostly using python (with
a bit of manual editing, hey, I'm not perfect).

In the data_generation folder, you will find two sub-folders and a python script.  In the
'orig' subfolder, you can find the original treated data, which would be useless for the
purposes of the presentation.  In the 'var_lengths' subfolder, you can find the data with a
variable number of entries, which was made by hand.  I just copied the files and removed
a centimeter of data from each end.  Could have been done programmatically as well.

The last part of the data generation is the script.  This script will take the variable
length data and read it.  It will then introduce a position shift on every point (selected
randomly, but the same for every position) and some noise in the dose for the inner 80% to
simulate non symmetrical data.  The new data will be written in the data folder of the project.

##Analysis
Not done yet.