"""
Tool to explore a SHP file
"""

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd

map = Basemap(llcrnrlon=-5, llcrnrlat=42, urcrnrlon=10, urcrnrlat=51, resolution='i',
              projection='merc',
              lat_0=46, lon_0=2)

map.drawmapboundary()

# Ajouter les limites administratives de la région Auvergne
file = '../data/regions_france/regions-20180101-shp/regions-20180101'
map.readshapefile(file, 'french_regions',
                  # linewidth=1.5,
                  color='black',
                  drawbounds=False)

# plt.show()
def get_codes_de_regions(shape_infos, code = 'nom'):
    noms_regions = []
    for shp_line in shape_infos:
        noms_regions.append(shp_line[code])
    return set(noms_regions)


def describe_shp_info(shape_infos):
    print(shape_infos[0])

describe_shp_info(map.french_regions_info)
print(get_codes_de_regions(map.french_regions_info))
print(get_codes_de_regions(map.french_regions_info, 'SHAPENUM'))

# Constituer un DataFrame
shp_df= pd.DataFrame(map.french_regions_info)
grp = shp_df.groupby(by=['nom', 'RINGNUM'])
# afficher les noms de régions
print("Pour région Auvergne-Rhône-Alpes ")

print(grp.agg(sum))
# shp_df = pd.DataFrame()
# Accéder à une seule ligne .
print(grp.get_group(("Auvergne-Rhône-Alpes", 1)))
