# Clean up.
rm *.o
rm *.so
rm pytaf.c

# Cython
python setup.py build_ext --inplace
# python example.py
python test_n.py
python test_s.py


