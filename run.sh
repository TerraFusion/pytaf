# Tihs script is useful for Cython interface development and testing without
# installation. For example, you can run this scaript after you edit pytaf.pyx.
#
# Last Update: 2019/04/22

# Clean up.
python setup.py clean --all
rm *.o
rm *.so
rm pytaf.c

# Build Cython interface on the current working directory.
python setup.py build_ext --inplace

# Test example scripts.
python modis2ug.rn.py
python modis2ug.rn.h5.py
python modis2ug.rs.py
python modis2ug.rs.h5.py
python misr2ceres.py
python misr2ceres.h5.py
