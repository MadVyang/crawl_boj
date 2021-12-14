import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pyperclip

# execute chrome.exe with command below
# chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/temp"

# crawl numbers of problems solved
user_id = 'kzc123'
res = requests.get(f'https://www.acmicpc.net/user/{user_id}')
soup = bs(res.content, 'html.parser')
problem_list = soup.find('div', class_='problem-list')
problem_numbers = [x.get_text() for x in problem_list.find_all('a')]

# debug chrome setting
chrome_options = Options()
chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
chrome_service = Service('C:\chromedriver_win32\chromedriver.exe')
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

#
source_page_xpath = '/html/body/div[2]/div[2]/div[3]/div[6]/div/table/tbody/tr[1]/td[7]/a[1]'
copy_classname = 'copy-button'
lang_xpath = '/html/body/div[2]/div[2]/div[3]/div[7]/div/table/tbody/tr/td[8]'
lang_xpath2 = '/html/body/div[2]/div[2]/div[3]/div[9]/div/table/tbody/tr/td[8]'

#
for i in problem_numbers:
    status_page = f'https://www.acmicpc.net/status?from_mine=1&problem_id={i}&user_id={user_id}'
    driver.get(status_page)

    source_page_a_tag = driver.find_element(By.XPATH, source_page_xpath)
    source_page_href = source_page_a_tag.get_attribute('href')
    driver.get(source_page_href)

    driver.find_element(By.CLASS_NAME, copy_classname).click()
    source = pyperclip.paste()

    try:
        lang = driver.find_element(By.XPATH, lang_xpath).text
    except:
        lang = driver.find_element(By.XPATH, lang_xpath2).text

    ext = ''
    if lang[0] == 'C':
        ext = 'cpp'
    elif lang[0] == 'p' or lang[0] == 'P':
        ext = 'py'
    else:
        ext = 'java'

    with open(f'result/{i}.{ext}', 'w') as f:
        f.write(source)
