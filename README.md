[![Build Status](https://travis-ci.org/TerraFusion/pytaf.svg?branch=master)](https://travis-ci.org/TerraFusion/pytaf)

# pytaf
Python interface for Terra Advanced Fusion Resample/Reprojection functions

  * It is Cython-based.


## Installation

If you're new to Python, see our
[Wiki page](https://github.com/TerraFusion/pytaf/wiki) for complete guide.

Use `$pip install -r requirements.txt` to install required packages.
Then, run `$pip install .` or `$python setup.py install`.

If you have openMP installed, you can take advantage of openMP by using
 `$python setup.py.omp install`.


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
See [example.py](example.py) for usage.			    
See [Wiki page](https://github.com/TerraFusion/pytaf/wiki/User-Guide) for details.

## Example

run `python example.py` to see how resample_n() and resample_s() work.

More examples can be found under directory `examples`.

TerraFusion examples can be found under subdirectory `AF`. More information on the TerraFusion examples, check
[wiki page](https://github.com/TerraFusion/pytaf/wiki/TerraFusion-Examples) for details.


## Limitation

The pytaf.find_nn_block_index() function modifies target lat/lon values.
Thus, you need to make copies before you call resample_n() and resample_s() functions.

The resample_s assumes valid data value >=0. Both functions assign -999.0 to data points that no valid values can be found.
