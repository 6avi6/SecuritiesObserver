import scrapy
from scrapy.crawler import CrawlerProcess

import pandas as pd
from colorama import Fore, Back, Style

import time
from datetime import datetime

def pInfo(text):
    print(Fore.BLUE + text + Style.RESET_ALL)

import subprocess
#Path to cookies reader
other_script_path = "cookiesReader.py"
#Script to run cookies reader it s important to have updated cookies because scraper without of them can't read data properly!!!
#subprocess.run(["python", other_script_path])
time.sleep(2)

sharesTable = pd.read_csv('base.csv')
pagesTabe= pd.read_csv('pages_url.csv')
portfolio= pd.read_csv('user_account.csv')
#Checekin if there are stocks from user portolio
# Find paper names in portfolio not present in sharesTable
missing_paper_names = set(portfolio["paper name"]) - set(sharesTable["paper name"])
# Filter portfolio to get the missing rows
missing_rows = portfolio[portfolio["paper name"].isin(missing_paper_names)]
# Select only the required columns
missing_rows_subset = missing_rows[["paper name", "price", "date sec", "page id"]]

 # Rename the column "page id" to "page url id"
missing_rows_subset.rename(columns={"page id": "page url id"}, inplace=True)


# Append the missing rows to sharesTable it s use when user adds new paper to account
for index, row in missing_rows_subset.iterrows():
    new_row = {
        'paper name': row["paper name"],
        'price': row["price"],
        'date sec': row["date sec"],
        'page url id': row["page url id"],
    }
    sharesTable.loc[len(sharesTable)] = new_row

temp_merged_df=pd.merge(portfolio,pagesTabe,left_on="page id",right_on="id",how="inner")

new_df = temp_merged_df.loc[:, ["paper name", "page alias", "id", "address url"]]
# Perform the join operation to have table with aliases and adresses so scraper knows link to page of securites
merged_df = pd.merge(new_df, sharesTable, left_on=["paper name", "id"], right_on=["paper name", "page url id"], how="inner")

pInfo("DB Loaded")


def filter_out_today_rows(df):
    # Convert 'date sec' to datetime values
    df['date sec'] = pd.to_datetime(df['date sec'], unit='s')
    
    # Initialize the result DataFrame
    result = pd.DataFrame(columns=df.columns)
    
    # Iterate through unique "paper name"
    for paper_name in df['paper name'].unique():
        # Filter records from the original DataFrame for a given "paper name" and the maximum date
        max_date_sec = df[df['paper name'] == paper_name]['date sec'].max()
        group_records = df[(df['paper name'] == paper_name) & (df['date sec'] == max_date_sec)]
        
        # Iterate through each record in the group
        for _, record_row in group_records.iterrows():
            # Check if the date is not today
            if record_row['date sec'].date() != datetime.now().date():
                # Create a new row
                new_row = {
                    'paper name': paper_name,  # Use the "paper name" obtained from the iteration
                    'page alias': record_row['page alias'],
                    'address url': record_row['address url'],
                    'price': record_row['price'],
                    'date sec': int(time.time()),  # Current time as date sec
                    'page url id': record_row['page url id'],
                }
                
                # Add the new row to the result DataFrame using .loc
                result.loc[len(result)] = new_row

    return result

import cookie as c #import cookies from file

class MySpider(scrapy.Spider):

    name = 'Spider'
    not_today_db = filter_out_today_rows(merged_df)
    #assembling links for data that isn t updated
    start_urls = [(index, url, paper_name) for index, url, paper_name in zip(
        range(len(not_today_db)),
        (not_today_db['address url'] + not_today_db['page alias']).astype(str).to_numpy(),
        not_today_db['paper name']
    )]

    #scraping data from links with coookies from file cookie.py
def start_requests(self):
    # Load cookies from file cookie.py
    from cookie import cookies  # Import cookies from file

    # Iterate over start URLs
    for index, url, paper_name in self.start_urls:
        # Make request with cookies
        yield scrapy.Request(
            url,
            cookies=cookies,  # Use cookies obtained from the file
            callback=self.parse, #Using Parse func
            meta={'index': index, 'paper_name': paper_name}  # Pass additional metadata
        )

    # function that update courses & adding founded results to sharesTable
    def parse(self, response):
        global sharesTable 
        index = response.meta['index']
        paper_name = response.meta['paper_name']  # Access the paper_name from meta
        # extracting from stooq.pl
        if merged_df.loc[index, 'page url id'] == 1:
            kurs_text = response.xpath('//table[@id="t1"]//td[1]//span[1]/text()').get()

        if kurs_text:
            #printing name of new price of securities
            pInfo(paper_name)  
            new_row = {
                'paper name': paper_name, 
                'price': kurs_text,  #new price
                'date sec': int(time.time()),
                'page url id': merged_df.loc[index, 'page url id'],  
            }
            
            # Add the new row to sharesTable using .loc accessor
            sharesTable.loc[len(sharesTable)] = new_row
            print(new_row)
            #print(f"Index: {index}, Paper Name: {paper_name}, Kurs: {kurs_text} ,Time:{int(time.time())}")

            
            
   



# Run the spider

#hiding logs of spider 
process = CrawlerProcess(settings={
     'LOG_ENABLED': False#if you want to se logs comment this line

})

process.crawl(MySpider)
process.start()
print("Base table:")
print(sharesTable)

#writing updated data
sharesTable.to_csv('base.csv', index=False)
