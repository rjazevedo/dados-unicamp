from capes.cleaning import cleaning_functions


def get_columns_info_capes():
    return {
        'ano_base_a': {
            'old_names': ['AN_BASE'],
            'clean_type': 'Int16',
            'cleaning_function': None

        },
        'ano_nasc_a': {
            'old_names': ['AN_NASCIMENTO_DISCENTE'],
            'clean_type': "Int64",
            'cleaning_function': cleaning_functions.clean_ano

        },
        'ano_matr_discente': {
            'old_names': ['AN_MATRICULA_DISCENTE'],
            'clean_type': 'Int16',
            'cleaning_function': cleaning_functions.clean_ano

        },
        'me_matr_discente': {
            'old_names': ['ME_MATRICULA_DISCENTE'],
            'clean_type': 'Int8',
            'cleaning_function': cleaning_functions.clean_mes

        },
        'dt_matr_discente': {
            'old_names': ['DT_MATRICULA_DISCENTE'],
            'clean_type': 'str',
            'cleaning_function': cleaning_functions.clean_data

        },
        'ano_situacao_discente': {
            'old_names': ['AN_SITUACAO_DISCENTE'],
            'clean_type': 'Int16',
            'cleaning_function': cleaning_functions.clean_ano

        },
        'me_situacao_discente': {
            'old_names': ['ME_SITUACAO_DISCENTE'],
            'clean_type': 'Int8',
            'cleaning_function': cleaning_functions.clean_mes

        },
        'dt_situacao_discente': {
            'old_names': ['DT_SITUACAO_DISCENTE'],
            'clean_type': 'str',
            'cleaning_function': cleaning_functions.clean_data

        },
        'cd_area_avaliacao': {
            'old_names': ['CD_AREA_AVALIACAO'],
            'clean_type': 'Int8',
            'cleaning_function': cleaning_functions.clean_cd_area

        },
        'nm_area_avaliacao': {
            'old_names': ['NM_AREA_AVALIACAO'],
            'clean_type': 'str',
            'cleaning_function': cleaning_functions.clean_name

        },
        'cd_conceito_curso': {
            'old_names': ['CD_CONCEITO_CURSO'],
            'clean_type': 'str',
            'cleaning_function': None

        },
        'cd_conceito_programa': {
            'old_names': ['CD_CONCEITO_PROGRAMA'],
            'clean_type': 'str',
            'cleaning_function': None

        },
        'cd_entidade_capes': {
            'old_names': ['CD_ENTIDADE_CAPES'],
            'clean_type': 'Int32',
            'cleaning_function': None

        },
        'cd_entidade_emec': {
            'old_names': ['CD_ENTIDADE_EMEC'],
            'clean_type': 'Int32',
            'cleaning_function': cleaning_functions.clean_emec

        },
        'cd_programa_ies': {
            'old_names': ['CD_PROGRAMA_IES'],
            'clean_type': 'str',
            'cleaning_function': None

        },
        'cs_status_juridico': {
            'old_names': ['CS_STATUS_JURIDICO'],
            'clean_type': 'str',
            'cleaning_function': cleaning_functions.clean_name

        },
        'ds_depend_adm': {
            'old_names': ['DS_DEPENDENCIA_ADMINISTRATIVA'],
            'clean_type': 'str',
            'cleaning_function': cleaning_functions.clean_name

        },
        'ds_faixa_etaria': {
            'old_names': ['DS_FAIXA_ETARIA', 'DS_FAIXA_ETARIA_DISCENTE'],
            'clean_type': 'str',
            'cleaning_function': None

        },
        'ds_grau_acad_discente': {
            'old_names': ['DS_GRAU_ACADEMICO_DISCENTE'],
            'clean_type': 'str',
            'cleaning_function': cleaning_functions.clean_name

        },
        'ds_tipo_nacionalidade': {
            'old_names': ['DS_TIPO_NACIONALIDADE_DISCENTE'],
            'clean_type': 'str',
            'cleaning_function': None

        },
        'dt_tese_dissertacao': {
            'old_names': ['DT_TESE_DISSERTACAO'],
            'clean_type': 'str',
            'cleaning_function': None

        },
        'id_add_foto_programa': {
            'old_names': ['ID_ADD_FOTO_PROGRAMA'],
            'clean_type': 'Int32',
            'cleaning_function': None

        },
        'id_add_foto_programa_ies': {
            'old_names': ['ID_ADD_FOTO_PROGRAMA_IES'],
            'clean_type': 'Int32',
            'cleaning_function': None

        },
        'id_pessoa': {
            'old_names': ['ID_PESSOA'],
            'clean_type': 'Int64',
            'cleaning_function': None

        },
        'nm_discente': {
            'old_names': ['NM_DISCENTE'],
            'clean_type': 'str',
            'cleaning_function': cleaning_functions.clean_name

        },
        'nm_entidade_ensino': {
            'old_names': ['NM_ENTIDADE_ENSINO'],
            'clean_type': 'str',
            'cleaning_function': cleaning_functions.clean_name

        },
        'nm_grande_area': {
            'old_names': ['NM_GRANDE_AREA_CONHECIMENTO'],
            'clean_type': 'str',
            'cleaning_function': cleaning_functions.clean_name

        },
        'nm_grau_programa': {
            'old_names': ['NM_GRAU_PROGRAMA'],
            'clean_type': 'str',
            'cleaning_function': cleaning_functions.clean_name

        },
        'nm_modalidade_programa': {
            'old_names': ['NM_MODALIDADE_PROGRAMA'],
            'clean_type': 'str',
            'cleaning_function': cleaning_functions.clean_name

        },
        'nm_municipio_programa_ies': {
            'old_names': ['NM_MUNICIPIO_PROGRAMA_IES'],
            'clean_type': 'str',
            'cleaning_function': cleaning_functions.clean_name

        },
        'nm_nivel_conclusao_discente': {
            'old_names': ['NM_NIVEL_CONCLUSAO_DISCENTE'],
            'clean_type': 'str',
            'cleaning_function': cleaning_functions.clean_name

        },
        'nm_nivel_programa': {

            'old_names': ['NM_NIVEL_PROGRAMA'],
            'clean_type': 'str',
            'cleaning_function': cleaning_functions.clean_name

        },
        'nm_nivel_titulacao_discente': {
            'old_names': ['NM_NIVEL_TITULACAO_DISCENTE'],
            'clean_type': 'str',
            'cleaning_function': cleaning_functions.clean_name

        },
        'nm_orientador': {
            'old_names': ['NM_ORIENTADOR', 'NM_ORIENTADOR_PRINCIPAL'],
            'clean_type': 'str',
            'cleaning_function': None

        },
        'nm_tipo_orientador': {
            'old_names': ['NM_TIPO_DOCENTE_ORIENT_PRINC'],
            'clean_type': 'str',
            'cleaning_function': None

        },
        'pais_nac_a': {
            'old_names': ['NM_PAIS_NACIONALIDADE_DISCENTE', 'NM_PAIS_ORIGEM_DISCENTE'],
            'clean_type': 'str',
            'cleaning_function': cleaning_functions.clean_name

        },
        'nm_programa_ies': {
            'old_names': ['NM_PROGRAMA_IES'],
            'clean_type': 'str',
            'cleaning_function': cleaning_functions.clean_name

        },
        'nm_regiao': {
            'old_names': ['NM_REGIAO', 'NM_REGIAO_ENTIDADE'],
            'clean_type': 'str',
            'cleaning_function': cleaning_functions.clean_name

        },
        'nm_situacao_discente': {
            'old_names': ['NM_SITUACAO_DISCENTE'],
            'clean_type': 'str',
            'cleaning_function': cleaning_functions.clean_name

        },
        'nm_tese_dissertacao': {
            'old_names': ['NM_TESE_DISSERTACAO'],
            'clean_type': 'str',
            'cleaning_function': None

        },
        'nr_documento_discente': {
            'old_names': ['NR_DOCUMENTO_DISCENTE'],
            'clean_type': 'str',
            'cleaning_function': None

        },
        'idade_anobase_a': {
            'old_names': ['NR_IDADE_DISCENTE'],
            'clean_type': 'Int16',
            'cleaning_function': None

        },
        'nr_seq_orientador': {
            'old_names': ['NR_SEQ_ORIENTADOR_PRINCIPAL'],
            'clean_type': 'Int64',
            'cleaning_function': None

        },
        'nr_seq_discente': {
            'old_names': ['NR_SEQUENCIAL_DISCENTE'],
            'clean_type': 'Int64',
            'cleaning_function': None

        },
        'nr_seq_tese': {
            'old_names': ['NR_SEQUENCIAL_TESE'],
            'clean_type': 'Int64',
            'cleaning_function': None

        },
        'qt_mes_titulacao': {
            'old_names': ['QT_MES_TITULACAO'],
            'clean_type': 'Int16',
            'cleaning_function': None

        },
        'sg_entidade_ensino': {
            'old_names': ['SG_ENTIDADE_ENSINO'],
            'clean_type': 'str',
            'cleaning_function': None

        },
        'sg_uf_ies': {
            'old_names': ['SG_UF_ENTIDADE_ENSINO', 'SG_UF_PROGRAMA'],
            'clean_type': 'str',
            'cleaning_function': None

        },
        'st_ingressante': {
            'old_names': ['ST_INGRESSANTE'],
            'clean_type': 'str',
            'cleaning_function': cleaning_functions.clean_name

        },
        'tp_documento_discente': {
            'old_names': ['TP_DOCUMENTO_DISCENTE'],
            'clean_type': 'str',
            'cleaning_function': None

        }
    }


# Returns a dictionary corresponding old names with the new ones
def get_columns_names():
    names_dict = {}
    cols_info = get_columns_info_capes()
    for new_name in cols_info:
        for old_name in cols_info[new_name]['old_names']:
            names_dict[old_name] = new_name
    return names_dict


def get_capes_clean_dtypes():
    columns_info = get_columns_info_capes()
    dtypes = {}
    for column in columns_info:
        dtypes[column] = columns_info[column]['clean_type']
    return dtypes
