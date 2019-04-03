# pytaf
Python interface for Terra Advanced Fusion

  * It is Cython-based.
  * It covers the basic functions in [advancedFusion/reproject.cpp](https://github.com/TerraFusion/advancedFusion/blob/master/src/reproject.cpp).

See [example.py](example.py) and [misr2modis.py](misr2modis.py) for usage.

# MODIS to User-defined grid.

Here is the workflow. The AFTool.c is the reference model.

1. Open AF file that contains many granules.
2. Generate lat/lon datasets using GDAL.
3. Use pytaf.find_nn_block_index() function. find_nn() generates core on Linux.


