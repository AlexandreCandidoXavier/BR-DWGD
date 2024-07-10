import xarray as xr
import matplotlib.pyplot as plt

"""Plotando media mensal da Umidade Relativa (1990-01-01-2019-12-31)
RH_20010101_20200731_BR-DWGD_UFES_UTEXAS_v_X.XX.nc
RH_19810101_20001231_BR-DWGD_UFES_UTEXAS_v_X.XX.nc
RH_19610101_19801231_BR-DWGD_UFES_UTEXAS_v_X.XX.nc
"""

# pegando variavel
path_var = '/home/alexandre/Dropbox/grade_2020/data/netcdf_files/'
ds = xr.open_mfdataset(path_var + 'RH*.nc', chunks={'time': 3000})

# pegando a variavel RH entre '1990-01-01' a '2019-12-31'
RH_data = ds.RH.sel(time=slice('1990-01-01', '2019-12-31'))

# agrupando em media mensal
RH_mean_month = RH_data.groupby('time.month').mean('time')

# plotando
RH_mean_month.plot(x='longitude', y='latitude', col='month',
                   cmap='RdBu', col_wrap=4)
plt.show()
