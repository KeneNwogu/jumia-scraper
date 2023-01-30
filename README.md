# Jumia Web Scraper README

## Introduction
This web scraper scrapes data from an e-commerce website and saves it into two tables, "Product" and "Category".

## Prerequisites
- Python 3 installed
- Access to the command line/terminal

## Usage
1. Create a ".env" file and use the ".env.example" file to set up your database configuration
2. Drop your "Product" and "Category" tables:
3. Install dependencies from requirements.txt:
```sh
> pip install requirements.txt
```
4. Run the scraper:
```sh
> python scraper.py
```


## Output
The scraper creates about 12 categories and 318 products. The data will be saved into the "Product" and "Category" tables.

## Note
Please note that the number of categories and products may change over time as the website updates its content.

