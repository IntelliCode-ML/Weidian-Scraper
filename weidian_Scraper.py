"""
Weidian Product Scraper

This module provides functionality to scrape product information from Weidian e-commerce platform.
It uses Selenium with undetected-chromedriver to handle dynamic content and anti-bot measures.

Dependencies:
    - selenium
    - undetected-chromedriver
    - pandas
    - time
    - random
    - os
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import undetected_chromedriver as uc
import os


def scrape_product(driver):
    """
    Scrapes detailed product information from a Weidian product page.
    
    Args:
        driv    er: Selenium WebDriver instance
        product_link (str): URL of the product page to scrape
        
    Returns:
        dict: Dictionary containing product information including:
            - name: Product name
            - price: Product price
            - image: Main product image URL
            - Color variants: List of variant images and their prices
    """
    wait = WebDriverWait(driver, 40)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "goods-info-name")))
    time.sleep(2)  # Wait for the page to load completely

    try:
        name = driver.find_element(By.CLASS_NAME, "goods-info-name").text
        print(f"Product name: {name}")
    except Exception as e:
        print("Error getting product name:", e)
        name = None

    try:
        price = driver.find_element(By.CSS_SELECTOR, ".price-num.flex").text
        print(f"Product price: {price}")
    except Exception as e:
        print("Error getting product price:", e)
        price = None

    try:
        image_elem = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "big-icture"))
        ).find_element(By.TAG_NAME, 'img')

        image = image_elem.get_attribute("src")
        print(f"Product image URL: {image}")
    except Exception as e:
        print("Error getting product image:", e)
        image = None

    try:
        li = driver.find_elements(By.CSS_SELECTOR, ".prop-list.list-prop")[2].find_elements(By.TAG_NAME, 'li')
        driver.execute_script("arguments[0].click();", li[0])
        image_prices = []
        varient_img_divs = driver.find_elements(By.CSS_SELECTOR, '.prop-item.el-tooltip__trigger.el-tooltip__trigger')

        for varient_img_div in varient_img_divs:
            driver.execute_script("arguments[0].click();", varient_img_div)
            img_price = driver.find_element(By.CSS_SELECTOR, ".price-num.flex").text
            image_prices.append(img_price)

        varient_img = [varient_img_div.find_element(By.TAG_NAME, 'img').get_attribute('src') for varient_img_div in varient_img_divs]

    except Exception as e:
        print("Error getting color variants:", e)
        varient_img = []
        img_price = None

    data = {
        "name": name,
        "price": price,
        "image": image
    }
    # Add each variant image as a separate column
    for idx, img_url in enumerate(varient_img, 1):
        data[f"Color Variant {idx}"] = [ img_url , image_prices[idx - 1]]
    return data

def main(Links):
    """
    Main function to scrape multiple Weidian product links and export data to Excel.
    
    Args:
        Links (list): List of Weidian product URLs to scrape
        
    Returns:
        pandas.DataFrame: DataFrame containing all scraped product information
        
    The function:
    1. Initializes a headless Chrome browser
    2. Scrapes each product link
    3. Processes the data to handle varying numbers of color variants
    4. Exports the results to an Excel file named 'product_variants.xlsx'
    """
    options = uc.ChromeOptions()
    # options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    driver = uc.Chrome(options=options)

    excel_data = []
    
    for link in Links:
        driver.get(link)
        data = scrape_product(driver, link)
        excel_data.append(data)

    max_color_variants = 0
    for item in excel_data:
        count = len([k for k in item.keys() if k.lower().startswith("color")])

        if count > max_color_variants:
            max_color_variants = count

    print(f"Maximum number of color variants found: {max_color_variants}")

    # Process the data
    processed_data = []
    for item in excel_data:
        print(f"Processing item: {item['name']}")
        row = {
            "Name": item['name'],
            "Price": item['price'],
            "Base Image": item['image']
        }
        for i in range(1, max_color_variants + 1):
            key = f"Color Variant {i}"
            if key in item:
                row[f"Variant {i} Image"] = item[key][0]
                row[f"Variant {i} Price"] = item[key][1]
            else:
                row[f"Variant {i} Image"] = None
                row[f"Variant {i} Price"] = None
        processed_data.append(row)
    df = pd.DataFrame(processed_data)
    # Export to Excel
    output_path = os.path.join(os.path.dirname(__file__), "product_variants.xlsx")
    df.to_excel(output_path, index=False)
    print(f"Data exported to {output_path}")

    return df


# main(['https://loongbuy.com/product-details?invitecode=T6RNZP68&weidian=7236745589', 'https://loongbuy.com/product-details?url=https://weidian.com/item.html?itemID=7455742830'])  # Replace with the actual product link
