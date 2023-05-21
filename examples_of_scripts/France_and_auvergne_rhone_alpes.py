from pygeomap_src.map_maker import Mapper
import matplotlib.pyplot as plt

from pygeomap_src.map_maker import villes_examples


map = Mapper(country='fr', title="France", points=villes_examples)

map.creer_carte()
map.ajout_regions(('nom', 'Occitanie'))
map.dessine_villes()

# afficher la carte d'Angleterre
plt.show()




