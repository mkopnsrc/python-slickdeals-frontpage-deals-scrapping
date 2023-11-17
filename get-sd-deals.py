# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import json
from html import unescape
import discord_hook

# scraper calss definition
class SlickDeals(scrapy.Spider):
    # spider name
    name = 'slickdeals'
    
    # base URL
    base_url = 'https://slickdeals.net'

    #settings={
    #    "FEEDS": {
    #        "items.json": {"format": "json"},
    #    },
    #}
    
    def words_strip(self, str):
        res = str.replace('about', '').replace('ago','').strip()
        #print(res)
        return res

    def convert_time_to_minutes(self, time_str):
        if 'day' in time_str:
            return int(time_str.split()[0]) * 24 * 60  # Convert days to minutes
        elif 'hour' in time_str:
            return int(time_str.split()[0]) * 60  # Convert hours to minutes
        elif 'minute' in time_str:
            if 'less than a minute' in time_str:
                return int(1)
            else:
                return int(time_str.split()[0])  # Extract minutes
    
    # crawler's entry point
    def start_requests(self):
        yield scrapy.Request(url=self.base_url, callback=self.parse)
            #break

    # parse content
    def parse(self, res):
        items = []
        cards = enumerate(res.css('ul.frontpageSlickdealsGrid').css('li.frontpageGrid__feedItem'),start=1)
        # loop over product cards
        for idx, card in cards:
            if card.css('a.dealCard__title::text').get() is not None:
                item = {
                    'title': unescape(card.css('a.dealCard__title::text').get()),
                    
                    'link': self.base_url + card.css('a.dealCard__title::attr(href)').get(),

                    'image_url': card.css('a.dealCard__imageContainer').css('img.dealCard__image::attr(src)').get().replace('200x200/','').replace('thumb','attach'),

                    'store': card.css('a.dealCard__storeLink::text').get().replace('\n', '').strip(),
                    
                    'price': '',
                    
                    'likes': card.css('span.dealCardSocialControls__voteCount::text').get(),

                    'time': self.words_strip(card.css('span.dealCard__statusTimestamp::text').get()),

                    'time_in_min': self.convert_time_to_minutes(self.words_strip(card.css('span.dealCard__statusTimestamp::text').get()))
                }
                
                # try to extract price
                try:
                    item['price'] = card.css('span.dealCard__price::text').get().replace('\n', '').strip()
                except Exception as e:
                    #print(e)
                    item['price'] = 'N/A'

                items.append(item)
                # store output results
                #yield items

            # End of If
        # End of For
        
        # Sort the data by time
        items = sorted(items, key=lambda x: self.convert_time_to_minutes(x['time']))
        
        # Search for dictionaries with a specific key-value time_in_min that has value less than 15 (minutes)
        search_results = [item for item in items if item.get("time_in_min") < 15]
            # print results to console
        print(json.dumps(search_results, indent=2))
        
        for item in search_results:
            # send items to discord webhook channel - hot-deals
            discord_hook.sendDiscordWebhook(item['title'],item['link'],item['image_url'],item['store'],item['price'],item['likes'])
        
        # Truncate the array variables
        items = None
        search_results = None

# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(SlickDeals)
    process.start()
    
    # debug selectors
    #SlickDeals.parse(SlickDeals, '')
