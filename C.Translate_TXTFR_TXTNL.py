"""
Translate_TXTFR_TXTNL.py - Version 1.0 (2023)
Auteur : Vincent Chapeau

Ce script Python utilise la bibliothèque googletrans pour traduire le contenu des fichiers texte du français (fr) au néerlandais (nl). Les fichiers source sont recherchés dans le dossier spécifié en tant qu'argument en ligne de commande. Les fichiers traduits sont enregistrés avec l'extension "_NL.txt" ajoutée à leur nom. Les fichiers existants en néerlandais (terminant par "_NL.txt" ou "_nl.txt") sont ignorés.

Usage :
python Translate_TXTFR_TXTNL.py <chemin_du_dossier>

Exemple :
python Translate_TXTFR_TXTNL.py /chemin/vers/votre/dossier

Le script parcourt récursivement le dossier spécifié, examine chaque fichier .txt, effectue la traduction et enregistre le résultat dans un fichier en néerlandais. En cas d'erreur lors de la traduction, il affiche un message d'erreur.

Assurez-vous d'avoir la bibliothèque googletrans installée. Vous pouvez l'installer en utilisant pip avec la commande suivante :
pip install googletrans==4.0.0-rc1

"""

# Importation des modules et code principal...


import os
import googletrans
from googletrans import Translator

translator = Translator()

def translate_text(txt_path):
    if txt_path.endswith(('_NL.txt', '_nl.txt')):
        return  # Ignore les fichiers _NL.txt ou _nl.txt existants
    nl_txt_path = txt_path.rsplit('.', 1)[0] + '_NL.txt'
    if not os.path.exists(nl_txt_path):
        with open(txt_path, 'r', encoding='utf-8') as file:
            text = file.read()
        try:
            translation = translator.translate(text, src='fr', dest='nl')
            nl_text = translation.text
            with open(nl_txt_path, 'w', encoding='utf-8') as nl_file:
                nl_file.write(nl_text)
            print(f"Traduction effectuée : {nl_txt_path}")
        except Exception as e:
            print(f"Erreur lors de la traduction du fichier {txt_path}: {str(e)}")
    else:
        print(f"Fichier _NL.txt déjà trouvé pour : {txt_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python Translate_TXTFR_TXTNL.py <chemin_du_dossier>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    for subdir, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                txt_path = os.path.join(subdir, file)
                translate_text(txt_path)
