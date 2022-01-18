from os import PathLike
import clean_module.identification
import clean_module.recover_cpf_dac_comvest
import clean_module.merge
import clean_module.random_index
import clean_module.cpf_verification

PATH = '/home/larissa/rais/dados/'
FILE_DAC_COMVEST = PATH + 'uniao_dac_comvest.csv'

# clean_module.identification.get_identification_from_all_years(PATH)
# clean_module.cpf_verification.remove_invalid_cpf(PATH, FILE_DAC_COMVEST)
# clean_module.recover_cpf_dac_comvest.recover_cpf_dac_comvest(PATH)
# clean_module.random_index.generate_index(PATH)

clean_module.merge.merge_rais_dac_comvest(PATH)
clean_module.clean_columns.clean_all_years(PATH)
# clean_module.verification.verify_output(PATH)