#!/usr/bin/env python
import string
import argparse
import glob
import h5py
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap

def get_base_name(s):
    s_lpos = s.rfind("/")
    if s_lpos != -1:
        s=s[s_lpos+1:]
    return s

def print_args(a):
    print(a.dset)
    print(a.S)
    print(a.scale)
    print(a.zoom)
    
def count_images(d):
    n = 1
    for i in range(0,d.ndim-2):
        # print(d.shape[i])
        n = n *d.shape[i]
    # print(n)
    return n

def get_attrs(d):
    valid_min=None
    valid_max=None
    scale_factor=1.0
    add_offset=0.0
    a = d.attrs
    if 'valid_max' in a.keys():
        valid_max = dset.attrs['valid_max']
        print(type(valid_max))
        print('valid_max='+str(valid_max))
    if 'valid_min' in a.keys():    
        valid_min = dset.attrs['valid_min']
        print('valid_min='+str(valid_min))        
    if 'scale_factor' in a.keys():
        scale_factor = dset.attrs['scale_factor']
        print('scale_factor='+str(scale_factor))
    if 'add_offset' in a.keys():
        add_offset = dset.attrs['add_offset']
        print('add_offset='+str(add_offset))
    return valid_min, valid_max, scale_factor, add_offset
    
def plot_image(data, lat, lon,
               file_name, dset_name,n, step=1, scale=False,
               valid_min=None, valid_max=None,
               scale_factor=1.0, add_offset=0.0, zoom=False):
    plt.close('all')
    if scale:
         invalid = np.logical_or(data > valid_max,
                                 data < valid_min)
         data[invalid] = np.nan
         data = scale_factor * data + add_offset
    data[data == -999] = np.nan    
    datam = np.ma.masked_array(data, np.isnan(data))
    if zoom:
        m = Basemap(projection='cyl', resolution='l',
                    llcrnrlat=np.min(lat), urcrnrlat=np.max(lat),
                    llcrnrlon=np.min(lon), urcrnrlon=np.max(lon))
        slat = (np.ceil(np.max(lat)) -  np.floor(np.min(lat))) / 6.0
        slon = (np.ceil(np.max(lon)) -  np.floor(np.min(lon))) / 6.0        
                                  
        m.drawparallels(np.arange(np.floor(np.min(lat)),
                                  np.ceil(np.max(lat)), slat),
                        labels=[1, 0, 0, 0])
        m.drawmeridians(np.arange(np.floor(np.min(lon)),
                                  np.ceil(np.max(lon)), slon),
                        labels=[0, 0, 0, 1])

    else:
        m = Basemap(projection='cyl', resolution='l',
                    llcrnrlat=-90, urcrnrlat = 90,
                    llcrnrlon=-180, urcrnrlon = 180)
        m.drawparallels(np.arange(-90., 120., 30.), labels=[1, 0, 0, 0])
        m.drawmeridians(np.arange(-180, 180., 45.), labels=[0, 0, 0, 1])
        
    m.drawcoastlines(linewidth=0.5)
    m.scatter(lon[::step, ::step],
              lat[::step, ::step],
              c=datam[::step, ::step], s=1,
              edgecolors=None, linewidth=0)
    if scale: 
        plt.colorbar()
    fig = plt.gcf()
    fig.suptitle('{0}.{1}.{2}'.format(file_name, dset_name,n))
    pngfile = file_name+'.'+dset_name+'.'+str(n)+'.py.png'
    fig.savefig(pngfile)
    
parser = argparse.ArgumentParser(
    description='Generate browse images from AF files.')
parser.add_argument('dset', type=str,
                    help='HDF5 dataset name with group path')
parser.add_argument('S', type=int, help='an integer for subsetting step')
parser.add_argument('-s', '--scale', action='store_false',
                    help='turn off applying scale/offset')
parser.add_argument('-z', '--zoom', action='store_true',
                    help='turn off applying zoom')
args = parser.parse_args()
# print_args(args)

for filename in glob.glob('*.h5'):
    print('Opening '+filename)
    with h5py.File(filename, 'r') as f:
        if args.dset in f.keys():
            dset = f[args.dset]
            dset_name = get_base_name(args.dset)
            lat = f['/Geolocation/Latitude']
            lon = f['/Geolocation/Longitude']
            print('Found '+args.dset+' in '+filename)
            print('No. of dimensions = ' + str(dset.ndim))
            mn, mx, sf, ao = get_attrs(dset)            
            if(dset.ndim > 2):
                n = count_images(dset)
                x = dset.shape[dset.ndim - 1]
                y = dset.shape[dset.ndim - 2]
                data = dset[:]
                datas = data.reshape(n, y, x)
                print('Data has been reshaped:')
                print(datas.shape)

                for i in range(0, n):
                    # print(i)
                    plot_image(datas[i,:,:], lat, lon,
                               filename, dset_name,i, args.S, args.scale,
                               mn, mx, sf, ao, args.zoom)
            else:
                data = dset[:]
                plot_image(data, lat, lon,
                           filename, 0, args.S, args.scale,
                           mn, mx, sf, ao, args.zoom)
