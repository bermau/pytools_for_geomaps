import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from geopy.geocoders import Nominatim
from pprint import pprint

# créer une carte basée sur les coordonnées de l'Angleterre
m = Basemap(llcrnrlon=-6, llcrnrlat=49, urcrnrlon=2, urcrnrlat=59, resolution='i')

# dessiner les côtes et les frontières
m.drawcoastlines(linewidth=0.5)
m.drawcountries(linewidth=0.5)

# ajouter un titre général à la carte
plt.title("Quelques villes d'Angleterre")

# paramétrer les villes avec un dictionnaire. Par défaut recherche dans OpenStreMap.
# on peut indiquer la position GPS, et la position de l'étiquette.

villes = {
    'Londres': {'label': "S"},
    'Cambridge': {'label': "NE"},
    'Manchester': {'label': "NE"},
    'Liverpool': {'label': "SW"},
    'Birmingham': {'label': "S"},
    # Ajout d'une ville avec des coordonnées GPS (longitude, latitude)
    'Ville Inconnue': {'coord': (-1.2578, 53.5074), 'label': 'E'}
}

# extraire les coordonnées de chaque ville depuis la base de données OpenStreetMap
geolocator = Nominatim(user_agent='my_app')
for ville in villes:
    coordinates = villes[ville].get('coord', None)
    if coordinates is None:
        location = geolocator.geocode(ville + ', UK')
        if location is not None:
            coord = (location.longitude, location.latitude)
            villes[ville]['coord'] = coord

pprint(villes)

# ajouter des marqueurs pour chaque ville avec leur nom
for nom in villes:
    coord = villes[nom]["coord"]
    long, lat = m(coord[0], coord[1])
    m.plot(long, lat, 'ro', markersize=5)
    distance = 0.05 * (m.urcrnry - m.llcrnry)
    pos_label = villes[nom].get('label', 'N')

    positions = {
        'N': (long, lat + distance, 'center', 'bottom'),
        'S': (long, lat - distance, 'center', 'top'),
        'E': (long + distance, lat, 'left', 'center'),
        'W': (long - distance, lat, 'right', 'center'),
        'NE': (long + distance, lat + distance, 'left', 'bottom'),
        'NW': (long - distance, lat + distance, 'right', 'bottom'),
        'SE': (long + distance, lat - distance, 'left', 'top'),
        'SW': (long - distance, lat - distance, 'right', 'top')
    }

    if pos_label in positions:
        position = positions[pos_label]
        plt.text(position[0], position[1], nom, fontsize=10, ha=position[2], va=position[3], color='red')
    else:
        print('Position inconnue')
    # if pos_label == 'N':
    #     plt.text(long, lat + distance, nom, fontsize=10, ha='center', va='bottom', color='red')
    # elif pos_label == 'S':
    #     plt.text(long, lat - distance, nom, fontsize=10, ha='center', va='top', color='red')
    # elif pos_label == 'E':
    #     plt.text(long + distance, lat, nom, fontsize=10, ha='left', va='center', color='red')
    # elif pos_label == 'W':
    #     plt.text(long - distance, lat, nom, fontsize=10, ha='right', va='center', color='red')
    # elif pos_label == 'NE':
    #     plt.text(long + distance, lat + distance, nom, fontsize=10, ha='left', va='bottom', color='red')
    # elif pos_label == 'NW':
    #     plt.text(long - distance, lat + distance, nom, fontsize=10, ha='right', va='bottom', color='red')
    # elif pos_label == 'SE':
    #     plt.text(long + distance, lat - distance, nom, fontsize=10, ha='left', va='top', color='red')
    # elif pos_label == 'SW':
    #     plt.text(long - distance, lat - distance, nom, fontsize=10, ha='right', va='top', color='red')


# afficher la carte
plt.show()
