import requests
import click
import time
import Article
from importlib import import_module
from bs4 import BeautifulSoup
from mako.template import Template


@click.command()
@click.option('--scraper')
def main(scraper):
    registered_scraper = get_scraper(scraper)
    page = requests.get(registered_scraper.location)
    parser = get_parser(registered_scraper, page.text)
    extract(registered_scraper.extract_articles(parser), registered_scraper.encoding)
    print("done!")

def extract(articles, encoding):
    tpl = Template(filename="scrape.tpl")
    text = tpl.render(attrs={ "articles": articles })
    file = open("screenshot.txt", "w", encoding=encoding) 
    file.write(text) 
    file.close() 

def get_parser(scraper, text):
    try:
        text = bytes(text, scraper.encoding)
    except Exception as error:
        print(error)
        text = ""

    return BeautifulSoup(text, "html.parser")

def get_scraper(scraper):
    try:
        name = scraper + "Scraper"
        module = import_module(name)
        return getattr(module, name)()
    except ModuleNotFoundError as error:
        print(error)

if __name__ == '__main__':
    main()