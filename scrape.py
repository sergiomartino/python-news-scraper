import requests
from bs4 import BeautifulSoup
import cherrypy
from mako.template import Template
from dataclasses import dataclass

class Scraper(object):

    @dataclass
    class Article:
      title: str
      subtitle: str

    @cherrypy.expose
    def index(self):  
        tpl = Template(filename="./scrape.tpl")
        page = requests.get("https://www.corriere.it")
        parser = self.get_parser(page.text)
        articles = filter(lambda b: b, map(self.extract_article, parser.select(".bck-media-news")))

        ctx = {
            "articles": articles
        }

        return tpl.render(attrs=ctx)

    def extract_article(self, block):
      title = block.find(class_="title-art-hp")
      subtitle = block.find(class_="subtitle-art")

      if title and subtitle:
        return self.Article(title.text, subtitle.text) 

      return None

    def get_parser(self, text):
        try:
          text = bytes(text, 'iso-8859-1')
        except Exception as error:
          print(error)
          text = ""

        return BeautifulSoup(text, "html.parser")


cherrypy.config.update({
    "tools.staticdir.on": True,
    "tools.staticdir.dir": "c:/repos/python/scraping"
})

cherrypy.quickstart(Scraper())
