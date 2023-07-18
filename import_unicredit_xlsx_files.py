import math

import pandas as pd
from sqlalchemy import create_engine

months_dict = {1: 'Gennaio', 2: 'Febbraio', 3: 'Marzo', 4: 'Aprile', 5: 'Maggio', 6: 'Giugno', 7: 'Luglio', 8: 'Agosto', 9: 'Settembre', 10: 'Ottobre', 11: 'Novembre', 12: 'Dicembre'}


def get_month_name(list_month_index):
    months_string = []
    for month_index in list_month_index:
        months_string.append(months_dict.get(month_index))
    return months_string

def merge_entrate_uscite(row):
    if not math.isnan(row['Entrate']):
        val = row['Entrate']
    else:
        val = -row['Uscite']
    return val

df = pd.read_excel('C:\\Users\\paolo\\Documents\\conti\\Unicredit\\EstrattoContoUnicredit_2023_06_30.xlsx', decimal=',')

df['canale'] = None
df['Data'] = pd.to_datetime(df['Data'], format='%d.%m.%y')
df['Valuta'] = pd.to_datetime(df['Valuta'], format='%d.%m.%y')
df['anno'] = pd.DatetimeIndex(df['Data']).year
df['sheet'] = get_month_name(pd.DatetimeIndex(df['Data']).month)
df['provenienza'] = 'unicredit'
df['divisa'] = 'EUR'
df['importo'] = df.apply(merge_entrate_uscite, axis=1)
df = df.drop('Entrate', axis=1)
df = df.drop('Uscite', axis=1)
df = df.rename(columns={'Data': 'data_contabile', 'Valuta': 'data_valuta', 'Descrizione': 'causale_descrizione'})
print(df.to_string())

engine = create_engine('postgresql://postgres:lorellasql@localhost/my_expenses')
df.to_sql('total_expenses', con=engine, if_exists='append', index=False)
