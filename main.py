import scrapy
from scrapy.crawler import CrawlerProcess

import pandas as pd
from colorama import Fore, Back, Style

import time

def pInfo(text):
    print(Fore.BLUE + text + Style.RESET_ALL)

import subprocess
# Ścieżka do pliku skryptu, który chcesz uruchomić
other_script_path = "cookiesReader.py"

# Uruchomienie innego skryptu
#subprocess.run(["python", other_script_path])
time.sleep(2)

sharesTable = pd.read_csv('base.csv')
pagesTabe= pd.read_csv('pages_url.csv')

merged_df=pd.merge(sharesTable,pagesTabe,left_on="page url id",right_on="id",how="inner")
pInfo("DB Loaded")

#print(merged_df)

from datetime import datetime
def filter_out_today_rows(data_frame):
    
    # Convert date_sec column to datetime objects
    data_frame['date sec'] = pd.to_datetime(data_frame['date sec'], unit='s')

    # Get today's date
    today = datetime.today().date()

    # Filter out rows with today's date
    filtered_df = data_frame[data_frame['date sec'].dt.date != today]

    return filtered_df



#print(not_today_db)

import cookie as c  # Importuj ciasteczka bezpośrednio z pliku Pythona



class MySpider(scrapy.Spider):

    name = 'Spider'
    not_today_db=filter_out_today_rows(merged_df)
    start_urls = [(index, url) for index, url in enumerate((not_today_db['address url'] + not_today_db['page alias']).astype(str).to_numpy())]
    print(start_urls)
    def start_requests(self):
        cookies = c.cookies  # Use cookies directly
        for index, url in self.start_urls:
            yield scrapy.Request(url, cookies=cookies, callback=self.parse, meta={'index': index})

    #function that update courses
    def parse(self, response):
        global sharesTable 
        index = response.meta['index']
        paper_name = merged_df.loc[index, 'paper name']
        kurs_text = response.xpath('//table[@id="t1"]//td[1]//span[1]/text()').get()
 
        if kurs_text:    
            new_row = {
                'paper name': paper_name,
                'price': kurs_text,  # Assuming kurs_text represents the price
                'date sec': int(time.time()),
                'page url id': merged_df.loc[index, 'page url id'],  # You didn't specify page_url_id in the provided info
                'page alias': merged_df.loc[index, 'page alias']  # You didn't specify page_alias in the provided info
            }
            print(new_row)
            pInfo("- _przeszło -")
            # Add the new row to sharesTable using .loc accessor
            #sharesTable.loc[len(sharesTable)] = new_row
            
            
            #print(f"Index: {index}, Paper Name: {paper_name}, Kurs: {kurs_text} ,Time:{int(time.time())}")
            
   



# Run the spider
process = CrawlerProcess(settings={
    # 'FEED_FORMAT': 'csv',  # Format wyjściowy
    # 'FEED_URI': 'output.csv',
     'LOG_ENABLED': False,
    # 'AUTOTHROTTLE_ENABLED': False 
})

process.crawl(MySpider)
pInfo("- _ -")
process.start()
print(sharesTable)
sharesTable.to_csv('base.csv', index=False)
#show current
import currentTime
currentTime.printTime()