import time
import pickle

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def save_cookies(driver, path):
    with open(path, 'wb') as f:
        pickle.dump(driver.get_cookies(), f)
def load_cookies(driver, path):
    with open(path, 'rb') as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)

url = 'https://www.matweb.com/search/DataSheet.aspx?MatGUID=e5e92a1ae7f24e1b918bf4e65dbc7e52'

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

cookies = load_cookies(driver, 'cookie')
# driver.add_cookie({'name': 'zhenghuanhuan@zhejianglab.com', 'value': 'zhijiang2893161'})
driver.get(url = 'https://www.matweb.com/search/DataSheet.aspx?MatGUID=e5e92a1ae7f24e1b918bf4e65dbc7e52')
# # element = driver.find_element(By.ID, value='#ctl00_ContentMain_ucDataSheet1_pnlIQY')
# # element.click()
time.sleep(100)
driver.close()
#ctl00_ContentMain_ucDataSheet1_pnlIQY
#ctl00_ContentMain_ucDataSheet1_pnlIQY > a
#ctl00_ContentMain_ucDataSheet1_pnlIQY > a > small
# gotit = driver.get_downloadable_files()
# driver.find_element(by='xpath',value="//*[@id='ctl00_ContentMain_ucDataSheet1_pnlIQY_Unregistered']/a/small").click()