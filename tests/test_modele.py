import numpy as np
import pytest
from sklearn.metrics import mean_absolute_error
from src.modele import calculer_mae

def test_mae_cas_connu()->None: #défini le test et le nom commence par test pour que pytest reconnaisse. La fonction ne retourne pas de résultat
    """"Vérifie la MAE avec un exemple dont le résultat est connu (20+50+50)/3=40"""
    reelles=np.array([800.0, 1000.0, 600.0]) #récupère les outils nécessaires, numpy créé les tableaux qui représentes des séances fictives pour qu'on puisse vérifier
    predites=np.array([820.0, 950.0, 650.0])
    resultat=calculer_mae(reelles, predites) #calculer_mae est la fonction récupérer de modele.py en l'appelant
    assert resultat==pytest.approx(40.0) # assert vérifie que le résultat donne 40 et que ca correspond au résultat de scikit.learn. pytest permet de tester
    assert resultat==pytest.approx(mean_absolute_error(reelles, predites)) #mean_absolute_error est le calcul de scikit_learn

#j'ajoute des tests pour vérifier les cas limites et les erreurs prévues de la fonction.
def test_ma_prediction_exacte()->None:
    """vérifie que des prédictions exacts donnent une MAE de 0, logique"""
    valeurs=np.array([600.0, 800.0])
    resultat=calculer_mae(valeurs, valeurs)
    assert resultat==pytest.approx(0.0)

def test_mae_tableaux_vides()->None:
    """vérifie que la fonction refuse des tableaux vides"""
    vide=np.array([])
    with pytest.raises(ValueError):
        calculer_mae(vide, vide)

def test_mae_formes_differentes()->None:
    """vérifie que la fonction refuse des tableaux de formes différentes"""
    reelles=np.array([600.0, 800.0])
    predites=np.array([650.0])
    with pytest.raises(ValueError):
        calculer_mae(reelles, predites)