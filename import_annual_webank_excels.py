import pandas as pd
from sqlalchemy import create_engine

sheets_dict = pd.read_excel('C:\\Users\\paolo\\Documents\\conti\\Bpm\\2022.xls', sheet_name=None)
already_saved_dict = ['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre']
all_sheets = []
for name, sheet in sheets_dict.items():
    sheet['sheet'] = name
    sheet['anno'] = 2022
    if 'totale' not in name.lower() and name not in already_saved_dict:
        sheet = sheet.rename(columns=lambda x: x.split('\n')[-1])
        all_sheets.append(sheet)

full_table = pd.concat(all_sheets)
full_table.reset_index(inplace=True, drop=True)
full_table.drop(full_table[full_table['Divisa'] != 'EUR'].index, inplace=True)
if 'Unnamed: 7' in full_table.columns:
    full_table.drop('Unnamed: 7', axis=1, inplace=True)

full_table.drop('Stato', axis=1, inplace=True)
full_table = full_table.rename(columns={'Data Contabile': 'data_contabile', 'Data Valuta': 'data_valuta', 'Causale / Descrizione': 'causale_descrizione', 'Importo': 'importo', 'Divisa': 'divisa', 'Canale': 'canale'})


engine = create_engine('postgresql://postgres:lorellasql@localhost/my_expenses')
full_table.to_sql('total_expenses', con=engine, if_exists='append', index=False)

print(full_table.to_string())
