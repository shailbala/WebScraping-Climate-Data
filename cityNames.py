
## scrape all cities/districts available and their url

from selenium import webdriver

driver = webdriver.Firefox()
driver.get('https://www.timeanddate.com/weather/india')
driver.implicitly_wait(220) #maximum time to load the link

## get all elements
elements = driver.find_elements_by_xpath('//table[@class="zebra fw tb-wt zebra va-m"]//tbody//tr//td//a')

print(type(elements))
## 377 results
print(len(elements))

city = []
url = []
for each in elements:
	city.append(each.text)
	url.append(each.get_attribute("href"))

with open('city_names.txt') as file:
	for each in city:
		file.write(each+"\n")

with open('city_names.txt', 'w') as file:
	for each in city:
		file.write(each+"\n")

driver.close()
