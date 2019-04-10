# pytaf
Python interface for Terra Advanced Fusion

  * It is Cython-based.
  * It covers the basic functions in [advancedFusion/reproject.cpp](https://github.com/TerraFusion/advancedFusion/blob/master/src/reproject.cpp).

See [example.py](example.py) for usage.

## MODIS to User-defined grid

Here is the workflow. The [AFtool.cpp](https://github.com/TerraFusion/advancedFusion/blob/master/src/AFtool.cpp) is the reference model.

1. Open AF file that contains many granules.
2. Generate target lat/lon datasets (using GDAL).
3. Use pytaf.find_nn_block_index() function to find indices in the source
dataset that corresponds to target lat/lon.
4. Use pytaf.interpolate_nn() function to retrieve values from the source
using the indices.
5. Plot data for comparison or save the interpolated data in HDF5 dataset.
6. In the future, may save the data in  netcdf-4 or geotiff.

See [modis2ug.py](modis2ug.py) for the complete code.

## MISR to MODIS

See [misr2modis.py](misr2modis.py) for the work-in-progress code.

## Browse image generation tool

  This script loops through AF files in the current working directory and
  generates images. For dataset that has more than 2D, it will be subsetted.
  The index values in higher diemensions will be used as output file name. 

  Usage:

  python gen_img.py [-s] [-z] /group/path/to/hdf5/dset stride

  -s: do not apply scale/offset. do not show color bar.
  stride: subsetting stride for large dataset.
  
  -z: zoom image by limiting map to lat/lon boundary

  Example:

  python gen_img.py -s /Source/Data_Fields/MISR_Radiance 100

  The above command will generate images by subsetting every 100th data point.
  
  
##  TO-DO
* Unit tests
* Packaging for pip/conda install
* More conversion examples

## Limitation

The pytaf.find_nn_block_index() function modifies target lat/lon values.

