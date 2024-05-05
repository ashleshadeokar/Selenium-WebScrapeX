# WebScrapeX: Automating Data Extraction from Dynamic Websites with Selenium

This Python script utilizes Selenium to scrape data from a website. It automates the process of navigating through web pages, inputting data, and extracting desired information.

## Prerequisites
- Python 3.x
- Selenium WebDriver (Microsoft Edge version)
- Microsoft Edge WebDriver (msedgedriver.exe)

## Setup
1. Install Python from python.org.
2. Install Selenium: `pip install selenium`
3. Download the Microsoft Edge WebDriver.
4. Update edge_driver_path variable in the script with the path to msedgedriver.exe.

## Usage
1. Run the script: python web_scraping.py.
2. The script will navigate to a specific website and perform actions like login, inputting dates, selecting categories, and clicking buttons to scrape data.
3. Extracted data will be saved to a CSV file named salesdata.csv in the same directory.

## Script Overview
- The script uses Selenium WebDriver to automate web browsing.
- It navigates to a specific website, logs in, and performs actions to access desired data.
- Data extraction is done using CSS selectors to locate elements containing the required information.
- Extracted data is stored in a CSV file for further analysis or processing.
