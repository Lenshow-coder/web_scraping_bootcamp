import re

import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


def remove_commas(value):
    return value.replace(",", "")


def try_int(value):
    try:
        return int(value)
    except ValueError:
        return value


def try_float(value):
    try:
        return float(value)
    except ValueError:
        return value


def extract_year(value):
    year = re.findall(r"\d{4}", value)

    if not year:
        return value

    return year


class CountryGdpItem(scrapy.Item):
    country_name = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    region = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    gdp = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, remove_commas, try_float),
        output_processor=TakeFirst()
    )
    year = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, extract_year, try_int),
        output_processor=TakeFirst()
    )
