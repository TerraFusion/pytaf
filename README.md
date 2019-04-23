[![Build Status](https://travis-ci.org/TerraFusion/pytaf.svg?branch=master)](https://travis-ci.org/TerraFusion/pytaf)

# pytaf
Python interface for Terra Advanced Fusion

  * It is Cython-based.
  * It covers the basic functions in [advancedFusion/reproject.cpp](https://github.com/TerraFusion/advancedFusion/blob/master/src/reproject.cpp).

See [example.py](example.py) for usage.

## Installation

If you're new to Python, see our
[Wiki page](https://github.com/TerraFusion/pytaf/wiki) for complete guide.

Use `$pip install -r requirements.txt` to install required packages.
Then, run `$pip install .` or `$python setup.py install`.


## Test

Use `$nosetests` or `$python setup.py test`.

## Usage

First, import the package.

`import pytaf`

Second, call the resample function. There are two high-level functions.

* resample_n(): nearest neighbor interpolation
* resample_s(): summary interpolation

```
target_data = pytaf.resample_s(source_lat, source_lon, target_lat, target_lon, 
	                       source_data, max_radius, std_dev, no_pixels)
```			    
			    
See [Wiki page](https://github.com/TerraFusion/pytaf/wiki/User-Guide) for details.

## MODIS to User-defined grid

Here is the workflow. The [AFtool.cpp](https://github.com/TerraFusion/advancedFusion/blob/master/src/AFtool.cpp) is the reference model.

1. Open AF file that contains many granules.
2. Generate target lat/lon datasets (using GDAL).
3. Use pytaf.find_nn_block_index() function to find indices in the source
dataset that corresponds to target lat/lon.
4. Use pytaf.interpolate_nn() function to retrieve values from the source
using the indices.
5. Plot the interpolated data for comparison or save them as an HDF5 dataset.
6. Alternatively, you may want to save the data in netcdf-4 or geotiff format.

See [modis2ug.py](modis2ug.py) for the complete code.

## MISR to MODIS

See [misr2modis.py](misr2modis.py) for the verification of pytaf against
AF tool outputs.

You can compare the results using the two plots:

[AF Tool generated output](misr2modis.h5.py.s.png)

[pytaf generated output](misr2modis.h5.py.t.png)

## MISR to CERES

See [misr2ceres.py](misr2ceres.py) to test 1-d target lat/lon handling.

You can check the MISR output plot.

[pytaf generated output of AN Red Radiance](misr2ceres.h5.py.png)

You can compare the above plot with CERES data plot from BF file.

[BF plot for Solar Zenith Angle](TERRA_BF_L1B_O53557_20100112014327_F000_V001.h5.py.png)

## Browse image generation tool

  This script loops through AF files in the current working directory and
  generates images. For dataset that has more than 2D, it will be subsetted.
  The index values in higher diemensions will be used as output file name. 

  Usage:

  `$python gen_img.py [-s] [-z] /hdf5/group/path/to/dset stride`

  -s: do not apply scale/offset. do not show color bar.
  
  -z: zoom image by limiting map to lat/lon boundary

  stride: subsetting stride for large dataset.

  Example:

  `$python gen_img.py -s /Source/Data_Fields/MISR_Radiance 100`

  The above command will generate images by subsetting every 100th data point.
  

  
##  TO-DO
* Unit tests
* Packaging for pip/conda install
* More conversion examples (e.g., CERES to MISR)

## Limitation

The pytaf.find_nn_block_index() function modifies target lat/lon values.
Thus, you need to make copies before you call resample_n() function.
