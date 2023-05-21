import os.path
import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from geopy.geocoders import Nominatim

from tools.explore_shp_file import describe_shp_info

from pprint import pprint

# Création d'un cache pour stocker les résultats géocodés
# geocode_cache = {}

# Initialisation du géocodeur
geolocator = Nominatim(user_agent="my_app")

# A propos des coordonnées : il est préférable d'utiliser l'ordre (latitude, longitude). C'est l'ordre généralement
# utilisé dans les systèmes de navigation GPS et dans les outils de cartographie. Fonction pour récupérer les
# coordonnées d'une ville en utilisant le cache. Attention au fait que plot de matplolib attend par défaut l'ordre
# inverse.
def get_coordinates(city ):
    if city in geocode_cache:
        # Récupérer les coordonnées à partir du cache
        return geocode_cache[city]
    else:
        # Géolocaliser la ville
        location = geolocator.geocode(city)
        if location is not None:
            # Enregistrer les coordonnées dans le cache
            geocode_cache[city] = (location.latitude, location.longitude)
            return geocode_cache[city]
        else:
            return None


# Enregistrer le cache dans un fichier
def save_geocache(fname='geo_cache.pickle'):
    with open(fname, 'wb') as f:
        pickle.dump(geocode_cache, f, pickle.HIGHEST_PROTOCOL)


def load_geocache(fname='geo_cache.pickle'):
    with open(fname, 'rb') as f:
        pick = pickle.load(f)
    return pick


class Mapper:

    def __init__(self, country, title, points, etopo=False):
        self.map = None
        self.country = country
        self.title = title
        self.villes = points
        self.etopo = etopo

    def creer_carte(self):
        # Créer une carte basée sur les coordonnées du pays.
        # J'ai ajouté deux nouveaux paramètres à la fonction Basemap pour spécifier la projection de la carte (
        # projection='merc') et les coordonnées du centre de la carte (lat_0 = 54.5, lon_0 = -4.36). Ces paramètres
        # permettent d'ajuster la projection de la carte pour mieux s'adapter aux dimensions de l'Angleterre et
        # éviter que le nord ne soit écrasé. Notez que j'ai également retiré le paramètre resolution='h' car il peut
        # provoquer des erreurs avec la projection mercator.
        plt.clf()
        if self.country in ["Angleterre", 'en']:
            self.map = Basemap(llcrnrlon=-8, llcrnrlat=49, urcrnrlon=2, urcrnrlat=59, resolution='i', projection='merc',
                               lat_0=54.5, lon_0=-4.36)
        elif self.country in ["France", 'fr']:
            self.map = Basemap(llcrnrlon=-5, llcrnrlat=42, urcrnrlon=10, urcrnrlat=51, resolution='i',
                               projection='merc',
                               lat_0=46, lon_0=2)
        elif self.country in ["Espagne", 'sp']:
            self.map = Basemap(llcrnrlon=-10, llcrnrlat=34, urcrnrlon=4, urcrnrlat=44, resolution='i',
                               projection='merc',
                               lat_0=39, lon_0=-3)

        # dessiner les côtes et les frontières
        self.map.drawcoastlines()  # tester option : linewidth=0.5
        self.map.drawcountries()
        self.map.drawrivers(color='b')
        # Autres à tester :
        # self.map.drawmapboundary(fill_color='pink')
        # self.map.fillcontinents(color='#ddaa66',lake_color='aqua')

        if self.country in ["France", 'fr']:
            # Ajouter les limites administratives de la région Auvergne
            file = os.path.abspath('../data/regions_france/regions-20180101-shp/regions-20180101')
            self.map.readshapefile(file, 'french_regions', linewidth=1.5, color='black', drawbounds = False)

            for info, shape in zip(self.map.french_regions_info, self.map.french_regions):
                if info['SHAPENUM'] == 18:
                    x, y = zip(*shape)
                    self.map.plot(x, y, marker=None, color='blue')

        # Ajouter le relief
        if self.etopo:
            self.map.etopo()

        # ajouter un titre général à la carte
        plt.title(self.title)


    def dessine_villes(self):
        """Affiche les villes et leur label"""
        # extraire les coordonnées de chaque ville depuis la base de données OpenStreetMap

        if self.villes:
            for nom_ville in self.villes:
                coordinates = self.villes[nom_ville].get('coord', None)
                if coordinates is None:
                    location = get_coordinates(nom_ville + ', UK')
                    if location is not None:
                        coord = (location[0], location[1])
                        self.villes[nom_ville]['coord'] = coord

            # ajouter des marqueurs pour chaque ville avec leur nom
            for nom_ville in self.villes:
                coord = self.villes[nom_ville]["coord"]
                print(f"coord vaut {coord}")
                long, lat = self.map(coord[1], coord[0])

                # Attention : plot attend x puis y (soit longitude puis latitude).
                self.map.plot(long, lat,  'ro', markersize=5)
                distance = 0.05 * (self.map.urcrnry - self.map.llcrnry)
                pos_label = self.villes[nom_ville].get('label', 'N')

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
                    plt.text(position[0], position[1], nom_ville, fontsize=10, ha=position[2], va=position[3], color='red')
                else:
                    print('Position inconnue')

    def save_svg(self):
        plt.savefig("../maps/tempo.svg")
        plt.savefig(f"../maps/{self.country}.svg")

cache_name = '../maps/geo_cache.pickle'
try:
    geocode_cache = load_geocache(cache_name)
    print("J'ai chargé le cache des données géographiques.")
except:
    print(f"Pas de fichier {cache_name}")
    geocode_cache = {}

villes_examples = {
        'Londres': {'label': "NE"},
        # 'Cambridge': {'label': "NE"},
        # 'Manchester': {'label': "NE"},
        'Blenheim Palace': {'label': "SW"},
        'Chartwell': {'label': "SW"},

        # 'Birmingham': {'label': "S"},
        # Ajout d'une ville avec des coordonnées GPS (latitude, longitude)
        'Ville quelconque': {'coord': (53.5074, -1.2578), 'label': 'E'},
    }

if __name__ == '__main__':
    # On paramètre les villes avec un dictionnaire. Par défaut recherche dans OpenStreetMap.
    # On peut indiquer la position GPS, et la position de l'étiquette.



    print(f"geocode_cache = {geocode_cache}")

    # map = Mapper(country='en', title="Quelques villes d'Angleterre concernant W.S. Churchill", points=villes)
    map = Mapper(country='fr', title="France", points=villes_examples)
    map.creer_carte()
    map.dessine_villes()

    # afficher la carte d'Angleterre
    plt.show()

