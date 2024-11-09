import abjad

# Crear una secuencia de notas
notas = "c'4 d'4 e'4 f'4 g'4"

# Convertir la secuencia de notas en una selección de contenedores de Abjad
voice = abjad.Voice(notas)

# Crear un pentagrama y añadir la voz de notas
staff = abjad.Staff([voice])

# Crear una partitura y añadir el pentagrama
score = abjad.Score([staff])

# Crear la partitura en formato LilyPond y guardarla como un archivo PDF
abjad.show(score)