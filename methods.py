import json

from db import cursor, connection
import pandas as pd

df = pd.read_csv('target_data.csv')


def commit_to_db():
    connection.commit()


def create_products_json_from_csv():
    document = {}
    categories = []
    products = []

    for row in df.iloc:
        category_name = row['primary_category']
        category = get_category(category_name)
        if category is None:
            category = create_category(row['main_image'], row['primary_category'])
        name = row['title']
        image_url = row['main_image']
        description = row['description']
        price = round(float(row['price']) * 750)

        product = {
            "name": name,
            "imageUrl": image_url,
            "description": description,
            "categoryId": category,
            "price": price
        }
        product_id = create_product(category_id=category, image_url=image_url,
                                    description=description, name=name, price=price)
        product['id'] = product_id
        images = row['images'].split("|")
        urls = create_product_images(images, product_id)
        product['images'] = urls
        categories.append(category)
        products.append(product)
    document['products'] = products
    document['categories'] = categories
    output = open('products.json', 'w')
    json.dump(document, output, indent=4)


def get_category(category_name):
    category_fetch_id = f"""
        SELECT id FROM Category WHERE name='{category_name}'
        """
    cursor.execute(category_fetch_id)
    results = cursor.fetchall()
    if len(results) < 1:
        return None
    return results[0][0]


def create_category(image_url, name):
    category_insert_statement = f"""
        INSERT INTO Category (imageUrl, name) VALUES (%s, %s) RETURNING id;
        """
    values = (image_url, name)
    cursor.execute(category_insert_statement, values)
    inserted_id = cursor.fetchone()[0]
    return inserted_id


def create_product(category_id, image_url, name, description, price):
    product_insert_statement = f"""
    INSERT INTO Product (imageUrl, name, description, price, categoryId) 
    VALUES (%s, %s, %s, %s, %s) 
    RETURNING id;
    """
    values = (image_url, name, description, price, category_id)
    cursor.execute(product_insert_statement, values)
    inserted_id = cursor.fetchone()[0]
    return inserted_id


def create_product_images(image_urls, product_id):
    image_ids = []
    for image_url in image_urls:
        product_image_insert_statement = f"""
            INSERT INTO ProductImage (imageUrl, productId) 
            VALUES (%s, %s) RETURNING id;
            """
        values = (image_url, product_id)
        cursor.execute(product_image_insert_statement, values)
        inserted_id = cursor.fetchone()[0]
        image_ids.append(inserted_id)
    return image_urls
