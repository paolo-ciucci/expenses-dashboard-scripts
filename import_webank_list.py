import numpy as np
import pandas as pd
from sqlalchemy import create_engine

months_dict = {1: 'Gennaio', 2: 'Febbraio', 3: 'Marzo', 4: 'Aprile', 5: 'Maggio', 6: 'Giugno', 7: 'Luglio', 8: 'Agosto', 9: 'Settembre', 10: 'Ottobre', 11: 'Novembre', 12: 'Dicembre'}


def get_month_name(list_month_index):
    months_string = []
    for month_index in list_month_index:
        months_string.append(months_dict.get(month_index))
    return months_string

def if_prelievo(row):
    if 'PRELEVAMENTO' in row['DESCRIZIONE DELLE OPERAZIONI']:
        val = 'Atm'
    else:
        val = None
    return val

df = pd.read_excel('C:\\Users\\paolo\\Documents\\conti\\Bpm\\lista_movimenti_2023-Apr-Giu.xlsx', decimal=',')
df = df.replace({np.nan:None})
# df['Data Operazione'] = pd.to_datetime(df.Data, format='%d/%m/%Y')
# df['Data Valuta Addebito'] = pd.to_datetime(df.Data, format='%d/%m/%Y')
df['anno'] = pd.DatetimeIndex(df['DATA CONTABILE']).year
df['sheet'] = get_month_name(pd.DatetimeIndex(df['DATA CONTABILE']).month)
df['provenienza'] = 'bpm'
df['divisa'] = 'EUR'
df['canale'] = df.apply(if_prelievo, axis=1)
df = df.rename(columns={'DATA CONTABILE': 'data_contabile', 'DATA VALUTA': 'data_valuta', 'DESCRIZIONE DELLE OPERAZIONI': 'causale_descrizione', 'Importo': 'importo'})
print(df.to_string())
engine = create_engine('postgresql://postgres:lorellasql@localhost/my_expenses')
df.to_sql('total_expenses', con=engine, if_exists='append', index=False)
