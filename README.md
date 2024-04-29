# SecuritiesObserver
The application is designed to display current stock prices, compare them with the user's portfolio, and present a summary of gains and losses. Additionally, it allows for displaying charts of stocks purchased by the user.

# :clipboard: How to Use the Program 

To effectively operate the program, follow these steps:

1. **Run the "cookiesReader.py" Script:** Start by executing the "cookiesReader.py" script. This script is essential for data scraping and ensures that no cookie files are accepted after script initialization.

2. **Fill in the "user_account.csv" File:** Populate the "user_account.csv" file with your owned stocks, adhering to the provided example content.

3. **Execute the "cookiesReader.py" Script:** Once the "user_account.csv" file is updated, run the "cookiesReader.py" script to refresh the stock data.

4. **Generate Report to CSV File:** Utilize the "portfolioSummary.py" script to generate a report into a CSV file. This script extracts data from both the "user_account.csv" and "baze.csv" files, containing comprehensive stock data over time.

5. **Utilize the "dataVisualization.py" File:** For data visualization, employ the "dataVisualization.py" script. It facilitates the creation of charts for each stock present in the database.

# :heavy_plus_sign: Additional Information
The SecuritiesObserver project is designed to display current stock prices, compare them with the user's portfolio, and present a summary of gains and losses. By default, it retrieves data from the stooq.pl website. To extend its functionality to read from other websites, the code would need to be adapted accordingly.

# :notebook: License 

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for the full text of the license.
