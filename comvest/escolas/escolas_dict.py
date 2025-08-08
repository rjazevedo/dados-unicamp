"""
Este módulo contém constantes (dicionários e conjuntos)
utilizadas para o pré-processamento e padronização de nomes de escolas.
"""

# Conjunto de stopwords gramaticais a serem removidas completamente dos nomes das escolas.
# Estes termos geralmente não contribuem para a identificação única da instituição.
STOPWORDS_GRAMATICAIS = {
    'DE', 'DA', 'DO', 'E', 'A', 'DOS', 'DAS', 'D', 'O',
    'C', 'LA', 'S', 'P', 'M', 'G', 'R', 'J', 'T', 'N',
    'LTDA'
}


# Dicionário para padronização de termos qualificadores em nomes de escolas.
# As chaves são as variações encontradas e os valores são as formas canônicas desejadas.
# Estes termos serão padronizados e MANTIDOS na string final para distintividade.
TERMOS_QUALIFICADORES_NORMALIZACAO = {
    # Tipos de Instituição / Qualificadores
    'COLEGIO': 'COL',
    'COLÉGIO': 'COL', # Adicionar se aparecer com acento na base original
    'ESCOLA': 'ESC',
    'EE': 'ESC EST', # Escola Estadual - padronizar para 'ESC' ou 'EE'
    'E.E.': 'ESC EST',
    'EDUCACIONAL': 'EDUC',
    'EDUCACAO': 'EDUC',
    'CENTRO': 'CEN',
    'INSTITUTO': 'INST',
    'ENSINO': 'ENS',
    'UNIDADE': 'UNID',
    'FUNDACAO': 'FUND',
    'SISTEMA': 'SIST',
    'CURSO': 'CUR',
    'CURSOS': 'CUR',
    'BASICA': 'BAS',
    'ORGANIZACAO': 'ORG',
    'SOCIEDADE': 'SOC',
    'ASSOCIACAO': 'ASSOC',
    'EDUCANDARIO': 'EDUC',
    'INSTITUICAO': 'INST',

    # Títulos e designações
    'PROFA': 'PROF',
    'PROFESSOR': 'PROF',
    'PROFESSORA': 'PROF',
    'PROF.': 'PROF',
    'DR.': 'DR',
    'DOUTOR': 'DR',
    'MADRE': 'MAD',
    'PADRE': 'PAD',
    'MONSENHOR': 'MONS',
    'CONSELHEIRO': 'CONS',
    'PRESIDENTE': 'PRES',
    'SENADOR': 'SEN',
    'VEREADOR': 'VER',
    'MINISTRO': 'MIN',
    'BISPO': 'BISPO',
    'CAPITAO': 'CAP',
    'CORONEL': 'CEL',
    'MAJOR': 'MAJ',
    'GENERAL': 'GEN',

    # Níveis e Modalidades de Ensino
    'MEDIO': 'MED',
    'FUNDAMENTAL': 'FUND',
    'INFANTIL': 'INF',
    'INF': 'INF',
    'TECNICO': 'TEC',
    'TECNICA': 'TEC',
    'TECNOLOGICO': 'TEC',
    'TECNOLOGICA': 'TEC',
    'TECN': 'TEC',
    'INTEGRADO': 'INT',
    'INTEGRAL': 'INT',
    'PROFISSIONAL': 'PROFISS', # Cuidado para não confundir com 'PROF' de professor
    'POLIVALENTE': 'POLI',
    'POLITECNICO': 'POLITEC',
    'POLITEC': 'POLITEC',
    'SUPERIOR': 'SUP', # Se aparecer na lista, adicionar
    'VESTIBULARES': 'VEST',
    'SUPLETIVO': 'SUPLET',
    'EDUC.BASICA': 'EDUC',

    # Adjetivos / Qualificadores Comuns
    'ESTADUAL': 'EST',
    'MUNICIPAL': 'MUN',
    'FEDERAL': 'FED',
    'NACIONAL': 'NAC',
    'PARTICULAR': 'PART', # Se aparecer na lista, adicionar
    'INTERATIVO': 'INT', # Cuidado com 'INTEGRADO'/'INTEGRAL'
    'BRASILEIRO': 'BR',
    'BRASILEIRA': 'BR',
    'NOVA': 'NOV',
    'CRISTA': 'CRIST',
    'CRISTAO': 'CRIST',
    'DIVINO': 'DIV',
    'SAGRADO': 'SAG',
    'SAGRADA': 'SAG',
    'NOSSA': 'NS',
    'SENHORA': 'SRA',
    'SANTA': 'STA',
    'SANTO': 'STO',
    'IMACULADA': 'IMAC',
    'AUXILIADORA': 'AUX',
    'ADVENTISTA': 'ADV',
    'SALESIANO': 'SALES',
    'SALESIANA': 'SALES',
    'AGOSTINIANO': 'AGOS',
    'FRANCISCANO': 'FRANC',
    'METODISTA': 'MET',
    'PRESBITERIANO': 'PRESB',
    'DIOCESANO': 'DIO',
    'COMUNITARIA': 'COM',
    'COOPERATIVA': 'COOP',
    'APLICADO': 'APLIC',
    'ESCOLAR': 'ESC', # Cuidado para não conflitar com ESCOLA
    'COMERCIAL': 'COM',
    'INDUSTRIAL': 'IND',
    'BASICA': 'BAS',
    'AGRÍCOLA': 'AGRI', # Se aparecer
    'MILITAR': 'MIL',
    'CIENCIA': 'CIENC',
    'CIENCIAS': 'CIENC',
    'CULTURA': 'CULT',
    'ARTE': 'ART',
    'ARTES': 'ART',
    'INFORMATICA': 'INF'
}
