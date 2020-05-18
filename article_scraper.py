from abc import ABC, abstractmethod

class ArticleScraper(ABC):
    encoding = "utf-8"
    
    @property
    @abstractmethod
    def location(self):
        pass

    @abstractmethod
    def extract_articles(parser): 
        pass
