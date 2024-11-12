import subprocess
from music21 import stream, note, environment

# Crear un entorno para configurar el programa de visualización (MuseScore)
env = environment.Environment()

# Establecer el ejecutable de MuseScore (ajusta la ruta si es necesario)
env['musescoreDirectPNGPath'] = 'C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe'  # Asegúrate de que esta ruta sea correcta

# Crear una secuencia de notas
score = stream.Score()
part = stream.Part()
part.append(note.Note('C4', quarterLength=1))
part.append(note.Note('D4', quarterLength=1))
part.append(note.Note('E4', quarterLength=1))
score.append(part)

# Guardar la partitura como MusicXML
score.write('musicxml', fp='output.xml')

# Usar MuseScore para convertir el archivo MusicXML a PDF
# Ejecutar el comando MuseScore desde Python
subprocess.run(['C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe', 'output.xml', '-o', 'output.pdf'])