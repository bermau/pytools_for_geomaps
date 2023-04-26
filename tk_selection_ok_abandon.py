import tkinter as tk

# fonction qui est appelée quand on appuie sur le bouton "Valider"
def valider_selection():
    # récupérer la sélection dans la zone de texte 1
    debut, fin = zone_texte1.tag_ranges(tk.SEL)
    if debut and fin:
        selection = zone_texte1.get(debut, fin)
        # afficher la sélection dans la zone de texte 2
        zone_texte2.insert(tk.END, selection + "\n")

# créer la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Mon programme avec Tkinter")

# créer la zone de texte 1 (multilignes)
zone_texte1 = tk.Text(fenetre)
zone_texte1.pack()

# créer le bouton "Valider"
bouton_valider = tk.Button(fenetre, text="Valider", command=valider_selection)
bouton_valider.pack()

# créer la zone de texte 2 (multilignes)
zone_texte2 = tk.Text(fenetre)
zone_texte2.pack()

# lancer la boucle principale de l'interface graphique
fenetre.mainloop()
