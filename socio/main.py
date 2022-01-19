import cleaning_module.clear
import cleaning_module.verify
import cleaning_module.merge

# Insira aqui o caminho para os arquivos originais, e o caminho para o diretório já existente onde serão criados os arquivos limpos
# Obs: De preferência, crie um diretório separado para os arquivos limpos, pois pode haver conflito de nomes
# Execute este script a partir do diretório em que o mesmo se encontra, pois caso contrário as funções de verificação falharão
PATH_FILE_SOCIO = '/home/larissa/socio/dados/original/socio.csv'
PATH_FILE_EMPRESA = '/home/larissa/socio/dados/new/empresa.csv'
PATH_FILE_CNAE_SECUNDARIA = '/home/larissa/socio/dados/original/cnae_secundaria.csv'
PATH_FILE_DAC_COMVEST = '/home/larissa/socio/dados/dac_comvest_ids.csv'
PATH_DIRECTORY_CLEAN = '/home/larissa/socio/dados/clean/'

cleaning_module.clear.clear_socio(PATH_FILE_SOCIO, PATH_DIRECTORY_CLEAN)
cleaning_module.clear.clear_empresa(PATH_FILE_EMPRESA, PATH_DIRECTORY_CLEAN)
cleaning_module.clear.clear_cnae_secundaria(PATH_FILE_CNAE_SECUNDARIA, PATH_DIRECTORY_CLEAN)
cleaning_module.verify.verify_cleaning(PATH_DIRECTORY_CLEAN)
cleaning_module.merge.merge_socio_dac_comvest(PATH_FILE_DAC_COMVEST, PATH_DIRECTORY_CLEAN)