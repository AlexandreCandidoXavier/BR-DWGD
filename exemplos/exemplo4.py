import xarray as xr
import matplotlib.pyplot as plt

"""
Plotando a média mensal da ET0 para algumas cidades periodo 1961-01-01' ate '1989-12-31.
"""

# pegando variavel
path_var = '/home/alexandre/Dropbox/grade_2020/grade_2020-07_2023/data/netcdf_new_dtype/'
ds = xr.open_mfdataset(path_var + 'ETo*.nc', chunks={'time': 3000}).sel(time=slice('1961-01-01', '1989-12-31'))
var = ds['ETo']

# cidades e coordenadas
cityInformation = {
    'Santa Maria-RS': [-29.7, -53.7],
    'Manaus-AM': [-3., -60.],
    'Petrolina-PE': [-9.4, -40.5],
    'Alegre-ES': [-20.7, -41.5]
}

# calculando a media mensal
varMean = var.resample(time='ME').mean('time')

# plotando
for city, cityCoord in cityInformation.items():
    varMean.sel(latitude=cityCoord[0], longitude=cityCoord[1],
                method='nearest').plot(label=city, linewidth=1)

plt.ylim(1, 8)
plt.title('')
plt.legend(ncol=2)
plt.show()
