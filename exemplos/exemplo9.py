import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import seaborn as sns

"""Comportamento da temperatuta média em diferentes regioes do Brasil
"""

# colocar em "path" o caminho correto dos arquivos NetCDF
path = '/home/alexandre/Dropbox/grade_2020/data/netcdf_files/'

# definição da dadas para calculos
day_first, day_last = '1961-01-01', '2019-12-31'

# pegando Tmax e Tmin, v2.1 e calculando as suas respectivas medias anuais
tmax = xr.open_mfdataset(path + 'Tmax*.nc').Tmax
tmax_yearly = tmax.sel(time=slice(day_first, day_last)).resample(time='Y').mean('time')

tmin = xr.open_mfdataset(path + 'Tmin*.nc').Tmin
tmin_yearly = tmin.sel(time=slice(day_first, day_last)).resample(time='Y').mean('time')

# Temperatura anual
temp_mean_yearly = (tmax_yearly+tmin_yearly) / 2

# calculos dos pesos das celulas de acordo com sua latitude
weights = np.cos(np.deg2rad(temp_mean_yearly.latitude))
weights.name = "weights"

# figura regioes
fig, ax = plt.subplots(1)
temp_mean_yearly.isel(time=0).plot(ax=ax)

# definindo regioes: cada linha tem as coordenadas limites da respectiva região na ordem:
# sul, sudeste, nordeste, centro-oeste, norte
names_regions = ['Sul', 'Sudeste', 'Nordeste', 'Centro-Oeste', 'Norte']
names_regions_abre = ['S', 'SE', 'NE', 'CO', 'N',]
regiao_lat = [[-34, -22],
              [-25.6, -13.8],
              [-18.6, -1],
              [-24.3, -7],
              [-12.7, 6]]

regiao_lon = [[-58, -47.2],
              [-51.5, -39],
              [-49, -34.4],
              [-62, -45.6],
              [-74, -46.3]]

# calculation of the regions yearly Tmean
for n in range(5):
    print(names_regions[n])
    lat_min, lat_max = regiao_lat[n][0], regiao_lat[n][1]
    lon_min, lon_max = regiao_lon[n][0], regiao_lon[n][1]

    ax.plot([lon_min, lon_max, lon_max, lon_min, lon_min],
            [lat_min, lat_min, lat_max, lat_max, lat_min], label=names_regions[n])

    # creating a mask of the region
    mask = (lon_min < tmax_yearly.longitude) & (lon_max > tmax_yearly.longitude) & \
           (lat_min < tmax_yearly.latitude) &  (lat_max > tmax_yearly.latitude)
    # yearly tmean to Dataframe
    # inserindo o peso na regiao
    temp_mean_yearly_r = temp_mean_yearly.where(mask)
    temp_mean_yearly_w = temp_mean_yearly_r.weighted(weights)
    temp_mean_yearly_region_w = temp_mean_yearly_w.mean(['latitude', 'longitude']).values
    df_region = pd.DataFrame(np.c_[temp_mean_yearly_r.time.dt.year,
                                   temp_mean_yearly_region_w], columns=['year', 't_mean'])
    df_region['region'] = names_regions[n]
    if n == 0:
        df_all = df_region
    else:
        df_all = pd.concat([df_all, df_region])

ax.legend(loc=2, prop={'size': 6})
ax.set_xlim(-75, -34)
ax.set_ylim(-35, 7)

# grafico simple linear regression "year" versus "t_mean" para cada regiao
g = sns.lmplot(x='year', y="t_mean", hue="region", data=df_all, legend=False)
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
       ncol=2, mode="expand", borderaxespad=0.)
plt.xlim(1960,2021)
plt.tight_layout()
plt.show()

# estatisticas por regiao na variavel "stat_region"
df_all['year_ano'] = df_all['year']
df_all['datas'] = df_all.index.values
df_all['name_legend'] = ''
stat_region = np.zeros((5,4))
for n in np.arange(5):
    x = df_all[df_all['region'] == names_regions[n]].year_ano.values
    y = df_all[df_all['region'] == names_regions[n]].t_mean.values
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    stat_region[n] = np.array([slope, r_value, p_value, std_err])

print(stat_region)
