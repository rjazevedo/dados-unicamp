
import pandas as pd

final_counties = pd.read_csv('final_counties.csv')
dados_cadastrais = pd.read_csv('dados_cadastrais.csv')

final_counties = final_counties[['municipio_x', 'uf_y', 'codigo_municipio']]
final_counties = final_counties.drop_duplicates(['municipio_x', 'uf_y'])

final_counties.columns = ['mun_nasc_d', 'uf_nasc_d', 'cod_mun_nasc_d']
mun_nasc_d_merge = pd.merge(dados_cadastrais, final_counties, how='left')
print(mun_nasc_d_merge.columns)

final_counties.columns = ['mun_esc_form_em', 'uf_esc_form_em', 'cod_mun_form_em']
mun_nasc_d_merge = pd.merge(mun_nasc_d_merge, final_counties, how='left')
print(mun_nasc_d_merge.columns)

mun_nasc_d_merge = mun_nasc_d_merge[['mun_nasc_d', 'uf_nasc_d', 'cod_mun_nasc_d', 'mun_esc_form_em', 'uf_esc_form_em', 'cod_mun_form_em']]
mun_nasc_d_merge.to_csv('dac_mun_codigo.csv', index=False)