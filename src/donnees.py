import pandas as pd

import matplotlib.pyplot as plt

donnees = pd.read_csv("donnees/gym_members_exercise_tracking.csv") #lit le CSV et place le tableau dans la variable donnees
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