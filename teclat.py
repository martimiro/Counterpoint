import tkinter as tk

notes = ["DO", "RE", "MI", "FA", "SOL", "LA", "SI"]
semi_notes = ["DO#\nREb", "RE#\nMIb", "FA#\nSOLb", "SOL#\nLAb", "LA#\nSIb"]

l_notes = []

octaves = 2
d_tecles_negres = 0

#Creen la finestra
window = tk.Tk()
window.title("Contrapunt a partir de un Cantus Firmus")
window.geometry("1500x800")

#Creem un canvas
canvas = tk.Canvas(window, width=1500, height=800)
canvas.pack()

#Create a label
main_label = tk.Label(window, text="Teclat piano", font=("Arial", 20))
main_label.pack(pady=20)

#Creem les tecles blanques d'un piano
for num in range(octaves):
    for nota in notes:
        button = tk.Button(canvas, text=nota, height=20, width=5)
        button.pack(pady=20, side=tk.LEFT)

#Creem les tecles negres d'un piano
for num in range(octaves):
    for semi_nota in semi_notes:
            black_button = tk.Button(canvas, text=semi_nota, height=50, width=3, bg="black", fg="white")
            black_button.place(x=50 + d_tecles_negres, y=100, width=30, height=120)
            d_tecles_negres =+ 70

window.mainloop()