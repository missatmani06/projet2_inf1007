import pytest
from src.donnees import VariableNumerique, VariableCategorielle
from src.exceptions import DonneeInvalideError #pour verifier que VariableNumerique et tout le reste fonctionne avec un test


def test_duree_valide() -> None:
    """Vérifie qu'une durée autorisée est convertie en nombre."""
    duree = VariableNumerique("Durée de la séance", 0.5, 2.0) #créé une variable qui accepte une durée entre 0.5 et 2 heures
    resultat = duree.valider("1.5") #on lui donne 1.5 pour vérifier si ca retourne bien 1.5 car fait parti de l'intervalle
    assert resultat == pytest.approx(1.5)

def test_categorie_valide() -> None:
    """Vérifie qu'un choix autorisé est accepté.""" #dans le fond que yoga est accepté
    entrainement = VariableCategorielle(
        "Type d'entraînement",
        ["Cardio", "HIIT", "Strength", "Yoga"]
    )
    resultat = entrainement.valider("Yoga")
    assert resultat == "Yoga"

def test_categorie_inconnue() -> None:
    """Vérifie qu'un choix inconnu lève notre exception."""
    entrainement = VariableCategorielle(
        "Type d'entraînement",
        ["Cardio", "HIIT", "Strength", "Yoga"]
    )
    with pytest.raises(DonneeInvalideError):
        entrainement.valider("Natation") #voir si natation est refusé

#je vérifie mtn les saisies numériques incorrects et les cas limites
def test_nombre_vide() -> None:
    """Vérifie qu'un champ contenant seulement des espaces est refusé."""
    duree = VariableNumerique("Durée", 0.5, 2.0)
    with pytest.raises(DonneeInvalideError):
        duree.valider("   ")

def test_nombre_invalide() -> None:
    """Vérifie qu'un texte non numérique est refusé."""
    duree = VariableNumerique("Durée", 0.5, 2.0)
    with pytest.raises(DonneeInvalideError):
        duree.valider("bonjour")

def test_nombre_hors_limites() -> None:
    """Vérifie que les valeurs sous le minimum et au-dessus sont refusées."""
    duree = VariableNumerique("Durée", 0.5, 2.0)
    with pytest.raises(DonneeInvalideError):
        duree.valider("0.4")
    with pytest.raises(DonneeInvalideError):
        duree.valider("2.1")

def test_nombre_aux_limites() -> None:
    """Vérifie que le minimum et le maximum sont acceptés."""
    duree = VariableNumerique("Durée", 0.5, 2.0)
    assert duree.valider("0.5") == pytest.approx(0.5)
    assert duree.valider("2.0") == pytest.approx(2.0)