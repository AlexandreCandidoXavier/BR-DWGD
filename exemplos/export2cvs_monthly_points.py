import numpy as np
import xarray as xr
import pandas as pd
import time

"""
Exportando dados MENSAIS de todas as variaveis para determinadas posicoes/pontos geograficas.

Para as variáveis pr e ETo, os valores são os acumulados,
para as demais, é média dos mês 
"""
# periodo para ser exportado
date_start, date_end = '1961-01-01', '2020-07-31'

# set correct path of the netcdf files
path_var = '/home/alexandre/Dropbox/grade_2020/data/netcdf_files/'

# Posicoes: Colocar em ordem, separando por virgula. Neste exemplo temos dois pontos em que as coordenadas
# (lat, lon) sao (-20.6,-44.6) e  (-21.0, -44.1), respectivamente para o primeiro e segundo ponto.
# Pode-se colocar quantos pontos quiser, apenas separe por virgula.
lat = [-20.6, -21.0]
lon = [-44.6, -44.1]

# variables names
var_names = ['Rs', 'u2','Tmax', 'Tmin', 'RH', 'pr', 'ETo']

# function to read the netcdf files
def rawData(var2get_xr, var_name2get):
    return var2get_xr[var_name2get].loc[dict(time=slice(date_start, date_end))].sel(longitude=xr.DataArray(lon, dims='z'),
                                          latitude=xr.DataArray(lat, dims='z'),
                                          method='nearest').values

# getting data from NetCDF files
for n, var_name2get in enumerate(var_names):
    print("getting " + var_name2get)
    if var_name2get in ["pr", "ETo"]:
        var2get_xr = xr.open_mfdataset(path_var + var_name2get + '*.nc').resample(time="M").sum("time")
        # var2get_xr[var_name2get].sel(latitude=lat[0], longitude=lon[0], method='nearest').plot()
    else:
        var2get_xr = xr.open_mfdataset(path_var + var_name2get + '*.nc').resample(time="M").mean("time")

    if n == 0:
        var_ar = rawData(var2get_xr, var_name2get)
        n_lines = var_ar.shape[0]
        time = var2get_xr.time.values
    else:
        var_ar = np.c_[var_ar, rawData(var2get_xr, var_name2get)]

# saving
for n in range(len(lat)):
    name_file =  'lat{:.2f}_lon{:.2f}.csv'.format(lat[n], lon[n])
    print(f'arquivo {n + 1} de um total de {len(lat)}; nome do arquivo: {name_file}')
    if ~np.isnan(var_ar[0, n]):
        file = var_ar[:, n::len(lon)]
        pd.DataFrame(file, index=time, columns=var_names).to_csv(name_file, float_format='%.1f')
