import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

"""
Exportando normais climatologicas período 1990/01/01-2019/12/31
no formato NetCDF
"""

# diretório dos arquivos NetCDF
path_var = '/home/alexandre/Dropbox/grade_2020/data/netcdf_files/'

# intervalo da seria histórica para os calculo das normais
date_start, date_end = '1991-01-01', '2019-12-31'

# nomes das variaveis, sendo:
# Tmean = (Tmax + Tmin) /2
var_names = ['pr', 'ETo', "Rs", 'Rs', 'u2', "Tmax", "Tmin", "Tmean"]

for var_name in var_names:
    print("rodando: " + var_name)

    # lendo arquivos
    if var_name != "Tmean":
        var = xr.open_mfdataset(path_var + var_name + '*.nc')
    else:
        tmax = xr.open_mfdataset(path_var + 'Tmax*.nc')
        tmin = xr.open_mfdataset(path_var + 'Tmin*.nc')
        var = (tmax["Tmax"] + tmin["Tmin"]) / 2
        var[var_name] = var

    # criando mascara para o continente e mar
    mask_ocean = 2 * np.ones(var[var_name].shape[1:]) * np.isnan(var[var_name].isel(time=0))
    mask_land = 1 * np.ones(var[var_name].shape[1:]) * ~np.isnan(var[var_name].isel(time=0))
    mask_array = (mask_ocean + mask_land).values

    # incorporando mascara em var
    var.coords['mask'] = xr.DataArray(mask_array, dims=('latitude', 'longitude'))

    # reamostrando para escala de tempo mensal
    # se variavel pr, ETo ou Rs, os valores mensais serão acumuladas
    if var_name in ['pr', 'ETo', "Rs"]:
        var_mean = var.loc[dict(time=slice(date_start, date_end))].resample(time='M').sum('time')
    else:
        var_mean = var.loc[dict(time=slice(date_start, date_end))].resample(time='M').mean('time')

    # calculando as médias mensais
    var_normal = var_mean.where(var.mask == 1).groupby('time.month').mean(dim='time')

    # plotando
    # var_normal[var_name].plot(x='longitude', y='latitude', col='month', col_wrap=4)
    # plt.show()

    # gravando
    var_normal.to_netcdf(var_name + "_normal.nc")
