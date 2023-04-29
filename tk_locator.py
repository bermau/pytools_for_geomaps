"""
Find location of a city using a Tkinter interface.
"""
import tkinter as tk
from find_location import find_location


# fonction qui prend une entrée de texte et la transforme
def find_locations(texte):
    return find_location(texte)


def extract_name_coord(string):
    print(type(string))
    champs_lst = string.split(",")
    return champs_lst[0], champs_lst[-3], champs_lst[-2]


# Volontairement Cette classe ne dérive pas de d'une classe de tk.
# Elle est destinée à être un attribut d'une classe de tk.
class TkGeoLocator:
    """
    Ouvre une fenêtre pour sélectionner un lieu.
    """

    def __init__(self, tk_master):
        self.racine = tk_master
        # self.racine.title("Trouver une ville")
        self.frame = tk.Frame(self.racine)
        self.coord_result = None  # pour renvoyer le résultat

        self.frame_haut = tk.Frame(self.frame, borderwidth=1)
        self.frame_haut.pack()

        # créer le widget d'entrée de texte
        self.entree_texte = tk.Entry(self.frame_haut)
        self.entree_texte.pack(side="left")

        # créer le bouton de validation
        self.bouton_valider = tk.Button(self.frame_haut, text="Valider", command=self.valider_entree)
        self.bouton_valider.pack(side="left")

        # créer la zone de texte pour afficher le résultat
        self.zone_texte = tk.Text(self.frame)
        self.zone_texte.pack()

        # créer le bouton de validation 2
        self.bouton_selection = tk.Button(self.frame, text="Selection", command=self.on_click_selection)
        self.bouton_selection.pack()

        # créer la zone de texte 2 (quelques lignes)
        self.zone_texte2 = tk.Text(self.frame, height=3)
        self.zone_texte2.pack()

        # En dessous un Frame avec 3 champs, puis un bouton choisir
        self.frame_bas = tk.Frame(self.frame, borderwidth=1)
        self.frame_bas.pack()
        self.entry_loc_name = tk.Entry(self.frame_bas)
        self.entry_loc_name.pack(side="left")
        self.entry_loc_lat = tk.Entry(self.frame_bas)
        self.entry_loc_lat.pack(side="left")
        self.entry_loc_long = tk.Entry(self.frame_bas)
        self.entry_loc_long.pack(side="left")
        self.but_choisir = tk.Button(self.frame_bas, text="Choisir", command=self.on_click_choose)
        self.but_choisir.pack(side="left")

        # raccourcis clavier
        self.entree_texte.bind("<Return>", lambda event: self.bouton_valider.invoke())
        self.entree_texte.focus_set()
        self.frame.pack()

    # fonction qui est appelée quand on appuie sur le bouton
    def valider_entree(self):
        """On a saisi Londres"""
        texte = self.entree_texte.get()
        result = find_locations(texte)
        print(result)
        for line in result:
            print(line)
            line2 = ",".join(line)
            self.zone_texte.insert(tk.END, str(line2) + "\n\n")

    def on_click_selection(self):
        """Récupérer la sélection dans la zone de texte 1. On a souligné une ligne.
        On veut extraire nom, latitude et longitude"""
        debut, fin = self.zone_texte.tag_ranges(tk.SEL)
        if debut and fin:
            selection = self.zone_texte.get(debut, fin)
            # afficher la sélection dans la zone de texte 2
            self.zone_texte2.insert(tk.END, selection + "\n")
            triplet = extract_name_coord(selection)
            self.entry_loc_name.insert(0, triplet[0])
            self.entry_loc_lat.insert(0, triplet[1])
            self.entry_loc_long.insert(0, triplet[2])

    def on_click_choose(self):
        """Sortir de la fenêtre en renvoyer les valeurs"""
        print(self.entry_loc_name.get(), self.entry_loc_lat.get(), self.entry_loc_long.get())
        self.coord_result = self.entry_loc_name.get(), self.entry_loc_lat.get(), self.entry_loc_long.get()

        self.racine.destroy()


if __name__ == '__main__':
    # créer la fenêtre principale

    root = tk.Tk()
    root.title("Chercher une localité")
    app = TkGeoLocator(tk_master=root)

    # lancer la boucle principale de l'interface graphique
    root.mainloop()
