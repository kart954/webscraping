from bs4 import BeautifulSoup
import requests
import urllib
import pytesseract
from pytesseract import image_to_string
from PIL import Image
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as exceptions
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import sys
import re

def get_captcha_text(location, size):
  #pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract' #path/to/pytesseract'
  #pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR'
  im = Image.open('screenshot.png')
  left = location['x']  + 160
  top = location['y'] + 50
  right = location['x'] + size['width']  + 200
  bottom = location['y'] + size['height'] + 200
  im = im.crop((left, top, right, bottom))
  im.save('screenshot2.png')
  captcha_text = image_to_string('screenshot2.png', lang='eng', config='--oem 3 --psm 10 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz0123456789')
  print("captcha_text: ",captcha_text)
  return captcha_text.strip()

def submit_to_website():
  url= 'https://src.udiseplus.gov.in/home'
  driver = webdriver.Chrome(executable_path= "C:\\chromedriver.exe")
  driver.set_window_size(1050, 708)
  #driver.set_page_load_timeout(9)
  driver.implicitly_wait(5)
  driver.get(url)
  sleep(2)
  actions = ActionChains(driver)
  element = driver.find_element_by_xpath('/html/body/div/div[2]/section[1]/div/div/div[2]/div[1]/form/div[2]/div[3]/div[1]/img') #find part of the page you want image of
  actions.move_to_element(element)
  location = element.location
  size = element.size
  print(f"location: {location},  size : {size}")
  driver.save_screenshot('screenshot.png')
  driver.find_element_by_css_selector("input[type='radio'][class='checkBoxSearchByPinCode']").click()
  bypincode = driver.find_element_by_xpath('//*[@id="search"]')
  bypincode.clear()
  bypincode.send_keys('122001')
  captcha = driver.find_element_by_xpath('//*[@id="searchSchool"]/div[2]/div[3]/div[1]/input')
  captcha.clear()
  captcha_text = re.sub('[^a-z0-9]','',get_captcha_text(location, size))
  if len(captcha_text) == 6:
    sleep(2)
    captcha.send_keys(captcha_text)
    driver.find_element_by_xpath('//*[@id="homeSearchBtn"]').click()
  else:
    print(f"[{captcha_text}] Not able to solver captcha!! problem wih OCR!!")
    sleep(10)
    driver.quit()
    
  sleep(30)
  driver.quit()
  sys.exit("Task completed!")

  
submit_to_website()




