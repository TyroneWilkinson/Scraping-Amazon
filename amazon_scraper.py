from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import csv

def search_result_finder(driver):
    """
    Scrapes the text depicting the total search results listed at the 
    top of Amazon's page.

    Parameter:
    driver: Chrome web driver pointing to page you want to scrape.

    Return:
    results (string): Text depicting the search results.
    """
    results = driver.find_element_by_xpath('//div/span[@dir="auto"]').text
    results += " " + driver.find_element_by_xpath('//div//span[@class="a-color-state a-text-bold"]').text.strip("\"")
    return results

# Prepare one .csv file.
csv_file1 = open('main_amazon.csv', 'w', encoding='utf-8', newline='')
csv_writer1 = csv.writer(csv_file1)
csv_writer1.writerow(['country', 'title', 'rating', 'price', 'sponsored', 'form']) 

# Windows users need to specify the path to chrome driver you just downloaded.
# You need to unzip the zipfile first and move the .exe file to any folder you want.
driver = webdriver.Chrome(r'C:\Users\TRW\chromedriver.exe')

# Prepare list of websites to visit.
url_list = []
main = "https://www.amazon."
#countries = ["com/au", "ca", "in", "sg", "ae", "co.uk", "com"]
countries = {"com.au":"Australia", "ca":"Canada", "in":"India", \
             "sg":"Singapore", "ae":"United Arab Emirates", \
             "co.uk":"United Kingdom", "com":"United States"}
search = "/s?k=improve+my+life"
for country in countries.keys():
    url_list.append(main+country+search)

for url in url_list:
    for country in countries.keys():
        if country in url:
            target_country = countries[country]
            break

    driver.get(url)

    # Expand Left-Pane Department List If Necessary 
    try: 
        expand_buttons = driver.find_elements_by_xpath('//span[@class="a-expander-prompt"]')
        for button in expand_buttons:
            button.click()
    except:
        pass

    # Total search results listed at the top of the page (string).
    search_results = search_result_finder(driver)   
    f = open(r'C:\Users\TRW\Documents\NYCDSA\Selenium\Web_Scraping_Project\main_search_results.txt', 'a')
    f.write(target_country+': '+search_results+'\n')
    f.close()

    pages = 10
    for page in range(pages):
        # Find all the results. The find_elements function will return a list of selenium select elements.
        # Check the documentation here: http://selenium-python.readthedocs.io/locating-elements.html
        default_results = driver.find_elements_by_xpath('//div[@data-component-type="s-search-result"]') # The block of site elements to iterate through
        # Iterate through the list and find the item results on the first page of each site.
        # using the "amazon_result_parser" function.
        for result in default_results:
            # Initialize an empty dictionary for each review
            result_dict = {}
            # Used try and except to skip the result elements that are empty. 
            # Used relative xpath to locate the needed elements.
            # Once elements are located, used 'element.text' to return its string.
            # To get the attribute instead of the text of each element, used 'element.get_attribute()'
            # NOTE: Pages which display '48' results vs '16' results per page are coded slightly differently. 
            if '48' in search_results:
                try:
                    title = result.find_element_by_xpath('.//span[@class="a-size-base-plus a-color-base a-text-normal"]').text
                except:
                    title = None
                try:
                    rating = result.find_element_by_xpath('.//div[3]/div/span[1]').get_attribute('aria-label')[:3]
                    rating = float(rating)
                except:
                    rating = None

            if '16' in search_results:
                try:
                    title = result.find_element_by_xpath('.//span[@class="a-size-medium a-color-base a-text-normal"]').text
                except:
                    title = None
                try:
                    rating = result.find_element_by_xpath('.//div[2]/div/span[1]').get_attribute('aria-label')[:3]
                    rating = float(rating)
                except:
                    rating = None
            try:
                price = result.find_element_by_xpath('.//span/span[@class="a-price-symbol"]').text
                price += result.find_element_by_xpath('.//span/span[@class="a-price-whole"]').text
                if "in" not in url: # Only India's site doesn't have fractional prices.
                    price += '.' + result.find_element_by_xpath('.//span/span[@class="a-price-fraction"]').text
            except:
                price = None
            try:    
                _ = result.find_element_by_xpath('.//span[@class="a-size-mini a-color-secondary"]').text
                sponsored = 1
            except:
                sponsored = 0
            try:
                form = result.find_element_by_xpath('.//a[@class="a-size-base a-link-normal a-text-bold"]').text
            except:
                form = None
            result_dict['country'] = target_country
            result_dict['title'] = title
            result_dict['rating'] = rating
            result_dict['price'] = price
            result_dict['sponsored'] = sponsored
            result_dict['form'] = form
            csv_writer1.writerow(result_dict.values())

        try:
            driver.find_element_by_xpath('//li[@class="a-last"]').click()
            time.sleep(3)
        except:
            break   
driver.close()