import pandas as pd
from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser

def extract_full_body_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state("networkidle")
        page.evaluate("() => window.scroll(0, document.body.scrollHeight)")
        page.wait_for_timeout(3000)
        html = page.content()
        browser.close()
        return html

def extract_values(html):

    games = []

    tree = HTMLParser(html)
    cards = tree.css("div[class*='ImpressionTracked']")
    
    for card in cards:
        # Title
        title_el = card.css_first("div.StoreSaleWidgetTitle")
        title = title_el.text(strip=True) if title_el else None

        # Thumbnail
        thumb_el = card.css_first("div.CapsuleImageCtn img")
        thumbnail = thumb_el.attributes.get("src") if thumb_el else None

        # Categories (platforms, etc.)
        category_els = card.css("a[class*='WidgetTag']")[:5]
        categories = [a.text(strip=True) for a in category_els] if category_els else []
        
        # Release date
        release_el = card.css_first("div._1qvTFgmehUzbdYM9cw0eS7")
        release_date = release_el.text(strip=True) if release_el else None

        # Rating (if present)
        rating_el = card.css_first("div.rating")  # adjust selector for actual site
        rating = rating_el.text(strip=True) if rating_el else None

        # Number of reviews (if present)
        reviews_el = card.css_first("span.review-count")  # adjust selector
        num_reviews = reviews_el.text(strip=True) if reviews_el else None
        
        # Price
        orig_el = card.css_first("div.StoreSalePriceWidgetContainer > div:first-child")
        original_price = orig_el.text(strip=True) if orig_el else None
        disc_el = card.css_first("div.StoreSalePriceWidgetContainer > div:last-child")
        discounted_price = disc_el.text(strip=True) if disc_el else None
        pct_el = card.css_first("div.StoreSalePriceWidgetContainer > div:first-child")
        discount_pct = pct_el.text(strip=True) if pct_el else None

        # Collect into dict
        games.append({
            "title": title,
            "thumbnail": thumbnail,
            "categories": categories,
            "release_date": release_date,
            "rating": rating,
            "num_reviews": num_reviews,
            "original_price": original_price,
            "discounted_price": discounted_price,
            "discount_pct": discount_pct
        })
    
    games_df = pd.DataFrame(games)
    return games_df

if __name__ == "__main__":
    url = "https://store.steampowered.com/specials/"
    html = extract_full_body_html(url)
    print(extract_values(html))
    extract_values(html).to_csv("steam_sales3.csv", index=False)



## values needed:
## 1. title
## 2. link to thumbnail
## 3. category tags
## 4. release_date
## 5. rating
## 6. number of reviews
## 7. original price
## 8. discounted price
## 9. discount percentage

