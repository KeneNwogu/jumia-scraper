import re

import requests
from bs4 import BeautifulSoup
from db import cursor, connection
from psycopg2 import sql

index = "https://www.jumia.com.ng"
response = requests.get(index)


def get_categories_from_index():
    category_links = []

    soup = BeautifulSoup(response.content, features='html5lib')
    menu = soup.find_all("div", class_="itm -pvs _v")
    for item in menu:
        tag = list(item.children)[0]
        children = list(tag.children)
        name = children[-1].string
        image_url = list(children[0].children)[0].get('data-src')
        category_link = tag.get('href')
        category_fetch_id = f"""
            SELECT id FROM Category WHERE name='{name}'
            """
        cursor.execute(category_fetch_id)
        results = cursor.fetchall()
        if len(results) > 0:
            continue
        category_insert_statement = f"""
        INSERT INTO Category (imageUrl, name) VALUES ('{image_url}', '{name}')
        """
        cursor.execute(category_insert_statement)
        category_links.append((category_link, name))
    connection.commit()
    return category_links


categories = get_categories_from_index()
# for each category, add to db and fetch 10 products from category


def fetch_products_from_category(category_link):
    link, category_name = category_link
    # get category id
    category_fetch_id = f"""
    SELECT id FROM Category WHERE name='{category_name}'
    """
    cursor.execute(category_fetch_id)
    results = cursor.fetchall()
    print(results)
    r = requests.get(link)
    soup = BeautifulSoup(r.content, features='html5lib')
    products = soup.find('div', class_='-paxs row _no-g _4cl-3cm-shs').children

    for product in products:
        product_children = list(product.children)
        product_link = product_children[0]
        product_div = list(product_link.children)[0]

        product_info = list(product_link.children)[1]
        product_name = list(product_info.children)[0].string

        product_img = list(product_div.children)[0]
        product_image_url = product_img.get('data-src')

        if product_name == "Official Store":
            continue

        image_parent = product_img.parent.parent
        price_container = list(image_parent.children)[1]
        price = list(price_container.children)[1].text
        next_link = index + image_parent.get('href')
        try:
            price_string = re.search(r"₦ ([0-9]+,[0-9]+)", price).group(1)
        except AttributeError:
            continue

        description_page = requests.get(next_link)
        description_page_soup = BeautifulSoup(description_page.content, features='html5lib')
        description = []
        try:
            description = list(map(lambda x: x.text, description_page_soup.find(class_='markup -pam')
                                   .find_all('li')))
        except AttributeError:
            pass

        description_text = "\n".join(description)

        product_insert_statement = f"""
        INSERT INTO Product (imageUrl, name, description, price, categoryId) VALUES ('{product_image_url}',
        '{str(product_name).replace("'", "''")}', '{str(description_text).replace("'", "''")}', 
        '{price_string.replace(",", "")}', 
        '{results[0][0]}')
        """
        try:
            cursor.execute(product_insert_statement)
            connection.commit()
        except:
            continue


for category in categories:
    fetch_products_from_category(category)
