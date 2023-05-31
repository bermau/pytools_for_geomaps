from pygeomap_src.map_maker import Mapper
import matplotlib.pyplot as plt

from pygeomap_src.map_maker import villes_examples

villes_chine = {
    'Pekin': {},
    'Canton': {'coord': (23.1301964, 113.2592945)},
    'Yumen': {},
    'Ville quelconque': {'coord': (53.5074, -1.2578), 'label': 'E'},
}

map = Mapper(country='China', title="La chine", points=villes_chine, etopo=True)

map.creer_carte()
#

# map.ajout_regions([('nom', 'Occitanie', 'red', 0.5), ('code_insee', '93', '#FF8957', 0.6)])
# # '#FF8957'
map.dessine_villes()

# afficher la carte d'Angleterre
plt.show()




