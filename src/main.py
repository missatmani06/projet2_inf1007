from src.interface import Application #crée l'objet application et le lance
def main() -> None:
    """Crée et lance l'application graphique."""
    application = Application()
    application.lancer()
if __name__ == "__main__":
    main()