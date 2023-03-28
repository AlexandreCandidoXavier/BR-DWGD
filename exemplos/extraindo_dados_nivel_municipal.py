import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import regionmask
import cartopy.crs as ccrs
import os
import geopandas as gpd
from joblib import Parallel, delayed
import rioxarray

# Extração dados MENSAIS de precipitação em nível municipal para o Brasil.
# Shape dos municípios obtidos em em:
# https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/15774-malhas.html?=&t=acesso-ao-produto
# Geometria shape foi simplificada em:
# https://mapshaper.org/
# arquivos shapes encontrados no diretório: exemplos/shape_file

var_names = ['Tmax', 'Tmin', 'Rs', 'RH', 'u2', 'pr']

# escolhedo a variavel, neste caso precipitação
nvar2get = "pr"

# caminho dos arquivos NetCDF da grade BR-DWGD
path_netcdf = '/home/alexandre/Dropbox/grade_2020/data/netcdf_files/'
var = xr.open_mfdataset(path_netcdf + nvar2get + '*.nc')[nvar2get]

# pegando o arquivo shape dos municipios
path = os.path.join(os.getcwd(), 'shape_file/BR_Municipios_2021.shp')
municipios = gpd.read_file(path)

# cetróides dos municipios
municipios_centroid_x = municipios.to_crs(epsg=5641).centroid.to_crs(municipios.crs).x.values
municipios_centroid_y = municipios.to_crs(epsg=5641).centroid.to_crs(municipios.crs).y.values

# mascara municipios
municipios_mask_poly = regionmask.Regions(name="municipios_mask",
                                          numbers=list(range(len(municipios))),
                                          names=list(municipios.CD_MUN),
                                          abbrevs=list(municipios.NM_MUN),
                                          outlines=list(municipios.geometry.values[i] for i in range(len(municipios))))

# mascara continente/mar
mask_ocean = 2 * np.ones(var.shape[1:]) * np.isnan(var.isel(time=0))
mask_land = 1 * np.ones(var.shape[1:]) * ~np.isnan(var.isel(time=0))
mask_array = (mask_ocean + mask_land).values

var.coords['mask'] = xr.DataArray(mask_array, dims=('latitude', 'longitude'))

# reamostrando para mensal
var_resample = var.resample(time='M').sum('time').where(var.mask == 1).compute()

# extrapolando
var_resample.rio.write_nodata(np.nan, inplace=True)
var_resample.rio.write_crs("epsg:4326", inplace=True)
var_resample_extrapolado = var_resample.rio.interpolate_na()


mask = municipios_mask_poly.mask(var_resample_extrapolado.isel(time=0),
                                 lat_name='latitude',
                                 lon_name='longitude')

# plt.figure(figsize=(12, 8))
# ax = plt.axes()
# # mask.plot(ax = ax)
# municipios.plot(ax=ax, alpha=0.8, facecolor='none', lw=1)
# var.isel(time=-10).plot(ax=ax)
# municipios.boundary.plot(ax=ax)

municipios_data_pandas = np.empty((len(var_resample_extrapolado.time)))

def coletando_dados(n, mask, lon, lat, municipios_data_pandas):
    # print(n)
    sel_mask = mask.where(mask == n).values
    id_lon = lon[np.where(~np.all(np.isnan(sel_mask), axis=0))]
    if len(id_lon) >= 1:
        id_lat = lat[np.where(~np.all(np.isnan(sel_mask), axis=1))]
        out_sel = var_resample_extrapolado.sel(latitude=slice(id_lat[0], id_lat[-1]),
                                   longitude=slice(id_lon[0], id_lon[-1])).compute().where(mask == n)

        for k in range(out_sel.shape[0]):
            cells = out_sel[k].values
            if np.all(np.isnan(cells)):
                municipios_data_pandas[k] = np.nan
            else:
                municipios_data_pandas[k] = np.nanmean(cells)

        # plt.figure(figsize=(12, 8))
        # ax = plt.axes()
        # out_sel.isel(time=0).plot(ax=ax)
        # municipios.plot(ax=ax, alpha=0.8, facecolor='none')
        # ax.axis(xmin=-64, xmax=-36, ymin=-32, ymax=-6)
        # plt.close("all")

    else:
        print(f'não tem célula dentro do limite: {n}')
        # centroid = municipios.centroid[municipios[n].name == municipios.CD_MUN]
        lon_municipios, lat_municipios = municipios_centroid_x[n], municipios_centroid_y[n]
        out_sel = var_resample_extrapolado.sel(latitude=lat_municipios,
                                   longitude=lon_municipios, method='nearest')
        municipios_data_pandas = out_sel.values
    #     saida = out_sel.values
    #
    return municipios_data_pandas


lat = mask.latitude.values
lon = mask.longitude.values

# start = time.time()
# b = []
# for n in range(219, 220):
#     municipios_data_pandas = np.empty((len(var_resample_extrapolado.time)))
#     c = coletando_dados(n, mask, lon, lat, municipios_data_pandas)
#     b.append(c)
#
# print(time.time() - start)

municipios_data_pandas = np.empty((len(var_resample_extrapolado.time)))
saida = Parallel(n_jobs=-1, verbose=4)(delayed(coletando_dados)(n, mask, lon, lat, municipios_data_pandas)
                                       for n in range(len(municipios.CD_MUN)))  # municipios_data_pandas.shape[0]

year = var_resample_extrapolado.time.dt.year.values
month = var_resample_extrapolado.time.dt.month.values
ano_mes = [f'{year[n]}-{month[n]}' for n in range(len(year))]
municipios_data = pd.DataFrame(np.empty((len(municipios.CD_MUN), len(var_resample_extrapolado.time)), dtype="int"),
                               columns=ano_mes,
                               index=municipios.index)

for n in range(len(municipios.CD_MUN)):
    municipios_data.iloc[n, :] = saida[n].astype("int")

# concatenado dados shape com dados da grade
municipios_data.set_index(municipios.index)
municipios = pd.concat((municipios, municipios_data), axis=1)


# plotando o mes de janeiro de 1961
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
time = '1961-01-31'
var_resample.sel(time=time).plot(ax=axes[0])
axes[0].set_title("prec = " + "1961-1")
var_resample_extrapolado.sel(time=time).plot(ax=axes[1])
axes[1].set_title("prec_extrap = " + "1961-1")
municipios.plot(ax=axes[2], column="1961-1")

# gravando
name2save = 'preci_muni_mensal.geojson' # para shapefile: 'preci_muni_mensal.shp'
municipios.to_file(name2save)
print("acabou")