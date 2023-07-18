import pandas as pd
from sqlalchemy import create_engine

months_dict = {1: 'Gennaio', 2: 'Febbraio', 3: 'Marzo', 4: 'Aprile', 5: 'Maggio', 6: 'Giugno', 7: 'Luglio', 8: 'Agosto', 9: 'Settembre', 10: 'Ottobre', 11: 'Novembre', 12: 'Dicembre'}


def get_month_name(list_month_index):
    months_string = []
    for month_index in list_month_index:
        months_string.append(months_dict.get(month_index))
    return months_string



df = pd.read_excel('C:\\Users\\paolo\\Documents\\conti\\Hype\\lista_parziale2022.xlsx', decimal=',')

df['canale'] = None
# df['Data Operazione'] = pd.to_datetime(df.Data, format='%d/%m/%Y')
# df['Data Valuta Addebito'] = pd.to_datetime(df.Data, format='%d/%m/%Y')
df['year'] = pd.DatetimeIndex(df['DATAVALUTA']).year
df['sheet'] = get_month_name(pd.DatetimeIndex(df['DATAVALUTA']).month)
df['provenienza'] = 'hype'
df['divisa'] = 'EUR'
df = df.rename(columns={'DATACONT': 'data_contabile', 'DATAVALUTA': 'data_valuta', 'Descrizione': 'causale_descrizione', 'Importo': 'importo'})
print(df.to_string())
# engine = create_engine('postgresql://postgres:lorellasql@localhost/my_expenses')
# df.to_sql('total_expenses', con=engine, if_exists='append', index=False)
