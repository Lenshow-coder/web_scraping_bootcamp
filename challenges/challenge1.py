from bs4 import BeautifulSoup
import requests
import pandas as pd

words_to_nums = {
    "Zero": 0, "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
}

response = requests.get("https://books.toscrape.com/")
clean_html = BeautifulSoup(response.text, "html.parser")

books = clean_html.select('article.product_pod')
book_data = []
for book in books:
    title = book.h3.a['title']
    price = book.select_one('p.price_color').text.strip()
    price = float(''.join(ch for ch in price if ch.isdigit() or ch == '.'))
    rating_class = book.select_one('p.star-rating')['class']# The rating is the second class, e.g., ['star-rating', 'Three']
    rating = words_to_nums[rating_class[1]] if len(rating_class) > 1 else None
    book_data.append({
        'title': title,
        'price': price,
        'rating': rating
    })

df = pd.DataFrame(book_data)
print(df.head(10))