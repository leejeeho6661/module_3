import scrapy
from module_03.items import Module03Item
import requests
from bs4 import BeautifulSoup


class MybotsSpider(scrapy.Spider):
    name = 'mybots'
    # custom_settings = {'JOBDIR': 'crawl_mybots1'}
    allowed_domains = ['www.imdb.com/chart/boxoffice/?ref_=nv_ch_cht']
    start_urls = ['https://www.imdb.com/chart/boxoffice/?ref_=nv_ch_cht']

    def parse(self, response):
        
        title = response.xpath('//*[@id="boxoffice"]/table/tbody/tr/td[2]/a/text()').extract()
        weekend = response.xpath('//*[@id="boxoffice"]/table/tbody/tr/td[3]/text()').extract()
        gross = response.xpath('//*[@id="boxoffice"]/table/tbody/tr/td[4]/span/text()').extract()
        weeks = response.xpath('//*[@id="boxoffice"]/table/tbody/tr/td[5]/text()').extract()
        # print('----------------',title,'----------------')
        # print('----------------',weekend,'----------------')
        # print('----------------',gross,'----------------')
        # print('----------------',weeks,'----------------')

        items = []
        cnt = 0
        for idx in zip(title,weekend,gross,weeks):
            item = Module03Item()
            item['title'] = idx[0]
            item['weekend'] = idx[1].replace(" ","").replace("\n","")
            item['gross'] = idx[2]
            item['weeks'] = idx[3]

            url = 'https://www.imdb.com/chart/boxoffice/?ref_=nv_ch_cht'
            response = requests.get(url)
            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                tbody = soup.select_one(".chart.full-width > tbody")
                titles = tbody.select(".titleColumn > a")
                
                new_url = 'https://www.imdb.com'+titles[cnt]['href']+'/?ref_=cht_bo_'+str(cnt+1)
                new_response = requests.get(new_url)
                cnt+=1
                response = requests.get(url)
                if new_response.status_code == 200:
                    html = new_response.text
                    soup = BeautifulSoup(html, 'html.parser')
                    rating = soup.select_one('div.ratingValue > strong')['title'].split(' ')[0]
                    item['rating'] = rating
                    people = soup.select_one('div.ratingValue > strong')['title'].split(' ')[3]
                    item['people'] = people
                    tmps = soup.select('div.subtext > a')
                    genre = ''
                    release = ''
                    new_cnt = 0
                    for tmp in tmps:
                        if new_cnt != (len(tmps)-1):
                            genre += tmp.get_text().strip()+" "
                        else:
                            release += tmp.get_text().strip()
                        new_cnt+=1
                    item['genre'] = genre = genre.strip()
                    item['movie_release'] = release
            items.append(item)
        

        return items

