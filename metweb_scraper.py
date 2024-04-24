import scrapy
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

import re
import pandas as pd
import os
import time
import flask
import unicodedata

from flask import request, jsonify


class met_web(scrapy.Spider):
    name="metweb"

    weather={}
    def start_requests(self):
        start_url=['https://www.matweb.com/Search/MaterialGroupSearch.aspx?GroupID=178']    # ASTM Steel
        #start_url=['http://www.matweb.com/search/QuickText.aspx?SearchText=AA7075']
        #start_url = ['http://www.matweb.com/search/QuickText.aspx?SearchText=AA5083']
        #start_url = ['http://www.matweb.com/search/QuickText.aspx?SearchText=AA7150']
        #start_url =['http://www.matweb.com/search/QuickText.aspx?SearchText=AA1235']
        for url in start_url:
            yield scrapy.Request(url=url, callback=self.parse)




    #'//div[@id='details']/div/div[@class='day muted']/div/div/h4'

    def parse(self, response):
        #start_url=['https://www.accuweather.com/en/pk/lahore/260622/daily-weather-forecast/260622?day=1']
        print('parse is checking')

        # material_name=response.xpath("//table[@id='tblResults']/tr/th[3]/a/text()").extract_first()
        # print('\n materials names :',material_name)
        #

        #####################Extract Composition######################################
        for resp in response.xpath("//table[@id='tblResults']/tr"):#//div[@id='feed-tabs']#//div[@id='details']/div/div[@class='day muted']
            #print(quote)


            composition_link=resp.xpath("td[3]/a/@href").extract_first()
            #print('\n composition  Row ',composition)


            if composition_link:

                composition_url='http://www.matweb.com'+composition_link
                print('\n URL is ',composition_url)
                start_url = [composition_url]

                for url in start_url:
                    yield scrapy.Request(url=url, callback=self.parse_2)
                    break
            else:
                print('empty cell', composition_link)


    def parse_2(self,response):
        print('#######Link 2 ########')
        url=response.request.url

        title=response.xpath("//table[@class='tabledataformat t_ableborder tableloose altrow']/tr/th/text()").extract_first()
        title = title.strip().replace('/','-')

        print('\n title is ',title)
        folder_path = os.getcwd()
        folder_path=folder_path+'/'+title
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        folder_path=folder_path+'/'
        detail = {'URL': [url], 'Title': [title]}
        detail_file =pd.DataFrame(data=detail)
        csv_file = folder_path + title + '.csv'
        if not os.path.exists(csv_file):
            detail_file.to_csv(csv_file,sep=',', encoding='utf-8',index=False)



if __name__ == '__main__':

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(met_web)
    process.start()
