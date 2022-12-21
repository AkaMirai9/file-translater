# file-translater

# Prérequis
Python >= 3
L'ensemble des modules listées dans requirements.txt

# Configuration
Le fichier languages.txt doit contenir sur chaque ligne l'abreviation correspondant à une langue cible :
    - L'ensemble des langages disponibles se trouvent dans le fichier languages.json

Attention: la ligne doit juste contenir les lettres et un retour à la ligne (pas d'espaces / de ponctuation)
PS: ne fonctionne pas avec le chinois pour le moment

# Utilisation
Sur Windows:
    - python3 .\fileTranslator\fileTranslator.py path\to\file\[langage].json

Cette commande créera ou écrasera un dossier result contenant l'ensemble des fichiers de traduction traduit dans toutes les langues demandées 


Attention: Ici [langage] fait référence au code du langage décris dans la section Configuration