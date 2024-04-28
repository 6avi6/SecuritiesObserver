import pandas as pd

# Wczytanie danych z plików
base_df = pd.read_csv('base.csv')
user_df = pd.read_csv('user_account.csv')

# Wybierz maksymalne daty dla każdej nazwy papieru wartościowego
max_dates = base_df.groupby('paper name').agg({
    'date sec': 'max',          # Maksymalna data
    'price': 'last',            # Ostatnia cena
}).reset_index()

# Połącz dane z plików na podstawie nazwy papieru wartościowego i maksymalnej daty
merged_df = pd.merge(user_df, max_dates, on='paper name')


# Usunięcie kolumny 'page_alias'
merged_df.drop(columns=['page alias','page url id'], inplace=True)

merged_df['date_sec_x'] = pd.to_datetime(merged_df['date sec_x'], unit='s').dt.strftime('%Y-%m-%d %H:%M')

# Konwersja kolumny 'date_sec_y' na format daty
merged_df['date_sec_y'] = pd.to_datetime(merged_df['date sec_y'], unit='s').dt.strftime('%Y-%m-%d %H:%M')


# Obliczenie aktualnej wartości posiadanych akcji
merged_df['purchase value'] = merged_df['price_x'] * merged_df['amount']
merged_df['current value'] = merged_df['price_y'] * merged_df['amount']
merged_df['return percentage'] = (merged_df['current value'] *100/ merged_df['purchase value'])-100
merged_df['profit'] =(merged_df['current value']- merged_df['purchase value'])* merged_df['amount']



print(merged_df)
# Wyświetl zestawienie cen z aktualną zawartością portfela użytkownika
# Zmiana nazw kolumn
merged_df.rename(columns={'price_x': 'purchase price', 'price_y': 'current price'}, inplace=True)
merged_df.rename(columns={'date_sec_x': 'purchase date', 'date_sec_y': 'current date'}, inplace=True)

print(merged_df[['paper name', 'purchase price','current price', 'amount','purchase value', 'current value','return percentage','profit']])

# Zapisanie DataFrame do pliku CSV (tworzenie pliku, jeśli nie istnieje)
merged_df.to_csv('raport.csv', index=False, mode='w')
