"""
Structure pour Application tk avec une sous-fenêtre.
Noter qu'ici les classes ne dérivent pas de classes de tk.
"""
# Exemple de https://stackoverflow.com/questions/17466561/what-is-the-best-way-to-structure-a-tkinter-application
# /17470842#17470842/
import tkinter as tk


class Demo1:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame, text='New Window', width=25, command=self.new_window)
        self.button1.pack()
        self.frame.pack()

    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo2(self.newWindow)


class Demo2:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text='Quit', width=25, command=self.close_windows)
        self.quitButton.pack()
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()


def main():
    root = tk.Tk()
    app = Demo1(root)
    root.mainloop()


if __name__ == '__main__':
    main()
