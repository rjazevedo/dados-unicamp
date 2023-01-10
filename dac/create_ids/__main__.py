from dac.create_ids import identificadores
import dac.clr_dados_cadastrais.__main__ as dados_cadastrais
import dac.clr_vida_academica_habilitacao.__main__ as vida_academica
import dac.clr_vida_academica_habilitacao.__main__ as vida_academica_habilitacao
import dac.clr_historico_escolar.__main__ as historico_escolar
import dac.clr_resumo_por_periodo.__main__ as resumo_periodo
from dac.create_ids.identificadores import DADOS_CADASTRAIS
from dac.create_ids.identificadores import VIDA_ACADEMICA
from dac.create_ids.identificadores import VIDA_ACADEMICA_HABILITACAO
from dac.create_ids.identificadores import HISTORICO_ESCOLAR
from dac.create_ids.identificadores import RESUMO_POR_PERIODO
from dac.create_ids.identificadores import DAC_COMVEST_IDS
from dac.utilities.io import Bases
import os


def main():
    preprocessing()
    identificadores.create_ids()


def preprocessing():
    if not(os.path.exists(Bases.RESULT_DAC.value + DADOS_CADASTRAIS)):    
        dados_cadastrais.main()

    if not(os.path.exists(Bases.RESULT_DAC.value + VIDA_ACADEMICA)):    
        vida_academica.main()

    if not(os.path.exists(Bases.RESULT_COMVEST.value + VIDA_ACADEMICA_HABILITACAO)):    
        #vida_academica_habilitacao.main()
        #TODO: Preciso ver com o rodolfo se isso daqui ta certo
        print("sem dados vida academica habilitação")

    if not(os.path.exists(Bases.RESULT_DAC.value + HISTORICO_ESCOLAR)):   
        historico_escolar.main()

    if not(os.path.exists(Bases.RESULT_DAC.value + RESUMO_POR_PERIODO)):    
        resumo_periodo.main()
    
    if not(os.path.exists(Bases.RESULT_RAIS.value + DAC_COMVEST_IDS)):    
        print("sem dados rais")


if __name__ == '__main__':
    main()