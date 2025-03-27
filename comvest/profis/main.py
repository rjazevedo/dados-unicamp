import sys
import subprocess
from clear_profis import clean_data
import os


# Adiciona o diretório do script ao sys.path para garantir que o clear_profis seja encontrado
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def install_requirements() -> None:
    """
    Instala as dependências listadas no arquivo requirements.txt.
    
    Retorna
    -------
    None
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError as e:
        print(f"Erro ao instalar dependências: {e}")
        sys.exit(1)


def main() -> None:
    install_requirements()
    clean_data()


if __name__ == "__main__":
    main()
