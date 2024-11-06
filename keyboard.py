import tkinter as tk
from tkinter import messagebox
import wave
import numpy as np
import os
import platform

notes = ["DO", "RE", "MI", "FA", "SOL", "LA", "SI"]
semi_notes = ["DO#\nREb", "RE#\nMIb", "FA#\nSOLb", "SOL#\nLAb", "LA#\nSIb"]
l_notes = []

frequencies = {"DO": 261.63, "DO#\nREb": 277.18, "RE": 293.66, "RE#\nMIb": 311.13, "MI": 329.63, "FA": 349.23, "FA#\nSOLb": 369.99, "SOL": 392.00,
              "SOL#\nLAb": 415.30, "LA": 440.00, "LA#\nSIb": 466.16, "SI": 493.88}

octaves = 2
d_tecles_negres = 0

#Creem la finestra
window = tk.Tk()
window.title("Contrapunt a partir de un Cantus Firmus")
window.geometry("1200x800")

#Creem un canvas
canvas = tk.Canvas(window, width=0, height=0)
canvas.pack()

#Esborrar la llista de notes
def remove_notes():
    l_notes.clear()

#Afegim les notes a la llista buida
def get_notes(nota):
    l_notes.append(nota)

#Fem que soni la llista
def wav_list():

    if len(l_notes) == 0:

        popup = tk.Toplevel(window)
        popup.title("ERROR")
        popup.geometry("300x150")

        # Afegir una etiqueta al pop-up
        etiqueta = tk.Label(popup, text="Introdueix unes quantes notes per escoltar el teu Cantus")
        etiqueta.pack(pady=10)

        # Afegir un botón per tancar la finestra
        boton_cerrar = tk.Button(popup, text="Tancar", command=popup.destroy)
        boton_cerrar.pack(pady=5)

    else:
        note_frequencies = [frequencies[note] for note in l_notes if note in frequencies]

        fs = 44100 
        duration = 2.0  # Durada en segons

        full_wave_data = np.array([], dtype=np.int16)

        for frequency in note_frequencies:
            t = np.linspace(0, duration, int(fs * duration), endpoint=False)
            wave_data = (0.5 * 32767 * np.sin(2 * np.pi * frequency * t)).astype(np.int16)
            full_wave_data = np.concatenate((full_wave_data, wave_data))

        with wave.open("cantus.wav", "wb") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(fs)
            f.writeframes(full_wave_data.tobytes())

        #Portabilitat
        if platform.system() == "Windows":
            os.system("start cantus.wav")
        elif platform.system() == "Darwin":  # MacOS
            os.system("open cantus.wav")
        elif platform.system() == "Linux":
            os.system("xdg-open cantus.wav")

#Botó per esborrar les notes
remove_button = tk.Button(window, text = "Esborra el teu cantus", command=remove_notes)
remove_button.pack(padx=10, pady=0, side=tk.LEFT)

#Botó per fer play
play_button = tk.Button(window, text=".wav amb el Cantus Firmus", command=wav_list)
play_button.pack(padx=10, pady=0, side=tk.LEFT)

#Creem les tecles blanques d'un piano
for i in range(octaves):
    for nota in notes:
        button = tk.Button(canvas, text=nota, pady=30, height=20, width=8, command=lambda nota=nota: get_notes(nota))
        button.pack(pady=20, side=tk.LEFT)

#Creem les tecles negres d'un piano
for z in range(octaves):
    for semi_nota in semi_notes:
            
            if semi_nota != semi_notes[1] and semi_nota != semi_notes[4]:
                black_button = tk.Button(canvas, text=semi_nota, height=50, width=20, bg="black", fg="white", 
                                         command=lambda nota=semi_nota: get_notes(nota))
                black_button.place(x = 50 + d_tecles_negres, y = 20, width = 38, height = 200)
                d_tecles_negres = d_tecles_negres + 67

            #Espai entre Mi i Fa / Si i Do
            else:
                black_button = tk.Button(canvas, text=semi_nota, height=50, width=20, bg="black", fg="white", 
                                         command=lambda nota=semi_nota: get_notes(nota))
                black_button.place(x = 50 + d_tecles_negres, y = 20, width = 38, height = 200)
                d_tecles_negres = d_tecles_negres + 130

window.mainloop()