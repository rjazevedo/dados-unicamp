import subprocess
import glob

from config.settings import get_config

config = get_config("rais")


def create_folder_tmp():
    path = config["path_output_data"]
    create_folder(path, "tmp")


def create_folder_year(year):
    path = config["path_output_data"] + "tmp/"
    create_folder(path, str(year))


def create_folder_inside_year(year, name_folder):
    path = config["path_output_data"] + "tmp/" + str(year) + "/"
    create_folder(path, name_folder)


def get_all_original_files_year(year):
    path = config["path_input_data"] + str(year) + "/"
    extension = get_extension(year)
    files = get_all_files(path, extension)
    return files


def get_all_tmp_files(year, directory, extension):
    path = config["path_output_data"] + "tmp/" + str(year) + "/" + directory + "/"
    files = get_all_files(path, extension)
    return files


def get_all_pre_processed_files(year, extension):
    path = config["path_pre_processed"] + str(year) + "/"
    files = get_all_files(path, extension)
    return files


def get_file_name(file):
    file = file.split("/")[-1]
    return file.split(".")[0]


# ------------------------------------------------------------------------------------------------
def create_folder(path, folder_name):
    # -p: precisa criar subpastas aninhadas (ex. pre_processed/<ano>/) e nao
    # deve falhar se a pasta ja existir (reexecucao apos falha parcial).
    command = "mkdir -p " + path + folder_name
    subprocess.run(command, shell=True)


def change_file_format(file, file_format):
    names = file.split(".")
    names[-1] = file_format
    names = ".".join(names)
    return names


def change_folder_name(file, folder):
    names = file.split("/")
    names[-2] = folder
    names = "/".join(names)
    return names


def get_year_path(year, path):
    path_year = path + str(year) + "/"
    return path_year


def get_all_files(path, extension):
    # sorted(): glob.glob() nao garante nenhuma ordem (depende do filesystem/SO),
    # e recover_cpf_dac_comvest.py usa sort_values() nao-estavel (default quicksort)
    # pra desempatar match probabilistico por similaridade -- com empate de score,
    # o resultado do desempate depende da ordem de entrada. Achado real: comparando
    # o mesmo dado via pkl (producao) vs parquet (cache novo, diretorio diferente),
    # a ordem do glob era diferente entre os dois diretorios e 2 de ~2M linhas
    # escolhiam um CPF homonimo diferente. sorted() torna a ordem deterministica
    # e reproduzivel entre diretorios/execucoes (nao elimina a arbitrariedade do
    # desempate em si, so a torna estavel).
    files = sorted(glob.glob(path + "*." + extension))
    return files


def get_extension(year):
    if year <= 2010:
        return "TXT"
    else:
        return "txt"
