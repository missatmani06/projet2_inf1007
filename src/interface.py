import tkinter as tk
from tkinter import ttk
import os
from src.donnees import (charger_metadonnees, creer_variables, enregistrer_prediction)#pour l'historique
from src.modele import ModeleCalories
from src.exceptions import DonneeInvalideError
import csv
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from src.donnees import lire_historique
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.donnees import charger_donnees

class Application:
    """Représente l'interface graphique de l'application."""
    def __init__(self) -> None:
        """Crée la fenêtre principale et ses premiers éléments."""
        dossier_src = os.path.dirname(os.path.abspath(__file__))
        self._dossier_projet = os.path.dirname(dossier_src)#repère le dossier src
        self._chemin_historique=os.path.join(self._dossier_projet, "historique_predictions.csv")
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
        self._fenetre.geometry("1000x700")#taille en pixel
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
        bouton_historique = ttk.Button(
            self._fenetre,
            text="Voir l'historique",
            command=self._afficher_historique
        )
        bouton_historique.pack(pady=10)
        avertissement = ttk.Label(
            self._fenetre,
            text=(
                "Exercice pédagogique : cette estimation ne constitue "
                "pas une mesure réelle de votre dépense énergétique."
            ),
            wraplength=700
        )
        avertissement.pack(pady=10)
        self._creer_graphique()
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
            self._actualiser_graphique(prediction)
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
        try:
            enregistrer_prediction(self._chemin_historique, valeurs, prediction)
        except OSError:
            self._resultat.config(#l'appel transmet à la fonction le chemin du fichier
                text=(
                     f"Calories estimées : {prediction:.1f}. "
                    "Impossible d'enregistrer l'historique."
                ),
                foreground="red")
                             
    def _afficher_historique(self) -> None:
        """Lit l'historique et l'affiche dans une fenêtre consultable."""
        try:
            historique = lire_historique(self._chemin_historique)
        except (OSError, csv.Error, KeyError):
            messagebox.showerror(
                "Historique",
                "Impossible de lire l'historique : "
                "le fichier est inaccessible ou son format est incorrect.",
                parent=self._fenetre
            )
            return

        if not historique:
            messagebox.showinfo(
                "Historique",
                "Aucune prédiction enregistrée.",
                parent=self._fenetre
            )
            return

        fenetre = tk.Toplevel(self._fenetre)
        fenetre.title("Historique des prédictions")
        fenetre.geometry("700x450")

        texte = ScrolledText(fenetre, wrap="word")
        texte.pack(fill="both", expand=True)

        for prediction in historique:
            for nom, valeur in prediction.items():
                texte.insert("end", f"{nom} : {valeur}\n")
            texte.insert("end", "\n")

        texte.config(state="disabled")
    def _creer_graphique(self) -> None:
        """Affiche la répartition des calories enregistrées dans le CSV."""
        chemin = os.path.join(
            self._dossier_projet,
            "donnees",
            "gym_members_exercise_tracking.csv"
        )
        donnees = charger_donnees(chemin)
        self._figure = Figure(figsize=(6, 2.4), dpi=100)#figure est l'objet qui contient le graphique
        self._axes = self._figure.add_subplot()#zone ou on dessine les barres et écrit le titre
        self._axes.hist(
            donnees["Calories_Burned"],
            bins=20,#regroupe les valeurs de calories de toutes les lignes du csv en 20 intervalles
            color="skyblue",
            edgecolor="white"
        )
        self._axes.set_title("Répartition des calories dans le dataset")
        self._axes.set_xlabel("Calories enregistrées dans le CSV")
        self._axes.set_ylabel("Nombre d'observations")
        self._figure.tight_layout()
        self._ligne_prediction = None
        self._canvas = FigureCanvasTkAgg(#affiche la figure directement dans tkinter
            self._figure, master=self._fenetre
        )
        self._canvas.draw()
        self._canvas.get_tk_widget().pack(
            fill="both", expand=True, padx=20, pady=10
        )

    def _actualiser_graphique(self, prediction: float) -> None:
        """Place la prédiction reçue sur l'histogramme."""
        if self._ligne_prediction is not None:
            self._ligne_prediction.remove()#retire l'ancienne ligne après chaque utilisation.

        self._ligne_prediction = self._axes.axvline(#dessine une ligne verticale à la valeur prédite
            x=prediction,
            color="purple",
            linewidth=2,
            label=f"Estimation : {prediction:.1f} calories"
        )
        self._axes.legend()#affiche l'explication de la ligne
        self._canvas.draw_idle()#pour mettre le graphique a jour dans la fenêtre

    def lancer(self) -> None:
        """Affiche la fenêtre et attend les actions de l'utilisateur."""
        self._fenetre.mainloop()