import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

"""Plotando e exportando em "csv" dados medios mensais de Tmax para 
algumas localidades. Normais 01/01/1990 a 31/12/2019
Arquivos:
"""
# pegando variavel
path_var = '/home/alexandre/Dropbox/grade_2020/data/netcdf_files/'
var = xr.open_mfdataset(path_var + 'Tmax*.nc', chunks={'time': 3000})['Tmax'].sel(time=slice('1990-01-01', '2019-12-31'))

# Nome e posicao dos pontos
posicoes = {'INPE-SP': [-23.2, -45.9],
            'UFCG-PB': [-7.2, -35.9],
            'UFC-CE': [-3.85, -38.6]}

varMonthly2Export = pd.DataFrame(np.empty((12, len(posicoes))),
                                 columns=posicoes.keys(),
                                 index=range(1, 13))
# media mensal
for name, lat_lon in posicoes.items():
    tmaxCityDaily = var.sel(latitude=lat_lon[0],
                            longitude=lat_lon[1],
                            method='nearest')
    tmaxCityMonthly = tmaxCityDaily.groupby('time.month').mean('time')
    # ploting
    tmaxCityMonthly.plot(label=name)
    # concatenating in pandas
    varMonthly2Export[name] = tmaxCityMonthly

plt.ylim(22, 33)
plt.title('')
plt.legend()
plt.show()

# exporting
varMonthly2Export.to_csv('dadosMensais.csv')
