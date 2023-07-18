import pandas as pd
import tabula

# read PDF file
# first page has a recap which breaks the following needed table, we have to use 'area' to pick the right table
file = 'C:/Users/paolo/Documents/conti/Unicredit/pdf/Estratto_conto_2023_06_30.pdf'
table_first_page = tabula.read_pdf(file, multiple_tables=True,
                                   area=(423, 42, 720, 560), lattice=True, pages="1")
first_df = table_first_page[0]
print(first_df.to_string())
# first_df.to_excel('C:\\Users\paolo\\Documents\\conti\\Unicredit\\EstrattoContoUnicredit_30-09-2021.xlsx', sheet_name='estratto_conto')


# other tables do not give issues, aside from some minor ones which will be modified manually
other_tables = tabula.read_pdf(file, multiple_tables=True,
                               pages="2", encoding='cp1252')
final_df = pd.DataFrame()

for table in other_tables:
    final_df = pd.concat([final_df, table])

final_df = pd.concat([final_df, first_df])
print(final_df.to_string())
final_df.to_excel('C:\\Users\paolo\\Documents\\conti\\Unicredit\\EstrattoContoUnicredit_2023_06_30.xlsx',
                  sheet_name='estratto_conto')
