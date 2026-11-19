import tkinter as tk
from tkinter import ttk
import os
from src.donnees import charger_metadonnees, creer_variables
from src.modele import ModeleCalories
from src.exceptions import DonneeInvalideError

class Application:
    """Représente l'interface graphique de l'application."""
    def __init__(self) -> None:
        """Crée la fenêtre principale et ses premiers éléments."""
        dossier_src = os.path.dirname(os.path.abspath(__file__))
        self._dossier_projet = os.path.dirname(dossier_src)#repère le dossier src
        chemin_json = os.path.join(#remonte au dossier principal du projet et construit le chemin vers le json
            self._dossier_projet, "modeles", "metadonnees.json"
        )
        self._metadonnees = charger_metadonnees(chemin_json)#conserve son contenue pour les prochains éléments de l'interfacw
        self._variables = creer_variables(self._metadonnees)#pour que l'appli conserve deux dict
        chemin_modele = os.path.join(#pour charger le modèle une seule fois à son démarrage
            self._dossier_projet, "modeles", "modele_calories.joblib"
        )
        self._modele = ModeleCalories(chemin_modele)
        self._fenetre = tk.Tk()#crée la fenêtre
        self._fenetre.title("Estimation des calories brûlées après une séance d'entraînement")#définir le titre
        self._fenetre.geometry("800x600")#taille en pixel
        titre = ttk.Label(#crée un txt dans la fenêtre
            self._fenetre,
            text="Estimer les calories brûlées après une séance",
            font=("Arial", 16)
        )
        titre.pack(pady=20)#pack place ce texte et pady ajoute un espace au dessus et en dessous
        self._creer_champs()#crée les champs au démarrage de la fenêtre
        self._resultat = ttk.Label(self._fenetre, text="")
        self._resultat.pack(pady=10)
        bouton = ttk.Button(
            self._fenetre,
            text="Prédire",
            command=self._predire
        )
        bouton.pack(pady=10)
        avertissement = ttk.Label(
            self._fenetre,
            text=(
                "Exercice pédagogique : cette estimation ne constitue "
                "pas une mesure réelle de votre dépense énergétique."
            ),
            wraplength=700
        )
        avertissement.pack(pady=10)
    def _creer_champs(self) -> None:
        """Crée un champ par entrée indiquée dans les métadonnées."""#menu déroulant etc
        self._champs = {}
        cadre = ttk.Frame(self._fenetre)
        cadre.pack(padx=20, pady=10)
        for ligne, nom in enumerate(self._metadonnees["entrees"]):
            etiquette = ttk.Label(cadre, text=nom)
            etiquette.grid(row=ligne, column=0, padx=5, pady=5)
            if nom in self._metadonnees["categories"]:
                champ = ttk.Combobox(
                    cadre,
                    values=self._metadonnees["categories"][nom],
                    state="readonly"
                )
            else:
                champ = ttk.Entry(cadre)
            champ.grid(row=ligne, column=1, padx=5, pady=5)
            self._champs[nom] = champ

    def _predire(self) -> None:
        """Lit les champs, valide les saisies et affiche la prédiction."""
        try:
            valeurs = {}
            for nom, champ in self._champs.items():
                saisie = champ.get()#recupere le texte de chaque champ
                valeurs[nom] = self._variables[nom].valider(saisie)#verifie le texte et retourne sa valeur utilisable
            prediction = self._modele.predire(valeurs)
        except DonneeInvalideError as erreur:#si le saisie est invalide, except affiche le message et
            self._resultat.config(
                text=str(erreur),
                foreground="red"
            )
            return
        self._resultat.config(
            text=f"Calories brûlées lors de ta séance. Bravo!: {prediction:.1f}",
            foreground="black"
        )
    def lancer(self) -> None:
        """Affiche la fenêtre et attend les actions de l'utilisateur."""
        self._fenetre.mainloop()