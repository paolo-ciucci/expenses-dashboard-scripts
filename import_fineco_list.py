import pandas as pd
from sqlalchemy import create_engine

months_dict = {1: 'Gennaio', 2: 'Febbraio', 3: 'Marzo', 4: 'Aprile', 5: 'Maggio', 6: 'Giugno', 7: 'Luglio', 8: 'Agosto', 9: 'Settembre', 10: 'Ottobre', 11: 'Novembre', 12: 'Dicembre'}


def get_month_name(list_month_index):
    months_string = []
    for month_index in list_month_index:
        months_string.append(months_dict.get(month_index))
    return months_string



df = pd.read_excel('C:\\Users\\paolo\\Documents\\conti\\Fineco\\movements_20230718.xlsx', decimal=',')

df['canale'] = None
df['Data'] = pd.to_datetime(df.Data, format='%d/%m/%Y')
df['year'] = pd.DatetimeIndex(df['Data']).year
df['sheet'] = get_month_name(pd.DatetimeIndex(df['Data']).month)
df['provenienza'] = 'fineco'
df['divisa'] = 'EUR'
df['causale_descrizione'] = df['Descrizione'] + ' ' + df['Descrizione_Completa']
df = df.drop('Descrizione', axis=1)
df = df.drop('Descrizione_Completa', axis=1)
df = df.rename(columns={'Data': 'data_contabile', 'Data': 'data_valuta', 'Importo': 'importo'})
print(df.to_string())
engine = create_engine('postgresql://postgres:lorellasql@localhost/my_expenses')
df.to_sql('total_expenses', con=engine, if_exists='append', index=False)
