from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select 
import time
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import csv

try:
    # Specify the path to the EdgeDriver executable
    edge_driver_path = 'msedgedriver.exe'

    # Setup the Selenium WebDriver
    service = Service(edge_driver_path)
    driver = webdriver.Edge(service=service)

    # Navigate to the website
    driver.get("https://ticketsales.com/login/")
    
    # Wait for the username field to be present
    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    
    # Find the password field and login button using the updated locator strategies
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.ID, 'login')

    # Input username and password
    username_field.send_keys('Email')
    password_field.send_keys('Password')
    
    # Click the login button
    login_button.click()
    time.sleep(10)
    
    # Function to extract sales data from an open listing
    def extract_sales_data():
        try:
            # Use a more specific selector to target the container for sales data
            sales_data_container = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[ng-repeat*='sale in marketdata.sales']"))
            )
            print("Sales data container found.")

            # List to store data dictionaries
            sales_data = []

            for row in sales_data_container:
                # Use the 'ng-binding' class which is common for all the data elements
                data_elements = row.find_elements(By.CSS_SELECTOR, ".ng-binding")
                
                # Make sure we have the expected number of elements before trying to extract data
                if len(data_elements) >= 4:
                    section = data_elements[0].text
                    quantity = data_elements[2].text  # Assuming the third ng-binding element is the quantity
                    date_time = data_elements[3].text  # Assuming the fourth ng-binding element is the date/time
                    price = data_elements[4].text  # Assuming the fifth ng-binding element is the price
                    
                    # Store the extracted data in a dictionary
                    sales_data.append({
                        "Section": section.strip(),
                        "Quantity": quantity.strip(),
                        "Date/Time": date_time.strip(),
                        "Price": price.strip()
                    })
                else:
                    print("Unexpected number of data elements found in a row.")

            #print(f"Extracted sales data: {sales_data}")
            return sales_data

        except Exception as e:
            print(f"An error occurred while extracting sales data: {e}")
            return []


    # URL of the page to scrape
    url = 'https://ticketsales.com/inventory/'

    # Wait for the page to load
    time.sleep(5)

    # Click on the '+' icon
    plus_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "i.glyphicon-plus")))
    plus_button.click()
    print("Add Inventory Clicked!!!")
    time.sleep(5)

    # Input the start date
    start_date = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'add_start_date')))
    start_date.clear()
    start_date.send_keys('04/26/2024')  # Replace with the desired start date
    print("start date selected.")

    # Input the end date
    end_date = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'add_end_date')))
    end_date.clear()
    end_date.send_keys('04/26/2024')  # Replace with the desired end date
    print("end date selected.")

    # Select the category from the dropdown
    category_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'add_eventcategory')))
    Select(category_select).select_by_visible_text('NBA')  # Replace with the actual category you want
    print("category selected.")

    # Click the search button
    search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[span[text()="Search"]]')))
    search_button.click()
    print("Search Clicked!")
    # Wait for search results to load
    time.sleep(5)

    csv_data = []

    # Wait for the search results to be visible
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[ng-repeat*='event in events']")))

    # Find all event containers
    events = driver.find_elements(By.CSS_SELECTOR, "div[ng-repeat*='event in events']")

    # List to store all sales data from all dollar signs
    all_sales_data = []

    for event in events:
        try:
            # Extract the event name from the event container
            event_name_div = event.find_element(By.CSS_SELECTOR, ".glyphicon-calendar").find_element(By.XPATH, "./..")
            event_name = event_name_div.text
            print(f"Event Name: {event_name}")

            # Find the dollar sign button within the event container
            dollar_sign_button = event.find_element(By.CSS_SELECTOR, "div[ng-click*='showSeatgeekPricing']")
            driver.execute_script("arguments[0].click();", dollar_sign_button)
            print("'$' clicked")
            time.sleep(5)  # Adjust as needed to ensure the page has loaded

            # Click on the sales tab if it is not already active
            sales_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[@ng-click=\"sg_mpd_viewmode = 'sales'\"]")))
            sales_tab.click()
            print("Sales tab clicked!")
            time.sleep(5)  # Adjust as needed to ensure the sales data has loaded

            # Extract sales data from the open listing
            sales_data = extract_sales_data()

            
            # Add the event name to each entry of sales data and add to the main list
            for sale in sales_data:
                sale['Event Name'] = event_name
                all_sales_data.append(sale)

            time.sleep(5)

        except Exception as e:
            print(f"No Data Found!: {e}")

     # Define CSV file location
    csv_file = 'salesdata.csv'  
    # Write the data to a CSV file
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Event Name', 'Section', 'Quantity', 'Date/Time', 'Price'])
        writer.writeheader()

        for data in all_sales_data:
            writer.writerow(data)
    print(f"Data has been written to {csv_file}")

except Exception as e:
    print("Error!!!")

