import xarray as xr
import matplotlib.pyplot as plt

""" Plotando a média mensal da ET0 para algumas cidades.
"""

# pegando variavel
path_var = '/home/alexandre/Dropbox/grade_2020/data/netcdf_files/'
ds = xr.open_mfdataset(path_var + 'ETo*.nc').sel(time=slice('1961-01-01','1989-12-31'))
var = ds['ETo']

# cidades e coordenadas
cityNames = ['Santa Maria-RS', 'Manaus-AM',
             'Petrolina-PE', 'Alegre-ES']
cityCoord = [[-29.7, -53.7],
             [-3., -60.],
             [-9.4, -40.5],
             [-20.7, -41.5]]

# calculando a media mensal
varMean = var.resample(time='M').mean('time')

# plotando
for n, city in enumerate(cityNames):
    varMean.sel(latitude=cityCoord[n][0], longitude=cityCoord[n][1],
                method='nearest').plot(label=city, linewidth=1)

plt.ylim(1, 8)
plt.title('')
plt.legend(ncol=2)
plt.show(block=False)
