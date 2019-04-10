#!/usr/bin/env python
import argparse
import glob
import h5py
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap

def print_args(a):
    print(a.dset)
    print(a.S)
    print(a.scale)
    
def count_images(d):
    n = 1
    for i in range(0,d.ndim-2):
        # print(d.shape[i])
        n = n *d.shape[i]
    # print(n)
    return n

def plot_image(data, lat, lon, file_name, n, step=1, scale=False):
    plt.close('all')
    data[data == -999] = np.nan
    datam = np.ma.masked_array(data, np.isnan(data))
    m = Basemap(projection='cyl', resolution='l',
                llcrnrlat=-90, urcrnrlat = 90,
                llcrnrlon=-180, urcrnrlon = 180)
    m.drawcoastlines(linewidth=0.5)
    m.drawparallels(np.arange(-90., 120., 30.), labels=[1, 0, 0, 0])
    m.drawmeridians(np.arange(-180, 180., 45.), labels=[0, 0, 0, 1])
    m.scatter(lon[::step, ::step],
              lat[::step, ::step],
              c=datam[::step, ::step], s=1,
              edgecolors=None, linewidth=0)
    if scale: 
        plt.colorbar()
    fig = plt.gcf()
    fig.suptitle('{0}.{1}'.format(file_name, n))
    pngfile = file_name+'.'+str(n)+'.py.png'
    fig.savefig(pngfile)
    
parser = argparse.ArgumentParser(
    description='Generate browse images from AF files.')
parser.add_argument('dset', type=str,
                    help='HDF5 dataset name with group path')
parser.add_argument('S', type=int, help='an integer for subsetting step')
parser.add_argument('-s', '--scale', action='store_false',
                    help='turn off applying scale/offset')
args = parser.parse_args()
# print_args(args)

for filename in glob.glob('*.h5'):
    print('Opening '+filename)
    with h5py.File(filename, 'r') as f:
        if args.dset in f.keys():
            dset = f[args.dset]
            lat = f['/Geolocation/Latitude']
            lon = f['/Geolocation/Longitude']
            print('Found '+args.dset+' in '+filename)
            print('No. of dimensions = ' + str(dset.ndim))
            if(dset.ndim > 2):
                n = count_images(dset)
                x = dset.shape[dset.ndim - 1]
                print(x)
                y = dset.shape[dset.ndim - 2]
                print(y)
                data = dset[:]
                datas = data.reshape(n, y, x)
                print(datas.shape)
                for i in range(0, n):
                    print(i)
                    plot_image(datas[i,:,:], lat, lon,
                               filename, i, args.S, args.scale)
            else:
                data = dset[:]
                plot_image(data, lat, lon,
                           filename, 0, args.S, args.scale)
