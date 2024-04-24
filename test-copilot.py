from selenium import webdriver
import json
import time

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()
url = 'https://www.matweb.com/Search/MaterialGroupSearch.aspx?GroupID=178'
# Navigate to the desired website
driver.get('https://www.matweb.com/Search/MaterialGroupSearch.aspx?GroupID=178')

# TODO we need to login and save the cookies
# Get the cookies from the current session
cookies = driver.get_cookies()

# Save the cookies as JSON
with open('./cookies.json', 'w') as file:
    json.dump(cookies, file)

# Close the browser
driver.quit()

# Open the desired website using Selenium
driver = webdriver.Chrome()
driver.get('https://www.matweb.com/Search/MaterialGroupSearch.aspx?GroupID=178')

# Load the cookies from the JSON file
with open('./cookies.json', 'r') as file:
    cookies = json.load(file)

# Add the cookies to the current session
for cookie in cookies:
    driver.add_cookie(cookie)

# Refresh the page to apply the cookies
driver.refresh()
time.sleep(20)

# Continue with the rest of your code
# ...
