import re
from bs4 import BeautifulSoup

from scrapy import Spider, Request
from items import RedditItem

class RedditSpider(Spider):
    name = 'reddit'
    allowed_domains = ['reddit.com']
    start_urls = ['https://www.reddit.com/r/circlejerk',
                    'https://www.reddit.com/r/gaming',
                    'https://www.reddit.com/r/floridaman',
                    'https://www.reddit.com/r/movies',
                    'https://www.reddit.com/r/science',
                    'https://www.reddit.com/r/seahawks',
                    'https://www.reddit.com/r/totallynotrobots',
                    'https://www.reddit.com/r/uwotm8',
                    'https://www.reddit.com/r/videos',
                    'https://www.reddit.com/r/worldnews']

def parse(self, response):
    links = response.xpath('//p[@class="title"]/a[@class="title may-blank "]/@href').extract()
    titles = response.xpath('//p[@class="title"]/a[@class="title may-blank "]/text()').extract()
    dates = response.xpath('//p[@class="tagline"]/time[@class="live-timestamp"]/@title').extract()
    votes = response.xpath('//div[@class="midcol unvoted"]/div[@class="score unvoted"]/text()').extract()
    comments = response.xpath('//div[@id="siteTable"]//a[@class="comments may-blank"]/@href').extract()

    for i, link in enumerate(comments):
        item = RedditItem()
        print(item)
        item['subreddit'] = str(re.findall('/r/[A-Za-z]*8?', link))[3:len(str(re.findall('/r/[A-Za-z]*8?', link))) - 2]
        item['link'] = links[i]
        item['title'] = titles[i]
        item['date'] = dates[i]
        if votes[i] == u'\u2022':
            item['vote'] = 'hidden'
        else:
            item['vote'] = int(votes[i])

        request = Request(link, callback=self.parse_comment_page)
        request.meta['item'] = item
        yield request

def parse_comment_page(self, response):
    item = response.meta['item']
    top = response.xpath('//div[@class="commentarea"]//div[@class="md"]').extract()[0]
    top_soup = BeautifulSoup(top, 'html.parser')
    item['top_comment'] = top_soup.get_text().replace('\n', ' ')

    yield item
