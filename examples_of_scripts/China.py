from pygeomap_src.map_maker import Mapper
import matplotlib.pyplot as plt

from pygeomap_src.map_maker import villes_examples


map = Mapper(country='China', title="La chine", points=None)

map.creer_carte()
#
# map.ajout_regions([('nom', 'Occitanie', 'red', 0.5), ('code_insee', '93', '#FF8957', 0.6)])
# # '#FF8957'
# map.dessine_villes()

# afficher la carte d'Angleterre
plt.show()




