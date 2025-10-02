from bs4 import BeautifulSoup
import requests
import pandas as pd
from dataclasses import dataclass

# Create Stock, Position, and Portfolio classes
@dataclass
class Stock:
    ticker: str
    exchange: str
    price: float = 0
    currency: str = "USD"
    price_usd: float = 0

    def __post_init__(self):
        price_info = get_price_info(self.ticker, self.exchange)

        if price_info["ticker"] == self.ticker:
            self.price = price_info["price"]
            self.currency = price_info["currency"]
            self.price_usd = price_info["price_usd"]

@dataclass
class Position:
    stock: Stock
    quantity: int

@dataclass
class Portfolio:
    positions: list[Position]

    def get_total_value(self):
        total_value = 0
        for position in self.positions:
            total_value += position.stock.price_usd * position.quantity
        return total_value
    

def get_fx_to_usd(currency):
    response = requests.get(f'https://www.google.com/finance/quote/{currency}-USD')
    clean_html = BeautifulSoup(response.content, "html.parser")
    fx_rate_div = clean_html.find('div', attrs= {"data-last-price": True})
    fx_rate = float(fx_rate_div["data-last-price"])
    return fx_rate

def get_price_info(ticker, exchange):
    response = requests.get(f'https://www.google.com/finance/quote/{ticker}:{exchange}')
    clean_html = BeautifulSoup(response.content, "html.parser")
    price_div = clean_html.find('div', attrs={"data-last-price": True})
    price = float(price_div["data-last-price"])
    currency = price_div["data-currency-code"]

    price_usd = price
    if currency != "USD":
        fx_rate = get_fx_to_usd(currency)
        price_usd = round(price * fx_rate, 2)

    return {"ticker": ticker, 
            "exchange": exchange, 
            "price": price, 
            "currency": currency, 
            "price_usd": price_usd,}


if __name__ == "__main__":
    shop = Stock("SHOP", "TSE") # CAD
    msft = Stock("MSFT", "NASDAQ") # USD
    googl = Stock("GOOGL", "NASDAQ")
    bns = Stock("BNS", "TSE")

    positions = [Position(shop, 10),
                 Position(msft, 2),
                 Position(bns, 100),
                 Position(googl, 30)]

    portfolio = Portfolio(positions)
    print (portfolio)
    print(portfolio.get_total_value())


