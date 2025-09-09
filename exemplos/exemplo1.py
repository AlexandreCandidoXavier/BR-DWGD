import xarray as xr
import matplotlib.pylab as plt

"""
Plotando dados e controles para todo Brasil em um dia:
Todos os arquivos da variavel diarios de Rs sao necessarios, ou seja,
os de controle tambem
"""

# set correct path of the variables
path_var = '/home/alexandre/Dropbox/grade_2020/grade_2020-07_2023/data/netcdf_new_dtype/'


# set correct path of the controls
path_control = '/home/alexandre/Dropbox/grade_2020/grade_2020-07_2023/data/netcdf_new_dtype/Controls/'

name_var = 'Rs'
data = xr.open_mfdataset(path_var + name_var + '*.nc', chunks={})
data_control = xr.open_mfdataset(path_control + name_var + '*.nc')
Rs = data[name_var]
Rs_count = data_control['count']
Rs_dist_nearest = data_control['dist_nearest']

# escolhendo o dia
day2get = '1961-01-01'

# Plotando
_, (ax1, ax2, ax3) = plt.subplots(1, 3)
Rs.sel(time=day2get).plot(ax=ax1), ax1.axis('off')
Rs_count.sel(time=day2get).plot(ax=ax2), ax2.axis('off')
Rs_dist_nearest.sel(time=day2get).plot(ax=ax3), ax3.axis('off')
plt.show()
