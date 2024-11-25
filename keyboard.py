import tkinter as tk
import wave
import numpy as np
import os
import platform
import subprocess
from music21 import stream, note, environment, metadata

notes = ["DO", "RE", "MI", "FA", "SOL", "LA", "SI"]
semi_notes = ["DO#\nREb", "RE#\nMIb", "FA#\nSOLb", "SOL#\nLAb", "LA#\nSIb"]
l_notes = []

frequencies = {
    "DO": 261.626, "DO#\nREb": 277.183, "RE": 293.665, "RE#\nMIb": 311.127, "MI": 329.628, "FA": 349.228, "FA#\nSOLb": 369.994, 
    "SOL": 391.995, "SOL#\nLAb": 415.305, "LA": 440, "LA#\nSIb": 466.164, "SI": 493.883
}

note_mapping = {
    "DO": "C", "RE": "D", "MI": "E", "FA": "F", "SOL": "G", "LA": "A", "SI": "B", "DO#\nREb": "C#", "RE#\nMIb": "D#", "FA#\nSOLb": "F#",
    "SOL#\nLAb": "G#", "LA#\nSIb": "A#"
}

octaves = 2
d_tecles_negres = 0

#Creem la finestra
window = tk.Tk()
window.title("Contrapunt a partir de un Cantus Firmus")
window.geometry("1200x800")

#Creem un canvas
canvas = tk.Canvas(window, width=0, height=0)
canvas.pack()

def crear_partitura():
    if len(l_notes) == 0:
        popup = tk.Toplevel(window)
        popup.title("ERROR")
        popup.geometry("300x150")

        # Afegir una etiqueta al pop-up
        etiqueta = tk.Label(popup, text="Introdueix unes quantes notes per veure el teu .pdf")
        etiqueta.pack(pady=10)

        # Afegir un botón per tancar la finestra
        close_button = tk.Button(popup, text="Tancar", command=popup.destroy)
        close_button.pack(pady=5)

    else:
        # Creem un entorn per configurar Musescore
        env = environment.Environment()
        env['musescoreDirectPNGPath'] = 'C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe'

        score = stream.Score()
        part = stream.Part()
        measure = stream.Measure()
        metadata = metadata.Metadata()

        measure.append(note.Note())
        part.append(measure)
        score.insert(0, metadata.Metadata())
        score.metadata.title = "Contrapunt 1:1"
        score.show()

        for note_tup in l_notes:
            note_name = note_tup[0]
            if note_name in note_mapping:
                note_name = note_mapping[note_name]  # Mapea el nombre de la nota
                part.append(note.Note(note_name, quarterLength=4))
        score.append(part)

        # Guardem la partitura com MusicXML
        score.write('musicxml', fp='cantus.xml')

        # Fem servir Musescore4 per passar de .xml a .pdf
        subprocess.run(['C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe', 'cantus.xml', '-o', 'cantus.pdf'])

#Esborrar la llista de notes
def remove_notes():
    l_notes.clear()

#Afegim les notes a la llista buida
def get_notes(nota, octave = 1):
    if octave == 2 and nota in frequencies:
        l_notes.append((nota, frequencies[nota] * 2))
    else:
        l_notes.append((nota, frequencies[nota]))

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
        close_button = tk.Button(popup, text="Tancar", command=popup.destroy)
        close_button.pack(pady=5)

    else:
        note_frequencies = [frequency for _, frequency in l_notes] # s'assigna a frequency i es recull a la nova llista
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

#Botó per generar partitures
partitura_button = tk.Button(window, text = ".pdf amb la teva partitura", command=crear_partitura)
partitura_button.pack(padx=10, pady=0, side=tk.LEFT)

#Creem les tecles blanques d'un piano
for i in range(octaves):
    for nota in notes:
        octave = i + 1
        button = tk.Button(canvas, text=nota, pady=30, height=20, width=8, command=lambda nota=nota, octave=octave: get_notes(nota, octave))                  
        button.pack(pady=20, side=tk.LEFT)

#Creem les tecles negres d'un piano
for z in range(octaves):
        octave = z + 1

        for semi_nota in semi_notes:
            if semi_nota != semi_notes[1] and semi_nota != semi_notes[4]:
                black_button = tk.Button(canvas, text=semi_nota, height=50, width=20, bg="black", fg="white", command=lambda nota=semi_nota, octave=octave: get_notes(nota, octave))
                black_button.place(x = 50 + d_tecles_negres, y = 20, width = 38, height = 200)
                d_tecles_negres = d_tecles_negres + 67

            #Espai entre Mi i Fa / Si i Do
            else:
                black_button = tk.Button(canvas, text=semi_nota, height=50, width=20, bg="black", fg="white", 
                        command=lambda nota=semi_nota, octave=octave: get_notes(nota, octave))
                black_button.place(x = 50 + d_tecles_negres, y = 20, width = 38, height = 200)
                d_tecles_negres = d_tecles_negres + 130

window.mainloop()