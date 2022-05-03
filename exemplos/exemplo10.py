from matplotlib import pyplot as plt
import pandas as pd
import xarray as xr
import gcsfs
import datetime
import numpy as np
import glob
import os


path2save_nc_file = "/home/alexandre/Dropbox/grade_2020/cmip6/"
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

# lendo os dados BR-DWGD
# set correct path of the variables
path = '/home/alexandre/Dropbox/grade_2020/data/netcdf_files/'

# definição das datas para calculo das normais
day_first, day_last = '1986-01-01', '2015-12-31'

tmax = xr.open_mfdataset(path + 'Tmax*.nc', combine='by_coords').Tmax
tmax_month = tmax.sel(time=slice(day_first, day_last)).groupby('time.month').mean()

tmin = xr.open_mfdataset(path + 'Tmin*.nc', combine='by_coords').Tmin
tmin_month = tmin.sel(time=slice(day_first, day_last)).groupby('time.month').mean()

# calculado as medias mensais
tas_BRDWGD = (tmax_month + tmin_month) / 2

tas_BRDWGD.coords['longitude'] = tas_BRDWGD.coords['longitude'] + 360


# criando mascara para o continente e mar
mask_ocean = 2 * np.ones(tas_BRDWGD.shape[1:]) * np.isnan(tas_BRDWGD.isel(month=0))
mask_land = 1 * np.ones(tas_BRDWGD.shape[1:]) * ~np.isnan(tas_BRDWGD.isel(month=0))
mask_array = mask_ocean + mask_land

# incorporando mascara
tas_BRDWGD.coords['mask'] = (('latitude', 'longitude'), mask_array)
tas_BRDWGD = tas_BRDWGD.to_dataset(name='tas')

df_results = pd.DataFrame(tas_BRDWGD.tas.mean(['latitude', 'longitude']).values, columns=['tas'])
df_results['month'] = months
df_results['source_id'] = 'BR-DWGD'
df_results['institution_id'] = 'UFES'
df_results['member_id'] = 'None'

# lendo banco de dados cmip6
arquivos = [file.split('/')[-1] for file in glob.glob(path2save_nc_file + "*.csv")]
if "cmip6-zarr-consolidated-stores.csv" in arquivos:
    df = pd.read_csv(path2save_nc_file + 'cmip6-zarr-consolidated-stores.csv')
else:
    df = pd.read_csv('https://storage.googleapis.com/cmip6/cmip6-zarr-consolidated-stores.csv')
    df.to_csv(path2save_nc_file + 'cmip6-zarr-consolidated-stores.csv')



# lendo banco de dados cmip6 os dados historicos para variável "tas" (temperatura na superfície) mensal
df_historical = df.query("activity_id == 'CMIP' & table_id == 'Amon' & " +\
    "variable_id == 'tas' & experiment_id == 'historical' & member_id == 'r1i1p1f1'")
print('Quantidade de modelos em df_historical:', len(df_historical))

##################################################################################
# gcs = gcsfs.GCSFileSystem(token='anon')
#
# # pegando todos os modelos, calculando as medias mensais e gravando em ".nc"
# # para posteriro utilização. Isto pode ser um pouco demorado
# source_ids = np.unique(df_historical.source_id.values)
# for n, source_id in enumerate(source_ids):
#     member_ids = df_historical.query(f"source_id == '{source_id}'").member_id
#     member_id = member_ids.iloc[0]
#     zstore = df_historical.query(f"source_id == '{source_id}' & member_id == '{member_id}'")
#     zstore_hist = zstore.zstore.values[0]
#
#     mapper = gcs.get_mapper(zstore_hist)
#     ds_hist = xr.open_zarr(mapper, consolidated = True)
#
#     start_time = pd.to_datetime(datetime.date(1850,1,15)) # I chose 15 for all dates to make it easier.
#     time_new_hist = [start_time + pd.DateOffset(months = x) for x in range(len(ds_hist.time))]
#     ds_hist = ds_hist.assign_coords(time = time_new_hist)
#
#     start_date = pd.to_datetime(datetime.date(1985,1,1))
#     end_date = pd.to_datetime(datetime.date(2014,12,31))
#     ds_hist_sel = ds_hist.isel(time=(ds_hist.time >= start_date) & (ds_hist.time <= end_date))
#     # ds_hist_sel.load()
#
#     tas_avg_hist = ds_hist_sel.groupby('time.month').mean() - 273.15
#
#     # recortando para a area BR-DGWD e reamostrando para a resolicao
#     try:
#         if 'latitude' in list(tas_avg_hist.coords._names):
#             tas_avg_hist = xr.DataArray(tas_avg_hist.tas.values.astype(np.float32),
#                                         coords=[tas_avg_hist.month.values, tas_avg_hist.latitude.values,
#                                                 tas_avg_hist.longitude.values],
#                                         dims=["month", "latitude", "longitude"])
#         else:
#             tas_avg_hist = xr.DataArray(tas_avg_hist.tas.values,
#                                         coords=[tas_avg_hist.month.values, tas_avg_hist.lat.values, tas_avg_hist.lon.values],
#                                         dims=["month", "latitude", "longitude"])
#
#
#         tas_avg_hist = tas_avg_hist.interp(latitude=tas_BRDWGD.latitude, longitude=tas_BRDWGD.longitude)
#         tas_avg_hist = tas_avg_hist.where(tas_BRDWGD.mask == 1)
#         tas_avg_hist = tas_avg_hist.to_dataset(name='tas')
#         tas_avg_hist.to_netcdf(path2save_nc_file + source_id + '_' + member_id + ".nc")
#         print('n: ', n, '; source_id', source_id, 'hist date range  :', ds_hist.time[0].values, ' , ', ds_hist.time[-1].values)
#
#     except:
#         print('source_id', source_id, 'erro')
##########################################################################################


# lendo dos dados das normais mensais
nc_files = glob.glob(path2save_nc_file + "*.nc")
for nc_file in nc_files:
    tas_avg_hist = xr.open_mfdataset(nc_file)
    source_id = nc_file.split("/")[-1].split("_")[0]
    df_tas_avg_hist = pd.DataFrame(tas_avg_hist.tas.mean(['latitude', 'longitude']), columns=['tas'])
    df_tas_avg_hist['month'] = months
    df_tas_avg_hist['source_id'] = source_id
    df_tas_avg_hist['institution_id'] = df_historical.loc[df_historical.source_id == source_id].institution_id.values[0]
    df_tas_avg_hist['member_id'] = df_historical.loc[df_historical.source_id == source_id].member_id.values[0]
    df_results = pd.concat([df_results, df_tas_avg_hist])
    # tas_avg_hist.tas.mean(['latitude', 'longitude']).plot(label=source_id)
    # tas_avg_hist.tas.isel(month=0).plot()
############################################################################
# dados observados "x"
x = df_results.loc[df_results["source_id"]=="BR-DWGD", "tas"]

source_ids = np.unique(df_results.loc[:, "source_id"].values)
source_ids = source_ids[source_ids != "BR-DWGD"]

liga = True
for source_id in source_ids:
    y = df_results.loc[df_results["source_id"]==source_id, "tas"]
    bias = np.mean(y - x)
    correlation = np.corrcoef(y, x)[1, 0]
    rmse = np.sqrt(((y - x)**2).mean())
    if liga:
        statisticas = pd.DataFrame([[bias, correlation, rmse]], columns=['Bias', 'R', 'RMSE'])
        statisticas['source_id'] = source_id
        liga = False
    else:
        statisticas_n = pd.DataFrame([[bias, correlation, rmse]], columns=['Bias', 'R', 'RMSE'])
        statisticas_n ['source_id'] = source_id
        statisticas = pd.concat([statisticas, statisticas_n])

vars = ['Bias', 'R', 'RMSE']
fig, axes = plt.subplots(1, 3, figsize=(3,12))
for n, var in enumerate(vars):
    sns.heatmap(pd.DataFrame(statisticas.loc[:, var].values, index=statisticas.loc[:, "source_id"].values,
                             columns=[var]), ax=axes[n], cbar_kws = dict(use_gridspec=False,location="bottom"))
    if n == 0:
        axes[n].set_yticks(range(len(var)))
        axes[n].set_yticklabels(statisticas.loc[:, "source_id"].values)
    else:
        axes[n].set_yticklabels('')


statisticas['R_rank'] = statisticas['R'].rank(ascending=False).astype(int)
statisticas['Bias_rank'] = abs(statisticas['Bias']).rank().astype(int)
statisticas['RMSE_rank'] = statisticas['RMSE'].rank().astype(int)
statisticas['AV rank'] = statisticas[['R_rank', 'Bias_rank', 'RMSE_rank']].mean(1)
statisticas.sort_values(by=['AV rank'], inplace=True)
# statisticas.set_index("source_id", inplace=True)

# plotando os 10 melhores
# dados observados
plt.plot(months, df_results.iloc[:12, 0], "--", color="gray", label="BR-DWGD")

source_id_tops = statisticas.loc[:, "source_id"].values[:20]
for source_id in source_id_tops:
    plt.plot(months, df_results.loc[df_results["source_id"] == source_id, "tas"], label=source_id)

plt.legend(ncol=2)
print("FIM")

# mapper = gcs.get_mapper(zstore_ssp585)
# ds_ssp585 = xr.open_zarr(mapper, consolidated = True)
#
# print('ssp585 date range:', ds_ssp585.time[0].values, ' , ', ds_ssp585.time[-1].values)
#
# start_time = pd.to_datetime(datetime.date(2015,1,15))
# time_new_ssp585 = [start_time + pd.DateOffset(months = x) for x in range(len(ds_ssp585.time))]
# ds_hist = ds_hist.assign_coords(time = time_new_hist)
# ds_ssp585 = ds_ssp585.assign_coords(time = time_new_ssp585)
#
#
#
# df_ssp585 = df.query("activity_id=='ScenarioMIP' & table_id == 'Amon' & " +\
#     "variable_id == 'tas' & experiment_id == 'ssp585' & member_id == 'r1i1p1f1'")
# print('Length of df_ssp585:', len(df_ssp585))
#
# zstore_ssp585 = df_ssp585.query(f"source_id == '{model}'").zstore.values[0]

# start_date = pd.to_datetime(datetime.date(2070,1,1))
# end_date = pd.to_datetime(datetime.date(2099,12,31))
# ds_ssp585_sel = ds_ssp585.isel(time=(ds_ssp585.time >= start_date) & (ds_ssp585.time <= end_date))
#
# tas_avg_ssp585 = ds_ssp585_sel.groupby('time.month').mean()
# ds_ssp585_sel.load()
#
# tas_30yr_diff = tas_avg_ssp585 - tas_avg_hist
# tas_30yr_diff.tas.plot(col = 'month', col_wrap = 6, vmax = 10, vmin = 0, cmap = 'hot_r')



# https://colab.research.google.com/drive/1B7gFBSr0eoZ5IbsA0lY8q3XL8n-3BOn4#scrollTo=LFwzDxM08CZr