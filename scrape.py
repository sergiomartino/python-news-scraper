import cherrypy
import requests
from argparse import ArgumentParser
from importlib import import_module
from bs4 import BeautifulSoup
from mako.template import Template
from dataclasses import dataclass
from article import Article

class Scraper(object):

    @cherrypy.expose
    def index(self):
        tpl = Template(filename="./scrape.tpl")
        scraper = self.get_scraper()
        page = requests.get(scraper.location)
        parser = self.get_parser(scraper, page.text)
        return tpl.render(attrs={"articles": scraper.extract_articles(parser) })

    def get_parser(self, scraper, text):
        try:
            text = bytes(text, scraper.encoding)
        except Exception as error:
            print(error)
            text = ""

        return BeautifulSoup(text, "html.parser")

    def get_scraper(self):
        argument_parser = ArgumentParser()
        argument_parser.add_argument('--scraper')
        args = argument_parser.parse_args()
        imported_module = import_module("scrapers")
        ScraperClass = getattr(imported_module, args.scraper + "Scraper")
        return ScraperClass()


cherrypy.config.update({
    "tools.staticdir.on": True,
    "tools.staticdir.dir": "/"
})

cherrypy.quickstart(Scraper())
