import tkinter as tk
from tkinter import messagebox

import keyboard

import keyboard

#Creem la finestra
window = tk.Tk()
window.title("Menu")
window.geometry("1200x800")

#Funció per sortir de la finestra
def sortir():
    #Messagebox per confirmar que surti
    exit = messagebox.askyesno(title="Sortir", message="Està segur que vol sortir?")

    if exit == True:
        window.destroy()

#Creem el botó per sortir
quit_button = tk.Button(window, text="Sortir", command=sortir)
quit_button.pack(padx = 10, pady = 0, side = tk.LEFT)

#Creem el botó per anar a la finestra del contrapunt 1:!
contrapunt_1 = tk.Button(window, text = "Contrapunt 1:1", command = keyboard.teclat)
contrapunt_1.pack(padx  =10, pady = 0, side = tk.LEFT)

window.mainloop()