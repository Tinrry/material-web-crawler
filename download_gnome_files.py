import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


# driver = webdriver.Firefox()

def login(driver):
  driver.get("https://profile.materialsproject.org/connect/portier")
  email = input("Wait till the login page is ready and then input the email address: ")
  elem = driver.find_element(By.NAME, "login_hint")
  elem.send_keys(email)
  elem.send_keys(Keys.RETURN)
  code = input("Wait till the email is recieved and input the code in the email: ")
  elem = driver.find_element(By.NAME, "code")
  elem.send_keys(code)
  elem.send_keys(Keys.RETURN)
  time.sleep(20) # Wait


def download(driver, url):
  try:
    driver.get(url)
    # Tried WebDriverWait+EC but this hardcoded wait seems to be more consistent smh.
    time.sleep(10) # Wait for webpage to load
    elements = driver.find_elements(By.CLASS_NAME, 'mpc-button-bar')
    b = elements[0].find_elements(By.CLASS_NAME, 'dropdown-trigger')[-1].find_elements(By.XPATH, 'button')[0]
    b.send_keys(Keys.ENTER)
    time.sleep(2) # Wait for webpage to response
    elements[0].find_elements(By.CLASS_NAME, "dropdown-content")[0].find_elements(By.XPATH, "div")[-1].click()
    time.sleep(2) # Wait for webpage to response
  except Exception as e:
    with open('error-1.log', 'a') as file:
      file.write(f"{url}\n")
    # refresh the page
    driver.refresh()
    print(f"Error downloading {url}: {e}")
    
  return

def read_file(abs_file):
  with open(abs_file, 'r') as file:
    lines = file.readlines()
  url_list = list(map(lambda x: x.rsplit(':', 1)[0], lines))
  return url_list

from selenium.webdriver.firefox.options import Options
from tqdm import tqdm

if __name__ == "__main__":
  # ofter a 1000+ files, firefox lost connection
  url_list = read_file('error.log')
  # snap in ubuntu, the profile is not loaded properly
  firefox_options = Options()
  firefox_options.add_argument("-profile")
  firefox_options.add_argument("/home/zhenghuanhuan/snap/firefox/common/.mozilla/firefox")      # Path to myserver profile
  driver = webdriver.Firefox(options=firefox_options)

  login(driver)
  # 增加进度条
  for url in tqdm(url_list, desc="Downloading files"):
    download(driver, url)
  driver.quit()
