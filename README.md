# Estimation des calories après une séance
L'application qu'on a crée estime les calories brûlées associées à une séance de sport à partir du type d’entraînement, de la durée, de la fréquence cardiaque moyenne, de l’âge et du poids. Elle vérifie les saisies, affiche l’estimation sur un graphique et conserve un historique local.

# Données
Nous avons utilisé le [Gym Members Exercise Dataset](https://www.kaggle.com/datasets/valakhorasani/gym-members-exercise-dataset), publié par Vala Khorasani sur Kaggle sous licence Apache 2.0. On a téléversé le fichier en format csv dans donnees/gym_members_exercise_tracking.csv qui contient 973 observations et 15 colonnes. La variable cible est Calories_Burned.

# Installation et lancement
Depuis la racine du dépôt, avec Python 3.14 et Tkinter :
Il faut écrire ceci dans le terminal pour l'installation des environnements utilisés et le lancement de 
l'application un après l'autre:
```bash
python -m pip install -r requirements.txt
python -m src.main
'''
#Quand l'application s'ouvre, elle charge le modèle sauvegardé au démarrage. Pour réentraîner et regénérer les fichiers dans le dossier modeles:
```bash
python -m src.modele
```

# Résultats du modèle
Nous avons entraîné une régression linéaire sur 778 observations et évalué ses prédictions sur les 195 observations restantes (random_state=42). La MAE mesure l’écart absolu moyen entre les prédictions et les valeurs du CSV. Nous avons trouvé une MAE de référence à partir de la moyenne des calories dans le csv. La moyenne est de 904 calories et la MAE de 231,2 calories. La MAE des séances tests quant-à-elle est de 42,1 calories. Le modèle obtient aussi un R^2 de 0,967 sur les 5 entrées des 195 tests. Sinon, nous avons constaté que les variables qui influencent énormément la prédiction sont Avg_BPM et la durée.
Le modèle obtient aussi un R² de 0,967 sur les données de test.

**Limite.**  Nous soupconnons que la variable des calories brûlées dans le csv téléchargé depuis Kaggle a été calculée à partir d'une formule mathématique qui tient compte de toutes les 14 autres valeurs. Bien sûr, on a pas les moyens de vérifier cette hypothèse, mais c'est sûr que la précision sur des mesures réelles de dépense énergétique reste à établir.

## Structure du projet
| Fichier ou dossier | Rôle 
| `src/main.py` | Lance l’application.
| `src/interface.py` | Construit la fenêtre avec Tkinter et affiche les estimations, le graphique et l’historique. 
| `src/donnees.py` | Lit les fichiers, valide les saisies et gère l’historique. 
| `src/modele.py` | Entraîne et évalue le modèle, ou charge le modèle sauvegardé pour prédire. 
| `src/exceptions.py` | Définit l’exception utilisée pour signaler une saisie invalide. 
| `modeles/` | Contient le modèle, son encodeur et les métadonnées. 
| `tests/` | Contient les tests de validation et de calcul de la MAE. 

**Outil du chapitre 7.** Dans `lire_historique`, `lambda ligne: ligne["date"]` indique à `sorted` d’utiliser la date comme clé de tri. L’option `reverse=True` place les prédictions les plus récentes en premier.

## Tests et couverture
```bash
python -m coverage run --source=src -m pytest
python -m coverage report -m
```

Le dernier rapport de couverture local indique 11 tests réussis et 22 % de couverture sur `src`. Les tests couvrent la validation des saisies et le calcul de la MAE. GitHub Actions lance `pytest` à chaque envoi de changements et à chaque pull request.

## Références
- [Tkinter — documentation Python](https://docs.python.org/3/library/tkinter.html)
- [Régression linéaire — documentation scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)
- [Intégrer un graphique Matplotlib dans Tkinter](https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html)