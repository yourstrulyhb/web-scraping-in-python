"""
   SP Spider
   A single-page Web Scraper in Python      
   by yourstrulyhb

   Get name, links, and pricing
   of portfolio themes mentioned in https://blog.hubspot.com/website/wordpress-portfolio-theme

   Produces:
   - HTML file of webpage
   - CSV file of data
"""

import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import date
import re
import pandas as pd


class SinglePageSpider(scrapy.Spider):
   name = 'Anna'
   webpage_title = "temp_title"
   filename = "temp_file"


   def set_filename(self, response):
      """ Creates a filename from current data and webpage title

      :param response: a Response object

      Return: a filename in lowercase with underscores format
      """
      today = date.today()
      title = response.css('html > head > title::text').extract()[0]
      self.webpage_title = title.strip().lower().replace(" ", "_")

      self.filename =  str(today) + '__' + self.webpage_title


   def save_to_csv(self, df: pd.DataFrame, filename: str):
      df.to_csv(filename + ".csv")


   
   def custom_scrape(self, response):
      #! Modify XPath or CSS selectors here!
      # TODO: Get portfolio theme name, links, prices
      
      theme_names = response.css('span#hs_cos_wrapper_post_body > h3 > a::text').extract()
      print(f'>>> Theme names: {len(theme_names)}')

      theme_links = response.css('span#hs_cos_wrapper_post_body > h3 > a::attr(href)').extract()
      print(f'>>> Theme links: {len(theme_links)}')

      theme_prices = response.xpath('//span[@id="hs_cos_wrapper_post_body"]/p/strong[contains(text(), "Pricing")]/..').extract()
      print(f'>>> Theme prices: {len(theme_prices)}')
      
      # Clean theme_prices data: remove text style tags <p>, <strong>, <em>
      for i in range(len(theme_prices)):
         theme_prices[i] = re.sub(r"<.*?>", "", theme_prices[i])
         theme_prices[i] = theme_prices[i].replace("Pricing:", "").replace(",", ";") # r".{1}<.?/.+[a-z].{1}>"


      # Input data to Dataframe
      data = {'name': theme_names,
               'link': theme_links,
               'price': theme_prices}

      df = pd.DataFrame(data, columns=['name', 'link', 'price'])
      print(df.head(5))

     
      self.save_to_csv(df = df, filename = self.filename)


   #! Scraping starts here
   def start_requests(self):
      start_urls = ['https://blog.hubspot.com/website/wordpress-portfolio-theme']
      
      for url in start_urls:
         yield scrapy.Request(url = url, callback = self.parse) # Create Response object, call back parse function


   def parse(self, response):
      """ Parses HTML (response object).
            Saves HTML content to a file.

      :param response: A Response object
      """

      self.set_filename(response)


      html_filename = self.filename + '.html'
      with open(html_filename, 'wb') as fout:
         fout.write(response.body)

      print(f">>> Saved webpage content to {html_filename}")


      # Start scraping! Customize scraping code in custom_scrape function
      self.custom_scrape(response)


    
if __name__ == '__main__':

   process = CrawlerProcess()
   process.crawl(SinglePageSpider)
   process.start()

