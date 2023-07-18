import pandas as pd
from sqlalchemy import create_engine


df = pd.read_excel('C:\\Users\\paolo\\Documents\\conti\\Hype\\EstrattoConto_parziale_Giu_2023Hype.xlsx', decimal=',')


df['data_contabile'] = pd.to_datetime(df['data_contabile'], format='%d/%m/%Y')
df['data_valuta'] = pd.to_datetime(df['data_valuta'], format='%d/%m/%Y')
print(df.to_string())
engine = create_engine('postgresql://postgres:lorellasql@localhost/my_expenses')
df.to_sql('total_expenses', con=engine, if_exists='append', index=False)
