import os
import subprocess
import sys

def run_command(command, cwd=None, error_message=None):
    """
    Exécute une commande shell et gère les erreurs
    
    :param command: Commande à exécuter
    :param cwd: Répertoire de travail (optionnel)
    :param error_message: Message personnalisé en cas d'erreur
    """
    # Normaliser le chemin et vérifier son existence
    if cwd:
        cwd = os.path.normpath(cwd)
        if not os.path.exists(cwd):
            print(f"Erreur : Le répertoire {cwd} n'existe pas.")
            sys.exit(1)

    try:
        # Utiliser une approche différente pour Windows
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd,
            capture_output=True, 
            text=True,
            encoding='utf-8'  # Spécification de l'encodage UTF-8
        )
        
        # Vérifier le code de retour
        if result.returncode != 0:
            print(f"Erreur lors de l'exécution de la commande : {result.stderr}")
            if error_message:
                print(error_message)
            sys.exit(1)
        
        print(result.stdout)
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        sys.exit(1)

def main():
    # Obtenir le chemin du répertoire racine du projet
    base_dir = os.path.normpath(os.getcwd())
    
    # Chemins absolus pour éviter les problèmes
    back_path = os.path.normpath(os.path.join(base_dir, "Back", "trading_back_v2"))
    api_path = os.path.normpath(os.path.join(base_dir, "API_trading"))
    front_path = os.path.normpath(os.path.join(base_dir, "Front", "trading_front"))

    # Vérifier l'existence des répertoires
    for path, name in [(back_path, "Backend"), (api_path, "API"), (front_path, "Frontend")]:
        if not os.path.exists(path):
            print(f"Erreur : Le répertoire {name} n'existe pas : {path}")
            sys.exit(1)

    # Construire l'image Backend
    print("Construction de l'image Backend...")
    run_command(
        "docker build -t trading-back:latest .", 
        cwd=back_path,
        error_message="Échec de la construction de l'image Backend"
    )
    
    # Construire l'image API
    print("Construction de l'image API...")
    run_command(
        "docker build -t trading-api:latest .", 
        cwd=api_path,
        error_message="Échec de la construction de l'image API"
    )
    
    # Construire l'image Frontend
    print("Construction de l'image Frontend...")
    run_command(
        "docker build -t trading-front:latest .", 
        cwd=front_path,
        error_message="Échec de la construction de l'image Frontend"
    )
    
    # Lancer docker-compose
    print("Lancement de docker-compose...")
    run_command(
        "docker-compose up -d --build",
        error_message="Échec du démarrage des services docker-compose"
    )
    
    print("Toutes les images ont été construites et les services sont démarrés.")

if __name__ == "__main__":
    main()

# python build_and_run.py