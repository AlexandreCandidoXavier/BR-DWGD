import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

""" Extraindo para uma posicao (Umuarama-PR) a serie historica diaria 
da temperatura maxima (Tmax), calculando a sua media 
mensal (01/01/1961-12/2010) e exportando dados diarios em arquivo cvs:

Tmax_20010101_20200731_BR-DWGD_UFES_UTEXAS_v_X.XX.nc
Tmax_19810101_20001231_BR-DWGD_UFES_UTEXAS_v_X.XX.nc
Tmax_19610101_19801231_BR-DWGD_UFES_UTEXAS_v_X.XX.nc
"""

# versoes
print(xr.__version__) # 0.17.0
print(np.__version__) # 1.20.2
print(pd.__version__) # 1.2.4

# set correct path of the variables
path_var = '/home/alexandre/Dropbox/grade_2020/data/netcdf_files/'
ds = xr.open_mfdataset(path_var + 'Tmax*.nc')

# pegando a variavel Tmax entre '1961-01-01', '1989-12-31'
Tmax_data = ds.Tmax.sel(time=slice('1961-01-01','1989-12-31'))

# pegando os dados para o posicao de Umuarama/Parana
Tmax_data_temporal = Tmax_data.sel(latitude=-23.76,longitude=-53.30,
                                   method='nearest')
# plotando dados diarios
_, (ax1, ax2) = plt.subplots(1, 2)
Tmax_data_temporal.plot(ax=ax1, linewidth=.3)

# plotando a media mensal
Tmax_mean_month = Tmax_data_temporal.groupby('time.month').mean('time')
Tmax_mean_month.plot(ax=ax2)
plt.show(block=False)

# exportando dados diarios em cvs: nome do arquivo 'Tmax.cvs'
fileName = 'Tmax.csv'
days = np.array(Tmax_data_temporal.time)
data_dataframe = pd.DataFrame(np.array(Tmax_data_temporal), index=days)
data_dataframe.to_csv(fileName)
