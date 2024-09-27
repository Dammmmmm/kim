# Étape 1 : Génération dynamique du fichier script.py
script_content = """
CONST1 = 42
CONST2 = 'Bonjour le monde'
CONST3 = [1, 2, 3, 4]
"""

# Écrire ce contenu dans un fichier script.py
with open('script.py', 'w') as f:
    f.write(script_content)


import importlib.util
import sys
import os

# Étape 2 : Charger le script.py dynamiquement
file_path = os.path.abspath('script.py')

# Charger les spécifications du fichier script.py
spec = importlib.util.spec_from_file_location('script', file_path)

# Créer un module à partir de la spécification
module = importlib.util.module_from_spec(spec)
print(sys.modules)
# Ajouter le module au cache des modules importés
sys.modules['script'] = module

# Exécuter le module pour l'ajouter au cache
spec.loader.exec_module(module)

print(sys.modules)

# Étape 3 : Utiliser les constantes du module mis en cache
print(module.CONST1)  # Affiche: 42
print(module.CONST2)  # Affiche: Bonjour le monde
print(module.CONST3)  # Affiche: [1, 2, 3, 4]
