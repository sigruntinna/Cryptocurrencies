from scrapy import Item, Field

# Code from: https://www.datasciencecentral.com/profiles/blogs/scraping-reddit

class RedditItem(Item):
    subreddit = Field()
    link = Field()
    title = Field()
    date = Field()
    vote = Field()
    top_comment = Field()
