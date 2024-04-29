import pandas as pd

# Load data from files
base_df = pd.read_csv('base.csv')         # Read data from the 'base.csv' file
user_df = pd.read_csv('user_account.csv') # Read data from the 'user_account.csv' file

# Select maximum dates for each stock paper name
max_dates = base_df.groupby('paper name').agg({
    'date sec': 'max',   # Maximum date
    'price': 'last',     # Last price
}).reset_index()

# Merge data from files based on stock paper name and maximum date
merged_df = pd.merge(user_df, max_dates, on='paper name')


# Drop the 'page_alias' column
merged_df.drop(columns=['page alias','page id'], inplace=True)

# Convert 'date_sec_x' column to date format
merged_df['date_sec_x'] = pd.to_datetime(merged_df['date sec_x'], unit='s').dt.strftime('%Y-%m-%d %H:%M')

# Convert 'date_sec_y' column to date format
merged_df['date_sec_y'] = pd.to_datetime(merged_df['date sec_y'], unit='s').dt.strftime('%Y-%m-%d %H:%M')

# Calculate the current value of owned stocks
merged_df['purchase value'] = merged_df['price_x'] * merged_df['amount']
merged_df['current value'] = merged_df['price_y'] * merged_df['amount']
merged_df['return percentage'] = ((merged_df['current value'] * 100) / merged_df['purchase value']) - 100
merged_df['profit'] = (merged_df['current value'] - merged_df['purchase value']) * merged_df['amount']



# Display a summary of prices with the current contents of the user's portfolio
# Rename columns
merged_df.rename(columns={'price_x': 'purchase price', 'price_y': 'current price'}, inplace=True)
merged_df.rename(columns={'date_sec_x': 'purchase date', 'date_sec_y': 'current date'}, inplace=True)

print(merged_df[['paper name', 'purchase price','current price', 'amount','purchase value', 'current value','return percentage','profit']])

# Save the DataFrame to a CSV file (create the file if it doesn't exist)
merged_df.to_csv('report.csv', index=False, mode='w')
