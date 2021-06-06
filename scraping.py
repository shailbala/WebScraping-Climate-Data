
from selenium import webdriver
## https://www.tutorialspoint.com/python_web_scraping/python_web_scraping_dynamic_websites.htm

## browser = webdriver.Firefox()
path = r'/usr/local/bin/'
driver = webdriver.Firefox()
#driver = webdriver.Firefox(executable_path=path)

m = [1,2,3,4,5]
month = "/historic?month="
year = "&year=2021"
cityNames = []
cityUrls = []

with open('city_urls.txt') as file:
    l = file.readlines()
    for line in l:
        cityUrls.append(line.strip("\n"))

with open('city_names.txt') as file:
    l = file.readlines()
    for line in l:
        cityNames.append(line.strip("\n"))


## for each month, get data for each city, store it in format:
## cityname+month
for mon in m:
    for i in range(len(cityUrls)):
        url = cityUrls[i]
        driver.get(url+month+str(mon)+year)
        driver.implicitly_wait(220) #maximum time to load the link
        script_text = driver.find_element_by_xpath("//section[@class='headline-banner__wrap']//script[2]").get_attribute('textContent')
        ## write to new file
        file = open(cityNames[i]+str(mon), 'w')
        file.write(script_text)
        file.close()

## we can use ID of the search toolbox for setting the element to select.
#driver.find_element_by_id('search_term').send_keys('.')
## find elements by class
## driver.find_element_by_class_name('weatherLinks')

## only one section with this class, contains two scripts
## 2nd one we need to save
## element = driver.find_element_by_class_name('headline-banner__wrap')
#script_text = driver.find_element_by_xpath("//script[contains(.,'\"copyright\"')]").text
#script_text = driver.find_element_by_xpath("//section[@class='headline-banner__wrap']//script[2]").text

#print(type(script_text))
#print(len(script_text))


driver.close()
