import undetected_chromedriver as uc
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
from weidian_Scraper import scrape_product
import csv

def save_to_csv(data, filename='products.csv'):
    """
    Save a list of dictionaries to a CSV file.

    Args:
        data (list): List of dictionaries containing product data.
        filename (str): Name of the CSV file to save. Default is 'products.csv'.
    """
    # Define the fieldnames (column headers) for the CSV
    fieldnames = ['name', 'price', 'image']

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header
            writer.writeheader()

            # Write all the data rows
            writer.writerows(data)

        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving to CSV: {e}")


class WebDriver:

    @staticmethod
    def driver():
        options = uc.ChromeOptions()
        # options.add_argument('--headless')  # Run in headless mode
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        driver = uc.Chrome(options=options)
        return driver


class SearchProduct:
    def __init__(self):
        self.base_url = "https://loongbuy.com/"
        self.driver = WebDriver.driver()
        self.driver.get(self.base_url)

    def search_bar(self, keyword:str):
        search_input = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Product link or name / Store link']"))
        )
        if search_input:
            search_input.send_keys(keyword)
            search_input.clear()
            search_input.send_keys(Keys.RETURN)

    import time

    def scroll_page(self, scroll_pause_time=5, max_scrolls=10):
        """
        Scrolls down the page to load dynamic content.

        Args:
            driver: Selenium WebDriver instance.
            scroll_pause_time: Seconds to wait after each scroll.
            max_scrolls: Number of times to scroll down.
        """
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        for i in range(max_scrolls):
            print(f"Scrolling... ({i + 1}/{max_scrolls})")
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(scroll_pause_time)

            # Calculate new scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            # Check if page height has changed
            if new_height == last_height:
                print("Reached end of page.")
                break
            last_height = new_height

    def scrape_products(self):
        # Wait for at least one product to be present, then find all products
        WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".goods-item")))
        product_elements = self.driver.find_elements(By.CSS_SELECTOR, ".goods-item")

        products = []
        for element in product_elements:
            try:
                image_url = element.find_element(By.CSS_SELECTOR, ".img-box img").get_attribute("src")
            except:
                image_url = None

            try:
                name = element.find_element(By.CSS_SELECTOR, ".text-box p").text
            except:
                name = None

            try:
                price = element.find_element(By.CSS_SELECTOR, ".text-box span").text
            except:
                price = None

            products.append({
                "name": name,
                "price": price,
                "image": image_url,
            })
        return products

if __name__ == '__main__':
    search_product = SearchProduct()
    search_product.search_bar("shoes")
    search_product.scroll_page(max_scrolls=10)
    products = search_product.scrape_products()
    save_to_csv(products)
    time.sleep(30)
