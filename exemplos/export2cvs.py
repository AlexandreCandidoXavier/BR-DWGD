import numpy as np
import xarray as xr
import pandas as pd
import time

"""
Exportando dados de todas as variaveis para determinadas posicoes geograficas. 
"""

# Posicoes: Colocar em ordem, separando por virgula. Neste exemplo temos dois pontos em que as coordenadas
# (lat, lon) sao (-20.6,-44.6) e  (-21.0, -44.1), respectivamente para o primeiro e segundo ponto.
# Pode-se colocar quantos pontos quiser, apenas separe por virgula.
lat = [-11.71]
lon = [-61.73]

# variables names
var_names = ['Rs', 'u2','Tmax', 'Tmin', 'RH', 'pr', 'ETo']

# set correct path of the netcdf files
path_var = '/home/alexandre/Dropbox/grade_2020/data/netcdf_files/'

# function to read the netcdf files
def rawData(var2get_xr, var_name2get):
    return var2get_xr[var_name2get].sel(longitude=xr.DataArray(lon, dims='z'),
                                          latitude=xr.DataArray(lat, dims='z'),
                                          method='nearest').values

# getting data from NetCDF files
for n, var_name2get in enumerate(var_names):
    print("getting " + var_name2get)
    var2get_xr = xr.open_mfdataset(path_var + var_name2get + '*.nc')
    if n == 0:
        var_ar = rawData(var2get_xr, var_name2get)
        n_lines = var_ar.shape[0]
        time = var2get_xr.time.values
    else:
        var_ar = np.c_[var_ar, rawData(var2get_xr, var_name2get)]

# saving
for n in range(len(lat)):
    print('arquivo {} de um total de {}'.format(n+1, len(lat)))
    name_file =  'lat{:.2f}_lon{:.2f}.csv'.format(lat[n], lon[n])
    if ~np.isnan(var_ar[0, n]):
        file = var_ar[:, n::len(lon)]
        pd.DataFrame(file, index=time, columns=var_names).to_csv(name_file, float_format='%.1f')