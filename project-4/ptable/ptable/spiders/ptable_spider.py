import scrapy
from ptable.items import PtableItem
from scrapy.loader import ItemLoader
from scrapy_playwright.page import PageMethod

class PtableSpiderSpider(scrapy.Spider):
    name = "ptable_spider"
    allowed_domains = ["pubchem.ncbi.nlm.nih.gov"]
    start_urls = ["https://pubchem.ncbi.nlm.nih.gov/ptable/"]

    def start_requests(self):
        yield scrapy.Request('https://pubchem.ncbi.nlm.nih.gov/ptable', meta=dict(
            playwright=True,
            playwright_page_methods=[
                PageMethod("wait_for_selector", "div.ptable"),
            ],
        ))
    
    
    def parse(self, response):
        for element in response.css("div.ptable div.element"):
            i = ItemLoader(item=PtableItem(), selector=element)
            i.add_css('symbol', '[data-tooltip="Symbol"]')
            i.add_css('name', '[data-tooltip="Name"]')
            i.add_css('atomic_number', '[data-tooltip="Atomic Number"]')
            i.add_css('atomic_mass', '[data-tooltip*="Atomic Mass"]')
            i.add_css('chemical_group', '[data-tooltip="Chemical Group Block"]')
            yield i.load_item()
