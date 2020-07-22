from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import csv


csv_file = open('amazon.csv', 'w', encoding='utf-8', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['title', 'rating', 'price', 'sponsored', 'form'])

# Windows users need to specify the path to chrome driver you just downloaded.
# You need to unzip the zipfile first and move the .exe file to any folder you want.
driver = webdriver.Chrome(r'C:\Users\TRW\chromedriver.exe')
# driver = webdriver.Chrome()


# Go to the page that we want to scrape
# url_list = []
# for url in url_list:
# 	driver.get(url)


#driver.get("https://www.amazon.com/s?k=improve+my+life")
#driver.get("https://www.amazon.sg/s?k=improve+my+life")

# Expand Department List

url_list = []
main = "https://www.amazon."
countries = ["com/au", "ca", "in", "sg", "ae", "co.uk", "com"]
search = "/s?k=improve+my+life"
for country in countries:
	url_list.append(main+country+search)

for url in url_list:
	driver.get(url)

	try:
		expand_buttons = driver.find_elements_by_xpath('//span[@class="a-expander-prompt"]')
		for button in expand_buttons:
			button.click()
	except:
		pass

	# Total Search Results
	search_results = driver.find_element_by_xpath('//div/span[@dir="auto"]').text
	search_results += " " + driver.find_element_by_xpath('//div//span[@class="a-color-state a-text-bold"]').text.strip("\"")

	print(url)
	print(search_results)
	print('+'*79)

	results = driver.find_elements_by_xpath('//div[@data-component-type="s-search-result"]')
	for result in results:
		result_dict = {}
		try:
			title = result.find_element_by_xpath('.//span[@class="a-size-base-plus a-color-base a-text-normal"]').text
		except:
			title = None
		try:
			rating = result.find_element_by_xpath('.//div[3]/div/span[1]').get_attribute('aria-label')[:3]
			rating = float(rating)
		except:
			rating = None
		try:
			price = result.find_element_by_xpath('.//span/span[@class="a-price-symbol"]').text
			price += result.find_element_by_xpath('.//span/span[@class="a-price-whole"]').text
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

		result_dict['title'] = title
		result_dict['rating'] = rating
		result_dict['price'] = price
		result_dict['sponsored'] = sponsored
		result_dict['form'] = form
		
		csv_writer.writerow(result_dict.values())



	#price = result.find_element_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]/div[2]/div/span/div/div/div[4]/div[2]/div/a/span/span[1]').text
	#print(price)

# ids = driver.find_elements_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]/div[1]')
# list_ids = []
# for i in ids:
# 	list_ids.append(i.get_attribute('id'))

# print(list_ids)


#depts = driver.find_elements_by_xpath 
#depts = 
#sub_depts = driver.find_elements_by_xpath('//li[@class="a-spacing-micro s-navigation-indent-1"]')

# Page index used to keep track of where we are.
#index = 1
# We want to start the first two pages.
# If everything works, we will change it to while True
# while True:
# 	try:
# 		element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
# 								"myDynamicElement"))








	# 	print("Scraping Page number " + str(index))
	# 	index = index + 1
	# 	# Find all the reviews. The find_elements function will return a list of selenium select elements.
	# 	# Check the documentation here: http://selenium-python.readthedocs.io/locating-elements.html
	# 	reviews = driver.find_elements_by_xpath('//div[@class="row border_grayThree onlyTopBorder noSideMargin"]')
	# 	# Iterate through the list and find the details of each review.
	# 	for review in reviews:
	# 		# Initialize an empty dictionary for each review
	# 		review_dict = {}
	# 		# Use try and except to skip the review elements that are empty. 
	# 		# Use relative xpath to locate the title.
	# 		# Once you locate the element, you can use 'element.text' to return its string.
	# 		# To get the attribute instead of the text of each element, use 'element.get_attribute()'
	# 		try:
	# 			title = review.find_element_by_xpath('.//div[@class="NHaasDS75Bd fontSize_12 wrapText"]').text
	# 		except:
	# 			continue

	# 		print('Title = {}'.format(title))

	# 		# OPTIONAL: How can we deal with the "read more" button?
			
	# 		# Use relative xpath to locate text, username, date_published, rating.
	# 		# Your code here

	# 		# Uncomment the following lines once you verified the xpath of different fields
			
	# 		# review_dict['title'] = title
	# 		# review_dict['text'] = text
	# 		# review_dict['username'] = username
	# 		# review_dict['date_published'] = date_published
	# 		# review_dict['rating'] = rating

	# 	# We need to scroll to the bottom of the page because the button is not in the current view yet.
	# 	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

	# 	# Locate the next button element on the page and then call `button.click()` to click it.
	# 	button = driver.find_element_by_xpath('//li[@class="nextClick displayInlineBlock padLeft5 "]')
	# 	button.click()
	# 	time.sleep(2)

	# except Exception as e:
	# 	print(e)
	# 	driver.close()
	# 	break