import numpy as np
import xarray as xr
import pandas as pd
import time

"""
Exportando dados DIÁRIOS de todas as variaveis para uma regiao, onde se conhece os 
limites da região e período de tempo dos dados à ser exportado.

Para as variáveis pr e ETo, os valores são os acumulados,
para as demais, é média dos mês.
"""

# set correct path of the netcdf files
path_var = '/home/alexandre/Dropbox/grade_2020/data/netcdf_files/'

# periodo para ser exportado
date_start, date_end = '1961-01-01', '2020-07-31'

# limits of the area
lat_min, lat_max = -17.4, -15.7
lon_min, lon_max = -40.5, -38.9

# variables names
var_names = ['Rs', 'u2','Tmax', 'Tmin', 'RH', 'pr', 'ETo']


# latitude and longitude of GRID
var = xr.open_mfdataset(path_var + 'pr*.nc')
latitude = var.latitude.values
longitude = var.longitude.values

lat = latitude[np.array(np.nonzero((latitude >= lat_min) &
                                  (latitude <= lat_max))).flatten()]
lon = longitude[np.array(np.nonzero((longitude >= lon_min) &
                                  (longitude <= lon_max))).flatten()]

lon, lat = np.meshgrid(lon, lat)
lon, lat = lon.flatten(), lat.flatten()

# function to read the netcdf files
def rawData(var2get_xr, var_name2get):
    return var2get_xr[var_name2get].loc[dict(time=slice(date_start, date_end))].sel(longitude=xr.DataArray(lon, dims='z'),
                                          latitude=xr.DataArray(lat, dims='z'),
                                          method='nearest').values

# getting data from NetCDF files
for n, var_name2get in enumerate(var_names):
    print("lendo: " + var_name2get)
    # var2get_xr = xr.open_mfdataset(path_var + var_name2get + '*.nc').chunk(chunks={"time": 400})
    if var_name2get in ["pr", "ETo"]:
        var2get_xr = xr.open_mfdataset(path_var + var_name2get + '*.nc').resample(time="M").sum("time")
        # var2get_xr[var_name2get].sel(latitude=lat[0], longitude=lon[0], method='nearest').plot()
    else:
        var2get_xr = xr.open_mfdataset(path_var + var_name2get + '*.nc').resample(time="M").mean("time")

    if n == 0:
        var_ar = rawData(var2get_xr, var_name2get)
        n_lines = var_ar.shape[0]
        time = var2get_xr.loc[dict(time=slice(date_start, date_end))].time.values
    else:
        var_ar = np.c_[var_ar, rawData(var2get_xr, var_name2get)]

# saving
for n in range(len(lat)):
    name_file = 'lat{:.2f}_lon{:.2f}.csv'.format(lat[n], lon[n])
    print(f'arquivo {n + 1} de um total de {len(lat)}; nome do arquivo: {name_file}')
    print(name_file)
    if ~np.isnan(var_ar[0, n]):
        file = var_ar[:, n::len(lon)]
        pd.DataFrame(file, index=time, columns=var_names).to_csv(name_file, float_format='%.1f')