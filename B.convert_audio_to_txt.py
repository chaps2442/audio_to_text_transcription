"""
convert_audio_to_txt.py - Version 1.0 (2023)
Auteur : Vincent Chapeau

Ce script Python utilise la bibliothèque PyDub et la bibliothèque SpeechRecognition (speech_recognition) pour convertir des fichiers audio au format MP3 en fichiers audio WAV, puis pour transcrire le contenu audio en texte. Les fichiers MP3 sont recherchés dans le dossier spécifié en tant qu'argument en ligne de commande.

Usage :
python convert_audio_to_txt.py <chemin_du_dossier>

Exemple :
python convert_audio_to_txt.py /chemin/vers/votre/dossier

Le script parcourt récursivement le dossier spécifié, examine chaque fichier au format MP3, le convertit en WAV si nécessaire, effectue la transcription en utilisant la reconnaissance vocale de Google (fr-FR), et enregistre le résultat dans des fichiers texte au format .txt. Les fichiers de transcription sont enregistrés avec le même nom de base que les fichiers audio d'origine, mais avec l'extension .txt ajoutée.

text = r.recognize_google(audio_data, language='es')  # Transcription en espagnol
    Pour l'arabe : language='ar'
    Pour l'albanais : language='sq'
    Pour le bulgare : language='bg'
    Pour le hongrois : language='hu'
    Pour l'espagnol : language='es'

Assurez-vous d'avoir les bibliothèques PyDub et SpeechRecognition installées. Vous pouvez les installer en utilisant pip avec les commandes suivantes :
pip install pydub
pip install SpeechRecognition

"""

# Importation des modules et code principal...

from pydub import AudioSegment
import speech_recognition as sr
import os
import sys
import time

# Ajout d'un paramètre pour la langue
def transcribe_audio(file_path, language="fr-FR"):
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data, language=language)
            # Calculer la durée en utilisant pydub
            audio_segment = AudioSegment.from_file(file_path)
            duration = len(audio_segment) / 1000.0  # Durée en secondes
            return text, duration
        except sr.UnknownValueError:
            return "[Aucune transcription possible]", 0
        except sr.RequestError as e:
            return "[Erreur de requête]", 0


def write_transcription(file_path, text, log_file):
    partial_txt_path = file_path.rsplit('.', 1)[0] + '_partial.txt'
    final_txt_path = file_path.rsplit('.', 1)[0] + '.txt'
    with open(partial_txt_path, 'w', encoding='utf-8') as file:
        file.write(text)
    os.rename(partial_txt_path, final_txt_path)
    message = f'Transcription enregistrée : {final_txt_path}'
    print(message)
    log_file.write(message + "\n")

def batch_transcribe(folder_path, log_file_path, language):
    num_folders = 0
    num_transcribed = 0
    num_errors = 0
    total_duration = 0
    max_duration = 3600  # Limite de 60 minutes

    with open(log_file_path, 'w') as log_file:
        for subdir, dirs, files in sorted(os.walk(folder_path)):
            dirs.sort()  # Trier les sous-dossiers
            num_folders += 1
            for file in sorted(files):  # Trier les fichiers
                if file.endswith(".wav"):
                    filepath = os.path.join(subdir, file)
                    txt_path = filepath.rsplit('.', 1)[0] + '.txt'
                    partial_txt_path = filepath.rsplit('.', 1)[0] + '_partial.txt'
                    if not os.path.exists(txt_path) and not os.path.exists(partial_txt_path):
                        message = f"Transcription du fichier : {filepath}"
                        print(message)
                        log_file.write(message + "\n")
                        text, duration = transcribe_audio(filepath, language)
                        total_duration += duration
                        if text.startswith("["):
                            num_errors += 1
                        else:
                            num_transcribed += 1
                        write_transcription(filepath, text, log_file)
                        # Supprimer le fichier média original (autre que .wav)
                        os.remove(filepath)
                        if total_duration >= max_duration:
                            print("Pause pour éviter la limitation de l'API...")
                            time.sleep(120)  # Pause de 2 minutes
                            total_duration = 0
                    else:
                        message = f"La transcription existe déjà pour le fichier : {filepath}. Ignoré."
                        print(message)
                        log_file.write(message + "\n")

        # Écrire le résumé à la fin
        summary = f"\nRésumé:\nNombre de dossiers parcourus: {num_folders}\nNombre de transcriptions: {num_transcribed}\nErreurs: {num_errors}\n"
        print(summary)
        log_file.write(summary)

if len(sys.argv) != 3:
    print("Usage: python convert_audio_to_txt.py <chemin_du_dossier> <langue>")
    sys.exit(1)

folder_path = sys.argv[1]
language = sys.argv[2]  # Langue pour la transcription
log_file_path = os.path.join(folder_path, "transcription_log.txt")
batch_transcribe(folder_path, log_file_path, language)
