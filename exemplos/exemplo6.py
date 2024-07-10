import xarray as xr # versao '0.9.6'
import matplotlib.pyplot as plt # versao '2.0.2'

""" Para todas as variaveis existem dois controles, um he a distancia 
do centro da celula a estacao mais proxima ("dist_nearest") e o outro
he o numero de estacoes/pluviometros dentro da celula (informacoes 
ver "paper"). 
Aqui serao plotados os controles da grade precipitacaoo em duas 
localidades, Sorriso-MT e Campinas-SP (na verdade he da 
celula mais proxima a estas cidades).
"""

# lendo arquivo
path_var = '/home/alexandre/Dropbox/grade_2020/data/netcdf_files/Controls/'
ds = xr.open_mfdataset(path_var + 'pr_Control*.nc', chunks={'time': 3000})
dist_nearest = ds['dist_nearest']
count = ds['count']

# nome e posicoes dos pontos
posicoes = {'Sorriso-MT': [-12.5, -55.7],
            'Campinas-SP': [-22.8, -47.0]}

# plotando distancia do pluviometro mais proximo, ao longo do tempo,
# que foi utilizado na interpolacao
_, (ax1, ax2) = plt.subplots(2, 1)
for names, lat_lon in posicoes.items():
    dist_nearest.sel(latitude=lat_lon[0],
                     longitude=lat_lon[1],
                     method='nearest').plot(ax=ax1, label=names)

    # número de estações que contem na célula
    count.sel(latitude=lat_lon[0],
              longitude=lat_lon[1],
              method='nearest').plot(ax=ax2, label=names)

ax1.set_ylim(0, 400)
ax1.legend()
ax1.set_title('')
ax2.set_ylim(-1, 6)
ax2.legend()
ax2.set_title('')
plt.tight_layout()
plt.show()
