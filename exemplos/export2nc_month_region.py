import numpy as np
import xarray as xr
import pandas as pd
import time
import matplotlib.pyplot as plt
import rioxarray

path_var = '/home/alexandre/Dropbox/grade_2020/data/netcdf_files/'

lat_min, lat_max = -22, -13.8
lon_min, lon_max = -42.1, -38.5

# variables names
var_names = ['Rs', 'u2', 'Tmax', 'Tmin', 'RH', 'pr', 'ETo']

prec = xr.open_mfdataset(path_var + 'pr*.nc')

# criando mascara para o continente e mar
mask_ocean = 2 * np.ones(prec['pr'].shape[1:]) * np.isnan(prec['pr'].isel(time=0))
mask_land = 1 * np.ones(prec['pr'].shape[1:]) * ~np.isnan(prec['pr'].isel(time=0))
mask_array = (mask_ocean + mask_land).values

prec.coords['mask'] = xr.DataArray(mask_array, dims=('latitude', 'longitude'))

for n, var_name2get in enumerate(var_names):
    print("lendo: " + var_name2get)
    if var_name2get in ["pr", "ETo"]:
        var2get_xr = xr.open_mfdataset(path_var + var_name2get + '*.nc').resample(time="M").sum("time")

    else:
        var2get_xr = xr.open_mfdataset(path_var + var_name2get + '*.nc').resample(time="M").mean("time")

    var2get_xr = var2get_xr.where(prec.mask == 1, np.nan)
    var2get_xr.where(((var2get_xr.latitude < lat_max) &
                      (var2get_xr.latitude > lat_min) &
                      (var2get_xr.longitude < lon_max) &
                      (var2get_xr.longitude > lon_min)), drop=True).to_netcdf(f"{var_name2get}_test.nc")

