import pandas as pd
from sqlalchemy import create_engine

months_dict = {1: 'Gennaio', 2: 'Febbraio', 3: 'Marzo', 4: 'Aprile', 5: 'Maggio', 6: 'Giugno', 7: 'Luglio', 8: 'Agosto', 9: 'Settembre', 10: 'Ottobre', 11: 'Novembre', 12: 'Dicembre'}


def get_month_name(list_month_index):
    months_string = []
    for month_index in list_month_index:
        months_string.append(months_dict.get(month_index))
    return months_string



df = pd.read_excel('C:\\Users\\paolo\\Documents\\conti\\CA_Auto_Bank\\Movimenti_07-2023.xls', decimal=',')

df['canale'] = None
df['DATA CONTABILE'] = pd.to_datetime(df['DATA CONTABILE'], format='%d-%m-%Y')
df['year'] = pd.DatetimeIndex(df['DATA CONTABILE']).year
df['sheet'] = get_month_name(pd.DatetimeIndex(df['DATA CONTABILE']).month)
df['provenienza'] = 'ca_auto_bank'
df['divisa'] = 'EUR'
df = df.rename(columns={'DATA CONTABILE': 'data_contabile', 'DATA_VALUTA': 'data_valuta', 'Importo': 'importo', 'DESCRIZIONE': 'causale_descrizione'})
print(df.to_string())
engine = create_engine('postgresql://postgres:lorellasql@localhost/my_expenses')
df.to_sql('total_expenses', con=engine, if_exists='append', index=False)
