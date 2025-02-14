import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.feature import BORDERS

""" Abrindo e plotando a normal da temperatura media do mês janeiro, período 1961/01/01-1989/12/31 
"""

# pegando Tmax e Tmin, v2.1 e calculando as msuas respectivas medias mensais
path = '/home/alexandre/Dropbox/grade_2020/grade_2020-07_2023/data/netcdf_new_dtype/'

# definição das datas para calculo das normais
day_first, day_last = '1961-01-01', '1989-12-31'

tmax = xr.open_mfdataset(path + 'Tmax*.nc', chunks={'time': 3000}).Tmax
tmax_month = tmax.sel(time=slice(day_first, day_last)).groupby('time.month').mean('time')

tmin = xr.open_mfdataset(path + 'Tmin*.nc', chunks={'time': 3000}).Tmin
tmin_month = tmin.sel(time=slice(day_first, day_last)).groupby('time.month').mean('time')

# plotando normal, mes de Janeiro
month = 1 # 1=janeiro, 2=fevereiro, .... 12=dezembro
((tmax_month.sel(month=month) + tmin_month.sel(month=month)) / 2).plot(cmap=plt.cm.jet)

# plotando as medias para todos os meses
t_media = ((tmax_month + tmin_month) / 2)
p = t_media.plot(transform=ccrs.PlateCarree(), cmap=plt.cm.jet, col='month', col_wrap=4,
                                    subplot_kws={'projection': ccrs.PlateCarree()}, extend='both')

for ax in p.axes.flat:
    ax.coastlines()
    ax.add_feature(BORDERS)
    ax.set_extent([-75, -33, -33.5, 6])

plt.show()
