# Weidian Product Scraper

A powerful and user-friendly tool for scraping product information from Weidian e-commerce platform. This project includes both a command-line scraper and a graphical user interface (GUI) for easy interaction. 

Note: This code scrapes loongbuy.com to scrap weidian.com as it has more features to scrap.

## Features

- Scrapes detailed product information including:
  - Product name
  - Price
  - Main product image
  - Color variants with their respective images and prices
- Handles multiple product URLs in batch
- Exports data to Excel format
- User-friendly GUI interface
- Built-in error handling and loading indicators
- Anti-bot detection measures

## Prerequisites

- Python 3.7 or higher
- Chrome browser installed
- Required Python packages (install using `pip install -r requirements.txt`):
  - selenium
  - undetected-chromedriver
  - pandas
  - tkinter (usually comes with Python)

## Installation

1. Clone this repository:
```bash
git clone [repository-url]
cd weidian-scraper
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### GUI Application

1. Run the GUI application:
```bash
python GUI.py
```

2. Enter Weidian product links in the text box (one per line)
3. Click "Submit" to start the scraping process
4. Wait for the process to complete
5. The results will be saved as `product_variants.xlsx` in the same directory

### Command Line Usage

You can also use the scraper directly from Python:

```python
from weidian_Scraper import main

links = [
    'https://weidian.com/item.html?itemID=1234567890',
    'https://weidian.com/item.html?itemID=0987654321'
]

df = main(links)
```

## Output Format

The scraper generates an Excel file (`product_variants.xlsx`) with the following columns:
- Name: Product name
- Price: Product price
- Base Image: Main product image URL
- Variant X Image: URL for each color variant image
- Variant X Price: Price for each color variant

## Error Handling

The application includes comprehensive error handling for:
- Invalid URLs
- Network issues
- Missing product information
- Browser automation failures

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational purposes only. Please ensure you comply with Weidian's terms of service and robots.txt when using this scraper. 