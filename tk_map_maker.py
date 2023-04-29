"""Tk interface to create maps."""
import tkinter as tk
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image, ImageTk
from map_maker import Mapper  # , geocode_cache
from tk_locator import TkGeoLocator

villes = {
    'Londres': {'label': "NE"},
    # 'Cambridge': {'label': "NE"},
    # 'Manchester': {'label': "NE"},
    'Blenheim Palace': {'label': "SW"},
    'Chartwell': {'label': "SW"},
    # 'Birmingham': {'label': "S"},
    # Ajout d'une ville avec des coordonnées GPS (latitude, longitude)
    'Ville quelconque': {'coord': (53.5074, -1.2578), 'label': 'E'},
}


def ajouter_ville(triplet):
    """
    Add a city and its location in the dictionary
    :param triplet: (name, latitude, longitude)
    :return: None
    """
    name, latitude, longitude = triplet
    villes[name] = {'coord' : (float(latitude), float(longitude))}
    print(f"Villes devient {villes}")

# J'utilise une classe qui ne dérive pas d'une classe de tkinter.
# https://stackoverflow.com/questions/16115378/tkinter-example-code-for-multiple-windows-why-wont-buttons-load-correctly
class MapApp:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.master.title("Mes jolies cartes de géographie")
        self.resultat_deuxieme_fenetre = None
        # Country selector
        self.label_country = tk.Label(self.frame, text="Pays :")
        self.label_country.pack()
        self.selected_country = tk.StringVar(value="Angleterre")
        self.option_country = tk.OptionMenu(self.frame, self.selected_country,
                                            "Angleterre", "France", "Espagne")
        self.option_country.pack()

        self.button_map = tk.Button(self.frame, text="Afficher la carte", command=self.display_map)
        self.button_map.pack(side="right")

        self.canvas = tk.Canvas(self.frame, width=800, height=600)
        self.canvas.pack(side="bottom")

        # Créer un bouton pour ouvrir une fenêtre pour choisir un lieu à ajouter.
        self.frame_bas = tk.Frame(self.frame)
        self.frame_bas.pack()
        self.button_locator = tk.Button(self.frame_bas, text="Ajouter un lieu", command=self.ouvrir_fen_deux)
        self.button_locator.pack(side="right")
        self.frame.pack()

    def display_map(self):
        """Affiche la carte avec les villes"""
        country = self.selected_country.get()

        map = Mapper(country, country, points=villes)
        map.creer_carte()
        map.dessine_villes()
        map.save_svg()

        drawing = svg2rlg("./maps/tempo.svg")
        renderPM.drawToFile(drawing, "./maps/temp.png", fmt="PNG")

        img = Image.open("./maps/temp.png")
        photo = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor="nw", image=photo)
        self.canvas.image = photo

    def ouvrir_fen_deux(self):
        """Ouvre une seconde fenêtre pour choisir un lieu"""
        win2 = tk.Toplevel(self.master) # j'indique self.master et non pas self, qui n'est pas tk, mais son père.
        fen2 = TkGeoLocator(win2)

        fen2.frame.grab_set()  # le frame de cette fenêtre récupère tous les signaux
        self.frame.wait_window(fen2.frame)  # Attend que la deuxième fenêtre soit fermée (important :
        # Found my solution reading :
        # https://stackoverflow.com/questions/48292632/how-to-correctly-implement-wait-window

        self.resultat_deuxieme_fenetre = fen2.coord_result
        if self.resultat_deuxieme_fenetre:
            print(f"Il faut ajouter la ville : {self.resultat_deuxieme_fenetre}")
            ajouter_ville(self.resultat_deuxieme_fenetre)
        else:
            print(f"Rien de neuf !")


if __name__ == '__main__':
    root = tk.Tk()
    app = MapApp(root)
    root.mainloop()
