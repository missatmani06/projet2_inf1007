import os
import pandas as pd
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod #défini une classe parent qui impose une méthode à ses classes enfants
from src.exceptions import DonneeInvalideError
import json
import csv
from datetime import datetime
#mettre la lecture du csv dans une fonction réutilisable
def charger_donnees(chemin: str) -> pd.DataFrame:#dataframe peremet de retourner dans un tableau pandas
    """Lit un fichier CSV et retourne ses données dans un DataFrame.
    Reçoit le chemin du fichier.
    Lève FileNotFoundError si le fichier n'existe pas.
    Les erreurs de lecture du CSV sont transmises à l'appelant.
    """
    if not os.path.exists(chemin):#vérifie que le fichier existe avant de l'ouvrir
        raise FileNotFoundError(f"Fichier introuvable : {chemin}")
    with open(chemin, encoding="utf-8") as fichier:
        return pd.read_csv(fichier)#transmet le tableau à l'endroit qui a appeler la fonction alors la fonction n'affiche rien
    
def charger_metadonnees(chemin: str) -> dict:
    """Reçoit le chemin d'un JSON et retourne ses métadonnées.
    Lève FileNotFoundError si le fichier n'existe pas.
    Lève json.JSONDecodeError si le contenu JSON est invalide.
    Les autres erreurs de lecture sont transmises à l'appelant.
    """
    if not os.path.exists(chemin):
        raise FileNotFoundError(f"Fichier introuvable : {chemin}")
    with open(chemin, encoding="utf-8") as fichier:
        return json.load(fichier)
class Variable(ABC):
    """décris une variable d'entrée dans l'appli"""
    def __init__(self, nom:str)->None: #mémorise le nom lors de la création de l'objet
        """recoit le nom de variable et le mémorise"""
        self._nom=nom
    @abstractmethod #oblige les futurs classes enfants à définir leur propre méthode valider
    def valider(self, saisie:str)->float|str: #nb déc ou txt
        """recoit une saisie et renvoie sa valeur valider + lève DonneeInvalideError si la saisie est invalide
        la vérification sera définie dans les classes enfants"""
        pass

class VariableNumerique(Variable): #classe qui hérite de variable
    """Représente une variable numérique avec des limites inclusives."""

    def __init__(self, nom: str, minimum: float, maximum: float) -> None:
        """Reçoit et mémorise le nom et les limites de la variable."""
        super().__init__(nom)
        self._minimum = minimum #mémorise les limites propres à cette variable
        self._maximum = maximum

    def valider(self, saisie: str) -> float:
        """Reçoit un texte et retourne un nombre dans les limites.

        Lève DonneeInvalideError si le texte est vide, non numérique
        ou si le nombre est hors des limites autorisées.
        """
        saisie = saisie.strip() #pour éviter qu'un champ soit vide à cause des espaces

        if saisie == "":
            raise DonneeInvalideError(
                f"{self._nom} : veuillez remplir le champ."
            )

        try:
            valeur = float(saisie.replace(",", ".")) #transforme le texte en nombre et accepte les virgules ou points
        except ValueError:#intercepte un texte pas rapport 
            raise DonneeInvalideError(
                f"{self._nom} : veuillez entrer un nombre."
            )

        if not self._minimum <= valeur <= self._maximum:
            raise DonneeInvalideError(
                f"{self._nom} : entrez un nombre entre "
                f"{self._minimum} et {self._maximum}."
            )

        return valeur#renvoie le modèle valider pour que le modèle puisse l'utiliser

class VariableCategorielle(Variable):
    """représente une variable avec une liste de choix autorisés"""
    def __init__(self, nom:str, choix:list[str])->None:
        """recoit le nom puis les choix autorisés et les mémorise"""
        super().__init__(nom)
        self._choix=choix.copy()

    def valider(self, saisie:str)->None:
         """Reçoit un texte et retourne le choix validé.

        Lève DonneeInvalideError si la saisie est vide
        ou ne fait pas partie des choix autorisés.
        """
         saisie=saisie.strip()
         if saisie=="":
             raise DonneeInvalideError(f"{self._nom}: veuillez sélectionner un choix.")
         if saisie not in self._choix:
             choix_possibles=",".join(self._choix)
             raise DonneeInvalideError(f"{self._nom}: choisissez parmis {choix_possibles}.")
         return saisie

def creer_variables(metadonnees: dict) -> dict[str, Variable]:
    """Reçoit les métadonnées et retourne les validateurs par nom.
    Lève KeyError si une information nécessaire manque.
    """
    variables = {}
    for nom in metadonnees["entrees"]:
        if nom in metadonnees["categories"]:
            choix = metadonnees["categories"][nom]
            variables[nom] = VariableCategorielle(nom, choix)
        else:
            limites = metadonnees["intervalles"][nom]
            variables[nom] = VariableNumerique(
                nom, limites["min"], limites["max"]
            )
    return variables
def enregistrer_prediction(chemin:str, valeurs:dict, prediction:float)->None:
    """pour ajouter au csv la date, les entrées et les prédictions recues.
    elle crée le fichier également avec ses en-tête au premier enregistrement et lève OSerror 
    si le fichier ne peut pas être lu ou écrit"""
    contient_des_donnees=(os.path.exists(chemin)and os.path.getsize(chemin)>0)
    colonnes=["date"]+list(valeurs.keys())+["Calories_estimees"]#les carctéristiques de la séances déjà valider
    date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ligne=[date]+list(valeurs.values())+[prediction]
    with open(chemin, "a", encoding="utf-8", newline="") as fichier: #le a signifie ajouter à la fin du fichier
        ecrivain=csv.writer(fichier)
        if not contient_des_donnees:
            ecrivain.writerow(colonnes)
        ecrivain.writerow(ligne)
def lire_historique(chemin: str) -> list[dict[str, str]]:#il faut appeler cette fonction pour mettre le bouton dans l'interface
    """Lit le CSV et retourne les prédictions, les plus récentes d'abord.
    Reçoit le chemin du fichier et retourne une liste vide s'il est absent.
    Lève OSError en cas d'erreur d'accès, csv.Error en cas d'erreur CSV
    et KeyError si une ligne ne contient pas la colonne Date.
    """
    if not os.path.exists(chemin):
        return []
    with open(chemin, encoding="utf-8", newline="") as fichier:
        historique = list(csv.DictReader(fichier))#lis chaque ligne comme un dictionnaire, les noms des colonnes deviennent les clées
    return sorted(
        historique,
        key=lambda ligne: ligne["date"],#trier selon la date
        reverse=True#place les dates les plus récentes en premier
    )

if __name__ == "__main__": #pour éviter que le code se relance à chaque fois qu'un fichier importe donnees.py
    chemin = os.path.join("donnees", "gym_members_exercise_tracking.csv")
    donnees=charger_donnees(chemin)
    print(donnees.shape) #donnees.shape donne ses dimensions, dans l’ordre (lignes, colonnes).

    print(donnees.isna().sum()) #isna() vérifie chaque case et donne True si la valeur est manquante et sum() compte les True dans chaque colonne. Un 0 signifie que pandas n’a détecté aucune valeur manquante dans cette colonne.

    colonnes = ["Session_Duration (hours)", "Calories_Burned"] #on séléctionne 2 colonnes pour afficher la plus petite et la plus grande valeur de chacune
    print(donnees[colonnes].agg(["min", "max"]))

    seances = donnees.nlargest(5, "Calories_Burned") # on séléctionne les 5 lignes ou le nb de calories brûlées est le plus élevé. 
    print(seances[["Calories_Burned", "Session_Duration (hours)", "Workout_Type"]]) #on affiche la durée et le type d'entraînement pour voir le contexte et si il y a quelque chose à nettoyer.

    plt.scatter(donnees["Session_Duration (hours)"], donnees["Calories_Burned"])
    plt.xlabel("Durée de la séance (heures)") #on créé un graphique pour voire si la corrélations des données fait du sens.
    plt.ylabel("Calories brûlées")
    plt.title("Calories brûlées selon la durée de la séance")
    plt.savefig("exploration_calories.png")
#""""Il n'y a aucune valeur manquante ni de valeur abérrantes. Nous avons donc rien corrigé."""