"""Tk interface to create maps."""
import tkinter as tk
# import requests
from io import BytesIO

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from PIL import Image, ImageTk
from map_drawer import Mapper


class MapApp:
    def __init__(self, master):
        self.master = master
        master.title("Mes cartes de géographie")

        self.label_country = tk.Label(master, text="Pays :")
        self.label_country.pack()
        self.selected_country = tk.StringVar(value="Angleterre")
        self.option_country = tk.OptionMenu(master, self.selected_country, "Angleterre", "France", "Espagne")
        self.option_country.pack()

        self.button_map = tk.Button(master, text="Afficher la carte", command=self.display_map)
        self.button_map.pack()

        self.canvas = tk.Canvas(master, width=800, height=600)
        self.canvas.pack()

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


root = tk.Tk()
app = MapApp(root)
root.mainloop()
