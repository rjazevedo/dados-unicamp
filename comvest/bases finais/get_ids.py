import pandas as pd

df = pd.read_csv('../auxiliares/dados/dados_comvest.csv')

df = df[df.duplicated(subset=['ano_vest','insc_vest'])]

print(df)