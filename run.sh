# Clean up.
rm *.o
rm *.so
rm pytaf.c

# Cython
python setup.py build_ext --inplace
# python example.py
python test_n.py
python modis2ug.rn.py
python modis2ug.rn.h5.py
python test_s.py
python modis2ug.rs.py
python modis2ug.rs.h5.py
