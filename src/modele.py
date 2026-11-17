import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt #pour faire les graphique prédit contre réel
import joblib # pour créé le fichier binaire
import json #pour enregister le travail effectué
from sklearn.model_selection import train_test_split #train_test_split est la fonction de scikit-learn qui répartit les séances en deux groupes
from sklearn.linear_model import LinearRegression
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
types_test_encodes = encodeur.transform(X_test[["Workout_Type"]]) #utilise le même encodeur avec le même ordre de colonne qu'on a fait dans le code précédent pour les 195 séances tests avec transform()
print(types_test_encodes.shape)

colonnes_numeriques= [
    "Session_Duration (hours)",
    "Avg_BPM",
    "Age",
    "Weight (kg)",

]
numeriques_train=X_train[colonnes_numeriques].to_numpy() #to_numpy transforme transforme les colonnes selec en tableau numpy
numeriques_test=X_test[colonnes_numeriques].to_numpy()

X_train_prepare=np.hstack((numeriques_train, types_encodes))#np.hstack colle ces deux tableaux
X_test_prepare=np.hstack((numeriques_test, types_test_encodes))
print(X_train_prepare.shape)
print(X_test_prepare.shape)

modele=LinearRegression() #on crée le modele
modele.fit(X_train_prepare, y_train) #entraîne le modèle avec les entrées des 778 séances entraînement et leurs calories enregistrées

predictions=modele.predict(X_test_prepare) #estime les calories des 195 séances de tests à partir de leurs entrées
print(predictions[:5])

erreurs=np.abs(y_test.to_numpy()- predictions) #calcul qui utilise numpy, donc vectorisé
mae_modele=np.mean(erreurs)
print(f"MAE du modèle: {mae_modele:.1f} calories")
print(f"MAE de la référence: {mae_reference:.1f}calories")
#on veut créé un graphique avec une droite rouge qui représente une prédiction exactement égale à la valeur du CSV
plt.figure()
plt.scatter(y_test, predictions)#c'est un graphique de nuage de points et chaques points qui se rapproche de la droite rouge correspond à une petite erreur et plus un point est éloigé, plus c'est une grosse erreur
bornes=[y_test.min(), y_test.max()]
plt.plot(bornes, bornes, color="red", label="Prédictions exacte")
plt.xlabel("Calories enregistrées dans le CSV")
plt.ylabel("Calories prédites")
plt.title("Évaluation de la régression linéaire")
plt.legend()
plt.tight_layout()
plt.savefig("evaluation_modele.png")
plt.close()

os.makedirs("modeles", exist_ok=True) #créé le dossier modeles
elements_a_sauvegarder={ #le dict regroupe le modèle, l'encodeur et les noms des entrées dans leur ordre
    "modele": modele,
    "encodeur": encodeur,
    "colonnes_numeriques": colonnes_numeriques,
    "entrees":entrees,

}
chemin_modele=os.path.join("modeles", "modele_calories.joblib")

with open(chemin_modele, "wb") as fichier: #"wb" ouvre un fichier pour écrire des données binaires
    joblib.dump(elements_a_sauvegarder, fichier) #enregistre ces objets dans le fichier
print("Modèle et encodeur sauvegardés.")

with open(chemin_modele, "rb") as fichier: #"rb" ouvre le fichier binaire en lecture
    elements_charges=joblib.load(fichier) #joblib.load récupère le dictionnaire sauvegardé
print(elements_charges.keys()) #keys affiches les noms des éléments du dict

intervalles={}
for colonne in colonnes_numeriques: #la boucle récupère les valeurs minimales et maximales des entrées
    intervalles[colonne]={
        "min": float(X_train[colonne].min()), #float les convertis en nombre python que JSON peut enregistrer
        "max": float(X_train[colonne].max()),
    }
metadonnees={ #ce dict contient les infos nécessaires pour construire les champs de l'interface
    "cible":"Calories_Burned",
    "entrees": entrees, #nom des entrées
    "colonnes_numeriques": colonnes_numeriques, #types d'entraînement
    "categories": {
        "Workout_Type": encodeur.categories_[0].tolist(),
    },
    "intervalles": intervalles, 
    "metrique": {
        "nom": "MAE",
        "modele": float(mae_modele),
        "reference": float(mae_reference),
    },
}
chemin_json=os.path.join("modeles", "metadonnees.json")
with open(chemin_json, "w", encoding="utf-8") as fichier:
    json.dump(metadonnees, fichier, indent=4, ensure_ascii=False) #écris le dict metadonnees dans un fichier texte et indent=4 le rend lisible