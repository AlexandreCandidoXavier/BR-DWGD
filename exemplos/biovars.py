import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import regionmask
import os
import geopandas as gpd
from joblib import Parallel, delayed
import rioxarray

"""
Geração dos dados bioclim de acordo com:
https://github.com/rspatial/dismo/blob/master/R/biovars.R

https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/15774-malhas.html?=&t=acesso-ao-produto
Geometria dos municípios foi simplificada em: https://mapshaper.org/
Arquivos shapes utilizados para este código, em: /exemplos/shape_file/
"""

def coletando_dados(n, mask, lon, lat, municipios_data_pandas):
    # print(n)
    sel_mask = mask.where(mask == n).values
    id_lon = lon[np.where(~np.all(np.isnan(sel_mask), axis=0))]
    if len(id_lon) >= 1:
        id_lat = lat[np.where(~np.all(np.isnan(sel_mask), axis=1))]
        out_sel = var_extrapolado.sel(latitude=slice(id_lat[0], id_lat[-1]),
                                               longitude=slice(id_lon[0], id_lon[-1])).compute().where(mask == n)

        for k in range(out_sel.shape[0]):
            municipios_data_pandas[k] = np.nanmean(out_sel[k].values)

    else:
        lon_municipios, lat_municipios = municipios_centroid_x[n], municipios_centroid_y[n]
        out_sel = var_extrapolado.sel(latitude=lat_municipios,
                                               longitude=lon_municipios,
                                               method='nearest')
        municipios_data_pandas = out_sel.values

    return municipios_data_pandas


# caminho dos arquivos NetCDF da grade BR-DWGD
path_netcdf = '/home/alexandre/Dropbox/grade_2020/data/netcdf_files/'
prec = xr.open_mfdataset(path_netcdf + 'pr*.nc')


# periodo a ser consedirado para coleta das variáveis
date_start, date_end = '1990-01-01', '2019-12-31'

def normais(var2get_xr):
    prec = xr.open_mfdataset(path_netcdf + var2get_xr + '*.nc')[var2get_xr]
    # criando mascara para o continente e mar
    mask_ocean = 2 * np.ones(prec.shape[1:]) * np.isnan(prec.isel(time=0))
    mask_land = 1 * np.ones(prec.shape[1:]) * ~np.isnan(prec.isel(time=0))
    mask_array = (mask_ocean + mask_land).values
    # incorporando mascara em ETo
    prec.coords['mask'] = xr.DataArray(mask_array, dims=('latitude', 'longitude'))
    if var2get_xr == 'pr':
        pr = prec.loc[dict(time=slice(date_start, date_end))]. \
            resample(time='M').sum('time').where(prec.mask == 1).groupby("time.month").mean().compute()
        wet = prec.loc[dict(time=slice(date_start, date_end))]. \
            resample(time='M').sum('time').where(prec.mask == 1).groupby("time.season").mean().compute()
        return pr, wet
    else:
        var = xr.open_mfdataset(path_netcdf + var2get_xr + '*.nc')[var2get_xr]. \
            loc[dict(time=slice(date_start, date_end))].groupby("time.month").mean().compute()
        var_quarter = xr.open_mfdataset(path_netcdf + var2get_xr + '*.nc')[var2get_xr]. \
            resample(time='M').mean('time').where(prec.mask == 1).groupby("time.season").mean().compute()
        return var, var_quarter

tmax, tmax_qrt = normais('Tmax')
tmin, tmin_qrt = normais('Tmin')
prec, wet = normais('pr')
tavg = (tmax.compute() + tmin.compute()) / 2
tavg_qrt = (tmax_qrt + tmin_qrt) / 2

# gravando netcdf mensal e sazonal
tmax.to_dataset(name='tmax').to_netcdf('tmax_mensal.nc')
tmin.to_dataset(name='tmin').to_netcdf('tmin_mensal.nc')
prec.to_dataset(name='prec').to_netcdf('prec_mensal.nc')
tavg.to_dataset(name='tavg').to_netcdf('tavg.nc')

tmax_qrt.to_dataset(name='tmax_qrt').to_netcdf('tmax_qrt.nc')
tmin_qrt.to_dataset(name='tmin_qrt').to_netcdf('tmin_qrt.nc')
wet.to_dataset(name='wet').to_netcdf('prec_qrt.nc')
tavg_qrt.to_dataset(name='tavg_qrt').to_netcdf('tavg_qrt.nc')

# bio1 = Mean annual temperature
bio1 = tavg.mean('month')

# bio2 = Mean diurnal range (mean of max temp - min temp)
bio2 = (tmax - tmin).mean("month")

# bio4 = Temperature seasonality (standard deviation *100)
bio4 = tavg.std('month') * 100

# bio5 = Max temperature of warmest month
bio5 = tmax.max('month')

# bio6 = Min temperature of coldest month
bio6 = tmin.min('month')

# bio7 = Temperature annual range (bio5-bio6)
bio7 = (bio5 - bio6)

# bio3 = Isothermality (bio2/bio7) (* 100)
bio3 = (bio2 / bio7) * 100

# bio8 = Mean temperature of the wettest quarter
wet_np = wet.values
ind = wet_np.argmax(axis=0)
a1, a2 = np.indices(ind.shape)
bio8 = tavg_qrt.values[ind, a1, a2]

# bio9 = Mean temperature of driest quarter
ind = wet_np.argmin(axis=0)
bio9 = tavg_qrt.values[ind, a1, a2]

# bio10 = Mean temperature of warmest quarter
tavg_qrt_np = tavg_qrt.values
ind = tavg_qrt_np.argmax(axis=0)
bio10 = tavg_qrt.values[ind, a1, a2]

# bio11 = Mean temperature of coldest quarter
ind = tavg_qrt_np.argmin(axis=0)
bio11 = tavg_qrt.values[ind, a1, a2]

# bio12 = Total (annual) precipitation
bio12 = prec.sum('month').where(prec.mask == 1, np.nan)

# bio13 = Precipitation of wettest month
bio13 = prec.max('month')

# bio14 = Precipitation of driest month
bio14 = prec.min('month')

# bio15 = Precipitation seasonality (coefficient of variation)
bio15 = prec.mean('month')/prec.std('month')

# bio16 = Precipitation of wettest quarter
ind = wet_np.argmax(axis=0)
bio16 = wet_np[ind, a1, a2]

# bio17 = Precipitation of driest quarter
ind = wet_np.argmin(axis=0)
bio17 = wet_np[ind, a1, a2]

# bio18 = Precipitation of warmest quarter
ind = tavg_qrt_np.argmax(axis=0)
bio18 = wet_np[ind, a1, a2]

# juntando e gravando
biovar = np.concatenate((bio1.values[np.newaxis, :, :],
                         bio2.values[np.newaxis, :, :],
                         bio3.values[np.newaxis, :, :],
                         bio4.values[np.newaxis, :, :],
                         bio5.values[np.newaxis, :, :],
                         bio6.values[np.newaxis, :, :],
                         bio7.values[np.newaxis, :, :],
                         bio8[np.newaxis, :, :],
                         bio9[np.newaxis, :, :],
                         bio10[np.newaxis, :, :],
                         bio11[np.newaxis, :, :],
                         bio12.values[np.newaxis, :, :],
                         bio13.values[np.newaxis, :, :],
                         bio14.values[np.newaxis, :, :],
                         bio15.values[np.newaxis, :, :],
                         ))

bio_names = [n for n in range(1, 16)]
lats, lons = bio1.latitude.values, bio1.longitude.values
bioclim = xr.DataArray(biovar, coords=[bio_names, lats, lons], dims=['bio_names', 'latitude', 'longitude']).to_dataset(name='bioclim')
bioclim.to_netcdf('bioclim.nc', format="NETCDF4")

# pegando o arquivo shape dos municipios
path = os.path.join(os.getcwd(), 'shape_file/BR_Municipios_2021.shp')
municipios = gpd.read_file(path, encoding="utf-8")

# centróides dos municípios para serem utilizados quando
# o município é muito pequeno e não há célula da grade dentro.
# Vai pegar da célula mais próxima ao centroide do município
municipios_centroid_x = municipios.to_crs(epsg=5641).centroid.to_crs(municipios.crs).x.values
municipios_centroid_y = municipios.to_crs(epsg=5641).centroid.to_crs(municipios.crs).y.values

# mascara dos municípios
municipios_mask_poly = regionmask.Regions(name="municipios_mask",
                                          numbers=list(range(len(municipios))),
                                          names=list(municipios.CD_MUN),
                                          abbrevs=list(municipios.NM_MUN),
                                          outlines=list(municipios.geometry.values[i] for i in range(len(municipios))))

# mascara continente/mar
var = bioclim.bioclim
mask_ocean = 2 * np.ones(var.shape[1:]) * np.isnan(var.isel(bio_names=1))
mask_land = 1 * np.ones(var.shape[1:]) * ~np.isnan(var.isel(bio_names=1))
mask_array = (mask_ocean + mask_land).values
var.coords['mask'] = xr.DataArray(mask_array, dims=('latitude', 'longitude'))

# Extrapolando os dados gradeados, para que municípios que estão
# no limite do Brasil tenham dados.
print("Extrapolando")
var.rio.write_nodata(np.nan, inplace=True)
var.rio.write_crs("epsg:4326", inplace=True)
var_extrapolado = var.rio.interpolate_na()

mask_munic = municipios_mask_poly.mask(var_extrapolado['latitude'], var_extrapolado['longitude'])

municipios_data_pandas = np.empty((len(var_extrapolado.bio_names)))
lat = mask_munic.latitude.values
lon = mask_munic.longitude.values

# start = time.time()
# c = coletando_dados(n, mask_munic, lon, lat, municipios_data_pandas)
# print(time.time() - start)

print("Extraindo dados dos municípios")
# coletando_dados(0, mask_munic, lon, lat, municipios_data_pandas)
saida = Parallel(n_jobs=-1, verbose=4)(delayed(coletando_dados)(n, mask_munic, lon, lat, municipios_data_pandas)
                                       for n in range(len(municipios.CD_MUN)))  # municipios_data_pandas.shape[0]

bio_names = [f'bio{n}' for n in var_extrapolado.bio_names.values]
municipios_data = pd.DataFrame(np.empty((len(municipios.CD_MUN), len(var_extrapolado.bio_names)),
                               dtype="int"), columns=bio_names, index=municipios.index)

for n in range(len(municipios.CD_MUN)):
    municipios_data.iloc[n, :] = saida[n]

# concatenado dados shape com dados da grade reamostrados
municipios_data.set_index(municipios.index)
municipios = pd.concat((municipios, municipios_data), axis=1)

# gravando
print("Gravando")
municipios.to_file('bioClim.shp')

print("Rodou")
