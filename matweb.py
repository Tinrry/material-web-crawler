import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def get_html(save_path, paper_url):
    # paper_url = "https://www.matweb.com/search/DataSheet.aspx?MatGUID=e5e92a1ae7f24e1b918bf4e65dbc7e52"

    chrome_options = Options()
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
    # chrome_options.add_argument('window-size=800x600')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--start-maximized')
    driver = webdriver.Chrome(chrome_options)

    driver.get(paper_url)
    print(driver.title)

    html = None

    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "form[name='aspnetForm']"))
        )

        html = element.get_attribute("innerHTML")
        file_name = os.path.join(save_path, paper_url[-5:] + '.html')
        with open(file_name, 'w') as file:
            file.write(html)
    finally:
        driver.quit()

if __name__ == '__main__':
    paper_url = "https://www.matweb.com/search/DataSheet.aspx?MatGUID=e5e92a1ae7f24e1b918bf4e65dbc7e52"
    save_path = "get_html"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    get_html(save_path, paper_url)