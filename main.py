from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Specifying incognito mode as you launch your browser[OPTIONAL]
option = webdriver.ChromeOptions()
#option.add_argument("--incognito")

# Create new Instance of Chrome in incognito mode
browser = webdriver.Chrome()

# Go to desired website
browser.get("https://allnashvillelistings.com/neighborhood-city/32862")

# Wait 20 seconds for page to load
timeout = 20
try:
    # Wait until the final element [Avatar link] is loaded.
    # Assumption: If Avatar link is loaded, the whole page would be relatively loaded because it is among
    # the last things to be loaded.
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='location-text']")))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()
city_element = browser.find_elements_by_xpath("//span[@class='bold']")

# List Comprehension to get the actual repo titles and not the selenium objects.
city = [x.text for x in city_element]

# print response in terminal
print('city:')
print(city, '\n')