from article_scraper import ArticleScraper
from article import Article

class CorriereDellaSeraScraper(ArticleScraper):
    location = "https://www.corriere.it"
    encoding = "iso-8859-1"

    def extract_articles(self, parser):
        news_blocks = parser.select(".bck-media-news")
        return filter(None, map(self.extract_article, news_blocks))

    def extract_article(self, block):
        title = block.find(class_="title-art-hp")
        subtitle = block.find(class_="subtitle-art")

        if title and subtitle:
            return Article(title.text, subtitle.text)

        return None
