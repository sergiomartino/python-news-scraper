import cherrypy
import requests
from bs4 import BeautifulSoup
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
        articles = filter(None, map(self.extract_article, parser.select(".bck-media-news")))

        return tpl.render(attrs={ "articles": articles })

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
    "tools.staticdir.dir": "/"
})

cherrypy.quickstart(Scraper())
