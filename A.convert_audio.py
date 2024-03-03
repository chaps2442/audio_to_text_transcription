"""
convert_audio.py - Version 1.0 (2023)
Auteur : Vincent Chapeau

Ce script Python utilise la bibliothèque PyDub pour convertir des fichiers audio dans différents formats en fichiers audio au format WAV. Les formats pris en charge incluent MP3, MP4, M4A, OGG et OPUS. Les fichiers audio sont recherchés dans le dossier spécifié en tant qu'argument en ligne de commande.

Usage :
python convert_audio.py <chemin_du_dossier>

Exemple :
python convert_audio.py /chemin/vers/votre/dossier

Le script parcourt récursivement le dossier spécifié, examine chaque fichier audio avec les extensions .mp3, .mp4, .m4a, .ogg ou .opus, le convertit en format WAV à l'aide de PyDub, et enregistre le résultat avec l'extension .wav ajoutée au nom du fichier d'origine.

Assurez-vous d'avoir la bibliothèque PyDub et les dépendances nécessaires installées. Vous pouvez les installer en utilisant pip avec la commande suivante :
pip install pydub

Le script peut être étendu pour prendre en charge d'autres formats audio en ajoutant leurs extensions à la liste des formats pris en charge.

"""

# Importation des modules et code principal...

import sys
from pydub import AudioSegment
import os

def convert_to_wav(folder_path, log_file_path):
    num_folders = 0
    num_converted = 0
    num_errors = 0

    with open(log_file_path, 'w') as log_file:
        for subdir, dirs, files in sorted(os.walk(folder_path)):
            dirs.sort()  # Trier les sous-dossiers
            num_folders += 1
            for file in sorted(files):  # Trier les fichiers
                if file.lower().endswith((".mp3", ".mp4", ".m4a", ".ogg", ".opus", ".avi", ".mov", ".flac", ".aac", ".wma", ".flv", ".webm")):
                    filepath = os.path.join(subdir, file)
                    wav_path = os.path.splitext(filepath)[0] + '.wav'
                    if not os.path.exists(wav_path):
                        try:
                            audio = AudioSegment.from_file(filepath)
                            audio.export(wav_path, format='wav')
                            message = f"Converted: {wav_path}"
                            print(message)
                            log_file.write(message + "\n")
                            num_converted += 1
                        except Exception as e:
                            message = f"Erreur lors de la conversion de {filepath}: {e}"
                            print(message)
                            log_file.write(message + "\n")
                            num_errors += 1
                    else:
                        message = f"Ignored (already exists): {wav_path}"
                        print(message)
                        log_file.write(message + "\n")
                else:
                    message = f"Ignored (not a target format): {file}"
                    print(message)
                    log_file.write(message + "\n")

        # Écrire le résumé à la fin
        summary = f"\nRésumé:\nNombre de dossiers parcourus: {num_folders}\nNombre de conversions: {num_converted}\nErreurs: {num_errors}\n"
        print(summary)
        log_file.write(summary)

if len(sys.argv) != 2:
    print("Usage: python convert_audio.py <chemin_du_dossier>")
    sys.exit(1)

folder_path = sys.argv[1]
log_file_path = os.path.join(folder_path, "conversion_log.txt")
convert_to_wav(folder_path, log_file_path)
