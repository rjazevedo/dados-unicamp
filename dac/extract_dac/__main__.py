from clr_vida_academica import vida_academica
from clr_dados_cadastrais import dados_cadastrais
from clr_historico_escolar import historico_escolar


def main():
	vida_academica.generate_clean_data()
	dados_cadastrais.generate_clean_data()
	historico_escolar.generate_clean_data()	

if __name__ == '__main__':
	main()