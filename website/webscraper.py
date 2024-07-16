import requests
from bs4 import BeautifulSoup

def search(query):
    url = f"https://www.amazon.com/s?k={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Referer': 'https://www.amazon.com/',
        'DNT': '1'  
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve content: {response.status_code}")
        return []

    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    product_containers = soup.find_all("div", class_="s-result-item")

    products = []
    for container in product_containers:
        product_name_element = container.find("span", class_="a-size-medium")
        product_link_element = container.find("a", class_="a-link-normal")
        product_price_element_whole = container.find("span", class_="a-price-whole")
        product_price_element_fraction = container.find("span", class_="a-price-fraction")
        product_image_element = container.find("img", class_="s-image")
        product_rating_element = container.find("span", class_="a-icon-alt")
        product_description_element = container.find("span", class_="a-size-base-plus")
        product_availability_element = container.find("span", class_="a-color-price")
        product_prime_element = container.find("i", class_="a-icon-prime")
        product_discount_element = container.find("span", class_="a-badge-text")
        product_seller_element = container.find("span", class_="a-size-small")

        if all([product_name_element, product_link_element, product_price_element_whole, product_price_element_fraction, product_image_element, product_rating_element]):
            product_name = product_name_element.text.strip()
            product_url = "https://www.amazon.com" + product_link_element['href']
            price_whole = product_price_element_whole.text.strip()
            price_fraction = product_price_element_fraction.text.strip()
            product_price = f"{price_whole}{price_fraction}"
            product_image = product_image_element["src"]
            product_rating = product_rating_element.text.strip().split()[0]
            product_ratings_number_element = container.find("span", class_="a-size-base")
            product_ratings_number = product_ratings_number_element.text.strip()
            product_description = product_description_element.text.strip() if product_description_element else "N/A"
            product_availability = product_availability_element.text.strip() if product_availability_element else "Available"
            product_prime = True if product_prime_element else False
            product_discount = product_discount_element.text.strip() if product_discount_element else "No discount"
            product_seller = product_seller_element.text.strip() if product_seller_element else "N/A"


            products.append({
                'name': product_name, 
                'url': product_url,
                'price': '$' + product_price,
                'image': product_image,
                'rating': product_rating + '/5',
                'ratings_number': product_ratings_number.replace(",", ""),
                'description': product_description,
                'availability': product_availability,
                'prime': product_prime,
                'discount': product_discount,
                'seller': product_seller,
            })

    return products







