import pandas as pd
from sqlalchemy import create_engine

months_dict = {1: 'Gennaio', 2: 'Febbraio', 3: 'Marzo', 4: 'Aprile', 5: 'Maggio', 6: 'Giugno', 7: 'Luglio', 8: 'Agosto', 9: 'Settembre', 10: 'Ottobre', 11: 'Novembre', 12: 'Dicembre'}


def change_uscite(x):
    if isinstance(x, float):
        return -x


def get_month_name(list_month_index):
    months_string = []
    for month_index in list_month_index:
        months_string.append(months_dict.get(month_index))
    return months_string



df = pd.read_excel('C:\\Users\\paolo\\Documents\\conti\\Unicredit\\EstrattoContoUnicredit_30-06-2022.xlsx', decimal=',')

df['Uscite'] = df.Uscite.apply(change_uscite)
df["importo"] = pd.to_numeric(df["Uscite"].fillna(0)) + pd.to_numeric(df["Entrate"].fillna(0))
df.drop(columns=["Uscite", "Entrate"], inplace=True)
df['canale'] = None
df['Data'] = pd.to_datetime(df.Data, format='%d.%m.%y')
df['Valuta'] = pd.to_datetime(df.Data, format='%d.%m.%y')
df['year'] = pd.DatetimeIndex(df['Data']).year
df['sheet'] = get_month_name(pd.DatetimeIndex(df['Data']).month)
df['provenienza'] = 'unicredit'
df['divisa'] = 'EUR'
df = df.rename(columns={'Data': 'data_contabile', 'Valuta': 'data_valuta', 'Descrizione': 'causale_descrizione'})
print(df.to_string())
engine = create_engine('postgresql://postgres:lorellasql@localhost/my_expenses')
df.to_sql('total_expenses', con=engine, if_exists='append', index=False)
