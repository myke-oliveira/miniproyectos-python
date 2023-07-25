#! /usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import sqlite3
from datetime import datetime
from sys import argv

ecommerces = [
    {
        'name': 'Mercado Livre',
        'url': 'https://www.mercadolivre.com.br/',
        'search_selector': '.nav-search-input',
        'title_selector': '.shops__item-title',
        'price_selector': 'span.andes-money-amount.ui-search-price__part.shops__price-part.andes-money-amount--cents-superscript',
        'link_selector': '.ui-search-item__group__element shops__items-group-details ui-search-link'
    },
    {
        'name': 'Shopee Brasil',
        'url': 'https://shopee.com.br/',
        'search_selector': '.shopee-searchbar-input__input',
        'title_selector': '.lNepqa',
        'price_selector': '.juCMSo',
        'link_selector': ''
    },
    {
        'name': 'Amazon',
        'url': 'https://www.amazon.com.br/',
        'search_selector': '#twotabsearchtextbox',
        'title_selector': 'h2.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-4',
        'price_selector': '.s-price-instructions-style a:first-child span:first-child .a-offscreen',
        'link_selector': 'h2.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-4 a',
    },
    {
        'name': 'Magazine Luiza',
        'url': 'https://www.magazineluiza.com.br/',
        'search_selector': '#input-search',
        'title_selector': '[data-testid="product-title"]',
        'price_selector': '[data-testid="price-value"]',
        'link_selector': '[data-testid="product-card-container"]',
    }
]

def main():
    word = ' '.join(argv[1:])
    today = datetime.today().strftime('%Y-%m-%d')
    
    data_base = DataBase()
    data_base.connect()

    with webdriver.Edge() as driver:
        wait = WebDriverWait(driver, 5)
        web_scrapper = WebScrapper(driver, wait)
        for ecommerce in ecommerces:
            print('='*80)
            print(ecommerce["name"].center(80))
            print('='*80)
            try:
                web_scrapper.visit(ecommerce)
                web_scrapper.search(ecommerce, word)
                quotations = web_scrapper.get_info(ecommerce)
                data_base.insertMany(quotations, today)
            except TimeoutException:
                print("Timout on find an element")
            except StaleElementReferenceException:
                print("Another error has occured")
                
    data_base.disconnect()


class WebScrapper():
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def visit(self, ecommerce):
        self.driver.get(ecommerce['url'])

    def search(self, ecommerce, word):
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ecommerce['search_selector'])))
        search_input = self.driver.find_element(By.CSS_SELECTOR, ecommerce['search_selector'])
        search_input.send_keys(word + Keys.ENTER)

    def get_info(self, ecommerce):
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ecommerce['title_selector'])))
        titles_elements = self.driver.find_elements(By.CSS_SELECTOR, ecommerce['title_selector'])
        prices_elements = self.driver.find_elements(By.CSS_SELECTOR, ecommerce['price_selector'])
        titles = list(map(lambda title_element: title_element.text, titles_elements))
        prices = list(map(lambda price_element: price_element.text, prices_elements))

        if len(titles) != len(prices):
            return []
        return list(map(lambda d: { 'product_name': d[0], 'price': d[1] }, zip(titles, prices)))


class DataBase():
    def connect(self):
        self.connection = sqlite3.connect('webscrapping.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS quotations (product_name, price, date)')
    
    def disconnect(self):
        self.connection.close()
        
    def insertMany(self, quotations, date):
        data = ((quotation['product_name'], quotation['price'], date) for quotation in quotations)
        self.cursor.executemany('INSERT INTO quotations VALUES (?, ?, ?)', data)
        self.connection.commit()

if __name__ == '__main__':
    main()
