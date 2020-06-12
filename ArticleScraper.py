from abc import ABC, abstractmethod

class ArticleScraper(ABC):
    encoding = "utf-8"
    
    @property
    @abstractmethod
    def location(self):
        raise Exception("location property must be defined")

    @abstractmethod
    def extract_articles(parser): 
        raise Exception("extract_articles method must be defined")
