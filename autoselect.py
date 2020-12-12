from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import pyautogui
import time
from datetime import datetime
import re
import operator
from notify_run  import Notify



def autoselect():
    print("Running Script....")
    driver.implicitly_wait(1)
    driver.get('https://fp.trafikverket.se/Boka/#/search/AtIIhtAaRmSph/5/0/0/0')
    time.sleep(3)
    frame = driver.find_element_by_css_selector('#examination-type-select')
    time.sleep(0.8)

    sel = Select(driver.find_element_by_id('examination-type-select'))
    sel.select_by_value("3")


    time.sleep(0.8)
    sel = Select(driver.find_element_by_id('language-select'))
    sel.select_by_value("13")
    time.sleep(0.8)


    location = driver.find_element_by_id('id-control-searchText')
    location.clear()
    location.send_keys("Stockholm City")
    location.send_keys('\n')

    print("Loading...")

    time.sleep(0.8)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "col-xs-6"))
        )
    except Exception as e:
        print(e)
        driver.quit()
    time.sleep(0.8)

    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "col-xs-6")))
        results = driver.find_element_by_tag_name("body")
        results = results.text
        returned = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', results)
        date = datetime.strptime(returned.group(), '%Y-%m-%d %H:%M')
        print("\n\nThis is date and time found:\t ",date)
        if date < mydate:
            print("\nBetter time found!\n")
            print("DONE")
            notify.send('Better time found', 'https://fp.trafikverket.se/Boka/#/search/AtIIhtAaRmSph/5/0/0/0')
            return False
        else:
            print("No better time found\n")
            time.sleep(500)
            return True
    except Exception as e:
        print(e)

if __name__ == '__main__':
    notify = Notify()
    mydate = datetime(2021, 2, 3)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome('./chromedriver.exe',options=options)
    check = True
    while check == True:
        check = autoselect()
