# Journal d’utilisation de l’IA

| Outil | Ce que j’ai demandé | Réponse reçue | Vérification faite | Décision |

| ChatGPT | Comment commencer le projet après avoir choisi le jeu de données ? | Lire le CSV avec pandas et examiner ses dimensions et ses valeurs manquantes. | J’ai exécuté le code dans VS Code. Le tableau contenait 973 lignes et 15 colonnes, sans valeur manquante. | **Gardé.** J’ai poursuivi l’analyse avec ce fichier.

| ChatGPT | Comment savoir si la régression linéaire fait mieux qu’une prédiction simple ? | Comparer sa MAE à celle d’une référence qui prédit toujours la moyenne des calories d’entraînement. | J’ai exécuté l’évaluation sur le même ensemble de test pour les deux méthodes. La MAE était de 42,1 calories pour le modèle et de 231,2 pour la référence. | **Gardé.** J’ai utilisé la MAE pour comparer les deux méthodes. |

| ChatGPT | Comment vérifier que l’application refuse les mauvaises saisies ? | Utiliser des classes de validation et écrire des tests pour les valeurs acceptées, les limites et les erreurs. | J’ai lancé `python -m pytest`. Les 11 tests du projet ont réussi, dont ceux qui vérifient les saisies invalides. | **Gardé.** J’ai conservé les validateurs et les tests. 

| ChatGPT | Pourquoi l’application affiche-t-elle une erreur quand j’ouvre l’historique ? | Vérifier si le nom de la colonne utilisée pour le tri correspond à l’en-tête du CSV. | Le terminal affichait `KeyError: 'Date'`. J’ai ouvert le CSV et constaté que l’en-tête était `date` en minuscule. Après correction, l’historique s’est ouvert. | **Modifié.** J’ai utilisé `date` dans le code de lecture pour correspondre au CSV. 

| ChatGPT | Les calories du CSV pourraient-elles avoir été obtenues par une formule ? | ChatGPT a proposé une formule utilisant la durée, la fréquence cardiaque moyenne, l’âge et la colonne `Gender`. | ChatGPT a testé la formule sur le CSV téléchargé depuis Kaggle. Après arrondi, elle reproduisait les 973 valeurs de `Calories_Burned`. On ne peut évidemment pas savoir la méthode utilisée par l’auteur reste à confirmer. | 