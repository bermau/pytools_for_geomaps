"""Tk interface to create maps."""
import tkinter as tk
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from PIL import Image, ImageTk
from map_drawer import Mapper

# fonction qui prend une entrée de texte et la transforme
def transformer_texte(texte):
    return texte.upper()


class LocatorSelectorWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.racine = master
        self.result = None

        self.frame_haut = tk.Frame(self.racine)
        self.frame_haut.pack()

        # créer le widget d'entrée de texte
        self.entree_texte = tk.Entry(self.frame_haut)
        self.entree_texte.pack(side = "left")

        # créer le bouton de validation
        self.bouton_valider = tk.Button(self.frame_haut, text="Valider", command=self.valider_entree)
        self.bouton_valider.pack(side="left")

        # créer la zone de texte pour afficher le résultat
        self.zone_texte = tk.Text(self.racine)
        self.zone_texte.pack()

        # créer le bouton de validation 2
        self.bouton_selection = tk.Button(self.racine, text="Valider", command=self.on_click_selection)
        self.bouton_selection.pack()

        # créer la zone de texte 2 (multilignes)
        self.zone_texte2 = tk.Text(self.racine)
        self.zone_texte2.pack()

        # Créez un bouton pour fermer la fenêtre et renvoyer le résultat
        tk.Button(self, text="Fermer", command=self.fermer_fenetre).pack()

        # raccourcis clavier
        self.entree_texte.bind("<Return>", lambda event: self.bouton_valider.invoke())

    def fermer_fenetre_2 (self):
        # Mettez à jour la variable result avec le résultat de la deuxième fenêtre
        self.result = "Résultat de la deuxième fenêtre"

        # Fermez la fenêtre
        self.destroy()

    # fonction qui est appelée quand on appuie sur le bouton
    def valider_entree(self):
        texte = self.entree_texte.get()
        resultat = transformer_texte(texte)
        self.zone_texte.insert(tk.END, resultat + "\n")

    def on_click_selection(self):
        # récupérer la sélection dans la zone de texte 1
        debut, fin = self.zone_texte.tag_ranges(tk.SEL)
        if debut and fin:
            selection = self.zone_texte.get(debut, fin)
            # afficher la sélection dans la zone de texte 2
            self.zone_texte2.insert(tk.END, selection + "\n")

class MapApp:
    def __init__(self, master):
        self.master = master
        master.title("Mes cartes de géographie")
        self.resultat_deuxieme_fenetre = None

        self.label_country = tk.Label(master, text="Pays :")
        self.label_country.pack()
        self.selected_country = tk.StringVar(value="Angleterre")
        self.option_country = tk.OptionMenu(master, self.selected_country,
                                            "Angleterre", "France", "Espagne")
        self.option_country.pack()

        self.button_map = tk.Button(master, text="Afficher la carte", command=self.display_map)
        self.button_map.pack(side="right")

        self.canvas = tk.Canvas(master, width=800, height=600)
        self.canvas.pack(side="bottom")

        # Créez un bouton pour ouvrir la deuxième fenêtre
        a = tk.Button(self, text="Ajouter un lieu", command=self.ouvrir_fen_deux)
        a.pack()


    def display_map(self):
        country = self.selected_country.get()

        map = Mapper(country, country, None)
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
        fen = LocatorSelectorWindow(self)
        fen.grab_set() # Empêche l'utilisateur d'interagir avec la première fenêtre tant que la deuxième est ouverte
        self.wait_window(fen)  # Attend que la deuxième fenêtre soit fermée
        self.resultat_deuxieme_fenetre = fen.result

root = tk.Tk()
app = MapApp(root)
root.mainloop()
