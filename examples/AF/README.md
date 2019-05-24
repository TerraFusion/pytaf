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

See [modis2ug.py](https://github.com/TerraFusion/pytaf/blob/master/examples/AF/modis2ug.py) for the complete code.

## MISR to MODIS

See [misr2modis.py](https://github.com/TerraFusion/pytaf/blob/master/examples/AF/misr2modis.py) for the verification of pytaf against
AF tool outputs.

You can compare the results using the two plots:

[AF Tool generated output](https://github.com/TerraFusion/pytaf/blob/master/examples/AF/misr2modis.h5.py.s.png)

[pytaf generated output](https://github.com/TerraFusion/pytaf/blob/master/examples/AF/misr2modis.h5.py.t.png)

## MISR to CERES

See [misr2ceres.py](https://github.com/TerraFusion/pytaf/blob/master/examples/AF/misr2ceres.py) to test 1-d target lat/lon handling.

You can check the MISR output plot.

[pytaf generated output of AN Red Radiance](https://github.com/TerraFusion/pytaf/blob/master/examples/AF/misr2ceres.h5.py.png)

You can compare the above plot with CERES data plot from BF file.

[BF plot for Solar Zenith Angle](https://github.com/TerraFusion/pytaf/blob/master/examples/AF/TERRA_BF_L1B_O53557_20100112014327_F000_V001.h5.py.png)

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
  
