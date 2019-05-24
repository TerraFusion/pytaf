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

## Example


  

## Limitation

The pytaf.find_nn_block_index() function modifies target lat/lon values.
Thus, you need to make copies before you call resample_n() function.
