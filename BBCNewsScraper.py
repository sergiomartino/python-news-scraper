from ArticleScraper import ArticleScraper
from Article import Article

class BBCNewsScraper(ArticleScraper):
    location = "https://www.bbc.co.uk/news"
    
    def extract_articles(self, parser):
        articles = parser.select(".gs-c-promo-heading")
        return list(dict.fromkeys(
            filter(None, map(self.extract_article, articles))
        ))

    def extract_article(self, block):
        title = block.getText()

        if title:
            return Article(title)

        return None