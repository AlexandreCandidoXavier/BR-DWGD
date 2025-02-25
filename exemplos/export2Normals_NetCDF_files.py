import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import hvplot.xarray
import hvplot.pandas
import holoviews as hv
import hvplot

"""
Exportando normais climatologicas período 1990/01/01-2019/12/31
no formato NetCDF
"""

# diretório dos arquivos NetCDF
path_var = '/home/alexandre/Dropbox/grade_2020/grade_2020-07_2023/data/netcdf_new_dtype/'

# intervalo da seria histórica para os calculo das normais
date_start, date_end = '2017-01-01', '2019-12-31'

# nomes das variaveis, sendo:
# Tmean = (Tmax + Tmin) /2
var_names = ['pr', "Tmean", "Tmax", "Tmin", 'ETo', "Rs", 'Rs', 'u2']

for var_name in var_names:
    print("rodando: " + var_name)

    # lendo arquivos
    if var_name != "Tmean":
        var = xr.open_mfdataset(path_var + var_name + '*.nc')
    else:
        tmax = xr.open_mfdataset(path_var + 'Tmax*.nc', chunks={'time': 3000})
        tmin = xr.open_mfdataset(path_var + 'Tmin*.nc', chunks={'time': 3000})
        var = (tmax["Tmax"] + tmin["Tmin"]) / 2
        var[var_name] = var

    # criando mascara para o continente e mar
    if var_name == 'pr':
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

    var_mean_slice = var_mean.sel(latitude=slice(-22.5, -18.), longitude=slice(-50.5, -46.))

    # calculando as médias mensais
    # var_normal = var_mean_slice.where(var.mask == 1).groupby('time.month').mean(dim='time')
    frame_width = 500
    label = f'{var_name}; ano-mês: {str(var_mean_slice.time[0].values)[:7]}'

    if var_name != 'Tmean':
        fig = var_mean_slice[var_name].isel(time=0).hvplot.image(coastline=True,
                                                           cmap="viridis", tiles='EsriImagery',
                                                           label=label, frame_width=frame_width)
    else:
        fig = var_mean_slice.isel(time=0).hvplot.image(coastline=True, cmap="viridis", tiles='EsriImagery',
                                                     label=label, frame_width=frame_width)

    hvplot.save(fig, var_name + '_test.html')

    # plotando
    # var_normal[var_name].plot(x='longitude', y='latitude', col='month', col_wrap=4)
    # plt.show()

    # gravando
    var_mean_slice.to_netcdf(var_name + "_mensal.nc")
    pass
