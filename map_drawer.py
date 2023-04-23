import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from geopy.geocoders import Nominatim
from pprint import pprint


class MyMapper:

    def __init__(self, country, title, points):
        self.map = None
        self.country = country
        self.title = title
        self.villes = points

    def creer_carte(self):
        # créer une carte basée sur les coordonnées du pays
        # J'ai ajouté deux nouveaux paramètres à la fonction Basemap pour spécifier la projection de la carte (
        # projection='merc') et les coordonnées du centre de la carte (lat_0 = 54.5, lon_0 = -4.36). Ces paramètres
        # permettent d'ajuster la projection de la carte pour mieux s'adapter aux dimensions de l'Angleterre et
        # éviter que le nord ne soit écrasé. Notez que j'ai également retiré le paramètre resolution='h' car il peut
        # provoquer des erreurs avec la projection mercator.

        if self.country in ["Angleterre", 'en']:
            self.map = Basemap(llcrnrlon=-6, llcrnrlat=49, urcrnrlon=2, urcrnrlat=59, resolution='i', projection='merc',
                               lat_0=54.5, lon_0=-4.36)
        elif self.country in ["France", 'fr']:
            self.map = Basemap(llcrnrlon=-5, llcrnrlat=41, urcrnrlon=10, urcrnrlat=51, resolution='i',
                               projection='merc',
                               lat_0=46, lon_0=2)
        elif self.country in ["Espagne", 'sp']:
            self.map = Basemap(llcrnrlon=-10, llcrnrlat=34, urcrnrlon=4, urcrnrlat=44, resolution='i',
                               projection='merc',
                               lat_0=39, lon_0=-3)

        # dessiner les côtes et les frontières
        self.map.drawcoastlines(linewidth=0.5)
        self.map.drawcountries(linewidth=0.5)
        self.map.drawrivers(color='b')

        # ajouter un titre général à la carte
        plt.title(self.title)
        plt.savefig(f"./maps/{self.country}.svg")

    def dessine_villes(self):
        """Affiche les villes et leur label"""
        self.creer_carte()
        # extraire les coordonnées de chaque ville depuis la base de données OpenStreetMap
        geolocator = Nominatim(user_agent='my_app')
        for ville in self.villes:
            coordinates = self.villes[ville].get('coord', None)
            if coordinates is None:
                location = geolocator.geocode(ville + ', UK')
                if location is not None:
                    coord = (location.longitude, location.latitude)
                    self.villes[ville]['coord'] = coord
        pprint(self.villes)
        # ajouter des marqueurs pour chaque ville avec leur nom
        for nom in self.villes:
            coord = self.villes[nom]["coord"]
            long, lat = self.map(coord[0], coord[1])
            self.map.plot(long, lat, 'ro', markersize=5)
            distance = 0.05 * (self.map.urcrnry - self.map.llcrnry)
            pos_label = self.villes[nom].get('label', 'N')

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


if __name__ == '__main__':
    # On paramétre les villes avec un dictionnaire. Par défaut recherche dans OpenStreetMap.
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

    map = MyMapper(country='fr', title="Quelques villes d'Angleterre", points=villes)
    map.creer_carte()
    map.dessine_villes()

    # afficher la carte
    plt.show()
