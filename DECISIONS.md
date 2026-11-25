# Fiche de décisions

| Choix | Options envisagées | Choix retenu et justification | Validé par l’auxiliaire (date)
| Domaine | Jeux, immobilier, sport | Sport, car nous voulions créer une application qui estime les calories après une séance d’entraînement. | 10 novembre 2026

| Jeu de données | Données de tic-tac-toe, données immobilières, données de séances de sport |
 Gym Members Exercise Dataset, car il contient 973 observations et fournit des variables numériques et catégorielles ainsi qu’une cible adaptée à notre application. | 10 novembre 2026

| Cible | Catégorie à prédire ou valeur numérique à estimer |
 `Calories_Burned`. Comme on cherche à estimer un nombre de calories, c’est un problème de régression. | 17 novembre 2026

| Métrique | MAE, R² | 
Erreur absolue moyenne, elle exprime l’écart absolu moyen en calories. Nous présentons aussi le R^2 en complément. | 17 novembre 2026

| Modèle | Prédiction constante comme référence, régression linéaire | 
Régression linéaire, elle est simple à expliquer et donne une MAE de 42,1 calories, contre 231,2 pour la référence sur les mêmes données de test. | 17 novembre

| Technologie d’interface | Tkinter |
Tkinter avec Matplotlib. Tkinter permet de créer les champs et les boutons. Matplotlib affiche l’estimation sur le graphique intégré à la fenêtre. | 18 novembre