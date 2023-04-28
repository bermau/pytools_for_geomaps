"""Une fenêtre en ouvre une seconde"""

import tkinter as tk


class PremiereFenetre(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.root = master
        self.resultat_deuxieme_fenetre = None

        # Ajoutez ici les widgets que vous souhaitez dans votre première fenêtre

        # Créez un bouton pour ouvrir la deuxième fenêtre
        tk.Button(self, text="Ouvrir la deuxième fenêtre", command=self.ouvrir_deuxieme_fenetre).pack()
        self.pack()

    def ouvrir_deuxieme_fenetre(self):
        fenetre = DeuxiemeFenetre(self)
        fenetre.grab_set()  # Empêche l'utilisateur d'interagir avec la première fenêtre quand la seconde est ouverte
        self.wait_window(fenetre)  # Attend que la deuxième fenêtre soit fermée
        self.resultat_deuxieme_fenetre = fenetre.result
        print(f"La fenêtre a reçu {self.resultat_deuxieme_fenetre}")


class DeuxiemeFenetre(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.result = None

        # Ajoutez ici les widgets que vous souhaitez dans votre deuxième fenêtre

        # Créez un bouton pour fermer la fenêtre et renvoyer le résultat
        tk.Button(self, text="Fermer", command=self.fermer_fenetre).pack()

    def fermer_fenetre(self):
        # Mettez à jour la variable result avec le résultat de la deuxième fenêtre
        self.result = "Résultat de la deuxième fenêtre"

        # Fermez la fenêtre
        self.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    fenetre1 = PremiereFenetre(root)
    root.mainloop()
