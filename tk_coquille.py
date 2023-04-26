import tkinter as tk


# fonction qui prend une entrée de texte et la transforme
def transformer_texte(texte):
    return texte.upper()


class Application(tk.Frame):
    def __init__(self, master=None):
        # tk.Frame.__init__(self, racine)
        super().__init__(master)
        self.racine = master

        # créer le widget d'entrée de texte
        self.entree_texte = tk.Entry(self.racine)
        self.entree_texte.pack()

        # créer le bouton de validation
        self.bouton_valider = tk.Button(self.racine, text="Valider", command=self.valider_entree)
        self.bouton_valider.pack()

        # créer la zone de texte pour afficher le résultat
        self.zone_texte = tk.Text(self.racine)
        self.zone_texte.pack()

        # créer le bouton de validation 2
        self.bouton_selection = tk.Button(self.racine, text="Valider", command=self.on_click_selection)
        self.bouton_selection.pack()

        # créer la zone de texte 2 (multilignes)
        self.zone_texte2 = tk.Text(self.racine)
        self.zone_texte2.pack()

        # raccourcis clavier
        self.entree_texte.bind("<Return>", lambda event: self.bouton_valider.invoke())

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


if __name__ == '__main__':
    # créer la fenêtre principale

    root = tk.Tk()
    root.title("Mon programme avec Tkinter")
    app = Application(master = root)

    # lancer la boucle principale de l'interface graphique
    root.mainloop()
