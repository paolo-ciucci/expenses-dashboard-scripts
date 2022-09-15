import pandas as pd
df = pd.read_excel('C:\\Users\\paolo\\Documents\\conti\\Hype\\Lista_movimenti_2018_hype.xlsx')
Total = df['Importo'].sum()
expenses = df[df['Importo'] < 0]['Importo'].sum()
gains = df[df['Importo'] > 0]['Importo'].sum()

print(Total)
print(expenses)
print(gains)
# print(df.to_string())