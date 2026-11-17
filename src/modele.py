import os
import pandas as pd
from sklearn.model_selection import train_test_split #train_test_split est la fonction de scikit-learn qui répartit les séances en deux groupes

from sklearn.preprocessing import OneHotEncoder

chemin= os.path.join("donnees", "gym_members_exercise_tracking.csv") #on ouvre le fichier csv du jeu de données
if not os.path.exists(chemin):
    raise FileNotFoundError(f"Fichier introuvable : {chemin}")
with open(chemin, encoding="utf-8") as fichier:
    donnees=pd.read_csv(fichier)

entrees = [
    "Workout_Type",
    "Session_Duration (hours)",
    "Avg_BPM",
    "Age",
    "Weight (kg)",
]

X = donnees[entrees]
y = donnees["Calories_Burned"] #calories enregistrées pour chaques séances.

X_train, X_test, y_train, y_test = train_test_split( #train_test_split les sépares ensemble pour que chaque séance garde sa valeur de calories
    X, y, test_size=0.20, random_state=42 #test_size réserve 20% des séances au test et random_state=42 permet de retrouver la même séparation à chaque exécution sur le même fichier.
)
#Pour une même séance, X contient les informations qu’on pourra donner au modèle, donc le type et la durée, le pouls, l'âge et le poids
# et y contient la réponse enregistrée dans le CSV. Les lettres X et y peuvent se lire comme « les entrées » et « les réponses ».
print("Séances d'entraînement :", len(X_train))
print("Séances de test :", len(X_test))

moyenne_reference = y_train.mean() #calcul la moyenne de calories brûlées des 778 séances d'entraînement
erreurs_reference = (y_test - moyenne_reference).abs() #soustrait aux calories de chacune des 195 séances de test et l'écart doit être positif où nul
mae_reference = erreurs_reference.mean() #fait la moyenne des 195 écarts calculés. C'est la MAE de 231,2 calories

print(f"Prédiction de référence : {moyenne_reference:.1f} calories") #on affiche une décimal
print(f"MAE de la référence : {mae_reference:.1f} calories")

print(X_train["Workout_Type"].value_counts()) #pour trouver le nombre de workout_type de ces 778 séances d'entraînement.
#on veut maintenant transformer ces workout_type en 4 colonnes de 0 et 1 (car la régression linéaire fait des calculs avec des nombres), une par type. Cela s'appelle l'encodage one-hot où chaque 1 indique la catégorie de la séance
encodeur = OneHotEncoder(sparse_output=False)
types_encodes = encodeur.fit_transform(X_train[["Workout_Type"]]) #repère les catégories dans les séances d'entraînement, puis les transforme en 0 et 1 et garde workout type sous forme de tableau à une colonne
print(types_encodes[:5]) #affiche seulement les 5 premières séances encodées

print(encodeur.categories_[0]) #donne l'ordre des colonnes
print(X_train["Workout_Type"].head(5).tolist()) #donne l'ordre des 5 séances dans x_train