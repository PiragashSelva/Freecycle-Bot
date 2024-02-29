#importing selenium-related dependencies
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#importing misc dependencies
import time
from collections import defaultdict
import os
from dotenv import load_dotenv

####initialising###
load_dotenv()
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
listings_dictionary = defaultdict(int) #initialising a dictionary of listings we've already seen
listings_dictionary["94034570"] = 1 #pre-loading the dictionary with the listings we've already seen

s = Service(r"C:\Program Files (x86)\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
#options.add_argument("user-data-dir=C:\\Users\\Username\\AppData\\Local\\Google\\Chrome\\User Data")

while True:

    driver = webdriver.Chrome(service=s, options=options)
    driver.get("https://www.freecycle.org/home/dashboard")
            
    try: #if the gdpr consent pops up then we execute this code to get rid of it
        ################################# REJECT NON-ESSENTIAL COOKIES #########################################
        element = WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.XPATH, "//button[2]"))
        )
        element.click()
        ########################################################################################################

        ###################################### ACCEPT ALL COOKIES ##############################################
        #element = WebDriverWait(driver,5).until(
        #    EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'css-47sehv')]"))
        #)
        #element.click()
        ########################################################################################################
    except: #if the gdpr consent doesn't pop up then we continue as usual
        pass

    ######################################## LOGGING IN ####################################################
    username = driver.find_element(By.XPATH, "//input[@name='user']")
    username.send_keys(LOGIN)
    
    password = driver.find_element(By.XPATH, "//input[@name='password']")
    password.send_keys(PASSWORD)

    password.send_keys(Keys.TAB)
    password.send_keys(Keys.RETURN)
    ########################################################################################################

    parent = WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='fc-data']"))
        )
    child = parent.find_elements(By.XPATH, "./child::*")
    listings = child[1:-1] #removing the first and last element as these are non-listing elements and therefore not of interest

    for listing in listings: #for all the listings, check if it's already in the dictionary
        if listing.get_attribute("data-id") in listings_dictionary:
            pass #if in the dictionary, do nothing
        else:        
            split = listing.text.split("\n")
            print(split[0] + " - " + split[5] + " - " + split[6]) # prints listing in format: OFFER/WANTED - TITLE - SHORT DESCRIPTION
            listings_dictionary[listing.get_attribute("data-id")] = [split[0] + " - " + split[5] + " - " + split[6]] #if it's not in the dictionary, add it to the dictionary and increase the counter
        
    driver.quit()
    time.sleep(60) #pause for 60 seconds then repeat