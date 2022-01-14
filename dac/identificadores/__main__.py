from identificadores import identificadores
from identificadores import transf_int
from identificadores import exploration
from identificadores import amostra
from identificadores import rescue2019
def main():
    identificadores.generate_ids()
    # amostra.get_ids()
    rescue2019.rescue()
    exploration.get_relations()

if __name__ == '__main__':
    main()