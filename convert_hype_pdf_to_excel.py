import pandas as pd
import tabula
months_dict = {1: 'Gennaio', 2: 'Febbraio', 3: 'Marzo', 4: 'Aprile', 5: 'Maggio', 6: 'Giugno', 7: 'Luglio', 8: 'Agosto', 9: 'Settembre', 10: 'Ottobre', 11: 'Novembre', 12: 'Dicembre'}

def get_month_name(list_month_index):
    months_string = []
    for month_index in list_month_index:
        months_string.append(months_dict.get(month_index))
    return months_string

final_df = pd.DataFrame()

# read PDF file
# first page has a recap which breaks the following needed table, we have to use 'area' to pick the right table
other_pages = tabula.read_pdf("C:\\Users\\paolo\\Documents\\conti\\Hype\\pdf\\ec_01_01_2023_30_06_2023.pdf", encoding = 'cp1252', multiple_tables=True, lattice=True, pages="2-6")

for table in other_pages:
    final_df = pd.concat([final_df, table])

head = ['Data\roperazione', 'Data\rcontabile', 'Tipologia', 'Nome', 'Descrizione', 'Importo']
final_df.columns = head
final_df = final_df.drop(index=0)

def get_data_contabile(row):
    if row['Data\rcontabile'] == '---':
        val = row['Data\roperazione']
    else:
        val = row['Data\rcontabile']
    return val

def format_importo(row):
    if '+' in row['Importo']:
        val = row['Importo'].replace('+ ', '').replace('€', '')
    else:
        val = row['Importo'].replace('- ', '-').replace('€', '')
    return val

final_df['canale'] = None
final_df['Data\rcontabile'] = final_df.apply(get_data_contabile, axis=1)
final_df['Data\roperazione'] = pd.to_datetime(final_df['Data\roperazione'], format='%d/%m/%Y')
final_df['Data\rcontabile'] = pd.to_datetime(final_df['Data\rcontabile'], format='%d/%m/%Y')
final_df['year'] = pd.DatetimeIndex(final_df['Data\roperazione']).year
final_df['sheet'] = get_month_name(pd.DatetimeIndex(final_df['Data\roperazione']).month)
final_df['provenienza'] = 'hype'
final_df['divisa'] = 'EUR'
final_df['causale_descrizione'] = final_df['Tipologia'] + ' ' + final_df['Nome'] + ' ' + final_df['Descrizione']
final_df = final_df.drop('Tipologia', axis=1)
final_df = final_df.drop('Nome', axis=1)
final_df = final_df.drop('Descrizione', axis=1)
final_df['Importo'] = final_df.apply(format_importo, axis=1)
final_df = final_df.rename(columns={'Data\roperazione': 'data_contabile', 'Data\rcontabile': 'data_valuta', 'DESCRIZIONE\rOPERAZIONE': 'causale_descrizione', 'Importo': 'importo'})
print(final_df.to_string())
final_df.to_excel('C:\\Users\paolo\\Documents\\conti\\Hype\\EstrattoConto_parziale_Giu_2023Hype_2.xlsx', sheet_name='estratto_conto')


