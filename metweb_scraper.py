from pprint import pprint

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

        #start_url=['http://www.matweb.com/search/QuickText.aspx?SearchText=AA7075']
        #start_url = ['http://www.matweb.com/search/QuickText.aspx?SearchText=AA5083']
        #start_url = ['http://www.matweb.com/search/QuickText.aspx?SearchText=AA7150']
        #start_url =['http://www.matweb.com/search/QuickText.aspx?SearchText=AA1235']
        start_url=['http://www.matweb.com/search/QuickText.aspx?SearchText=AA2618']     # this is for test not actual url
        for url in start_url:
            yield scrapy.Request(url=url, callback=self.parse)

# # todo debug descriptor need to locate the head_ck

#         material_url = ['http://www.matweb.com/search/DataSheet.aspx?MatGUID=e5e92a1ae7f24e1b918bf4e65dbc7e52']
#         for url in material_url:
#             yield scrapy.Request(url=url, callback=self.parse_2)


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
            else:
                print('empty cell', composition_link)


    def parse_2(self,response):
        print('#######Link 2 ########')
        url=response.request.url

        title=response.xpath("//table[@class='tabledataformat t_ableborder tableloose altrow']/tr/th/text()").extract_first()
        title = title.strip().replace('/','-')

        print('\ntitle is :',title)
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
        ####################Physical property header_end ########################################################
        d = {'col1': ['URL'], 'col2': [url], 'col3': ['Title'], 'col4': [title]}

        df = pd.DataFrame(data=d)
        table_title = ''
        table_title_reminder = True
        for resp in response.xpath(
                "//table[@class='tabledataformat']/tr"):  # //div[@id='feed-tabs']#//div[@id='details']/div/div[@class='day muted']
            header_ck = resp.xpath("tr[2]/th[1]/text()").extract_first()
            #  //*[@id="ctl00_ContentMain_ucDataSheet1_pnlMaterialData"]/table[2]/tbody/tr[2]/th[1]
            print('header_contain : ', header_ck)

            if header_ck:

                if table_title_reminder == True:
                    table_title = header_ck
                    table_title_reminder = False

                physical_property = resp.xpath("th[1]/text()").extract_first()
                metrix = resp.xpath("th[2]/text()").extract_first()
                english = resp.xpath("th[3]/text()").extract_first()
                comments = resp.xpath("th[4]/text()").extract_first()
                pprint(physical_property, metrix, english, comments)
                # if (metrix != 'None' and english != 'None'):
                #     print('\n physical property is ',physical_property,metrix,english,comments)
                #     d = {'col1': physical_property, 'col2': metrix, 'col3': english, 'col4': comments}
                #
                #     df = df.append(d, ignore_index=True)

            else:
                print('some thing unexpected happened')

        print('\n ############### Dataframe is######################')
        file_name=title+".csv"
        print(df)
        file_name = folder_path+table_title+".csv"
        df.drop(df.index[0],inplace=True)
        df.to_csv(file_name, sep=',', header=False,index=False)

if __name__ == '__main__':

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(met_web)
    process.start()
