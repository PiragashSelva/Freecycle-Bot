# importing discord-related dependencies
import discord
from discord.ext import commands
# importing selenium-related dependencies
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# importing misc dependencies
import asyncio
from collections import defaultdict
import os
from dotenv import load_dotenv

####initialising###
load_dotenv()
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")
TOKEN = os.getenv("TOKEN")  

# Define your keywords here
keywords = ["TV", "bedframe", "lamp", "tool", "garden", "table", "bookshelves"]

class MyClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        self.bg_task = self.loop.create_task(self.web_scraper())

    async def on_ready(self): #prints statement to terminal when bot is connected and ready
        print("Success: Bot is connected!")
        print("-----------------------------------")

    async def web_scraper(self):
        await self.wait_until_ready()
        channel = client.get_channel(1162765234281398345) #UPDATE YOU CHANNEL HERE#

        listings_dictionary = defaultdict(int)  # initialising a dictionary of listings we've already seen

        s = Service(r"C:\Program Files (x86)\chromedriver.exe") #UPDATE THE LOCATION OF YOUR CHROMEDRIVER HERE#
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")

        while not self.is_closed():
            driver = webdriver.Chrome(service=s, options=options)
            driver.get("https://www.freecycle.org/home/dashboard")

            try:  # if the gdpr consent pops up then we execute this code to get rid of it
                ################################# REJECT NON-ESSENTIAL COOKIES #########################################
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//button[2]"))
                )
                element.click()
                ########################################################################################################

                ###################################### ACCEPT ALL COOKIES ##############################################
                # element = WebDriverWait(driver,5).until(
                #    EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'css-47sehv')]"))
                # )
                # element.click()
                ########################################################################################################
            except:  # if the gdpr consent doesn't pop up then we continue as usual
                pass

            ######################################## LOGGING IN ####################################################
            username = driver.find_element(By.XPATH, "//input[@name='user']")
            username.send_keys(LOGIN)

            password = driver.find_element(By.XPATH, "//input[@name='password']")
            password.send_keys(PASSWORD)

            password.send_keys(Keys.TAB)
            password.send_keys(Keys.RETURN)
            ########################################################################################################

            parent = WebDriverWait(driver, 5).until(   # navigating our way to the listings
                EC.presence_of_element_located((By.XPATH, "//*[@id='fc-data']"))
            ) 
            child = parent.find_elements(By.XPATH, "./child::*")
            listings = child[1:-1]  # removing the first and last element as these are non-listing elements and therefore not of interest

            for listing in listings:  # for all the listings, check if it's already in the dictionary
                if listing.get_attribute("data-id") in listings_dictionary:
                    pass  # if in the dictionary, do nothing
                else: # in not in the dictionary, execute the following
                    split = listing.text.split("\n") 
                    listing_info = split[0] + " - " + split[5] + " - " + split[6]  # stores the listing info in format: OFFER/WANTED - TITLE - SHORT DESCRIPTION
                    listings_dictionary[listing.get_attribute("data-id")] = [listing_info]  # adds it to the dictionary
                    if any(keyword.lower() in listing_info.lower() for keyword in keywords): # if keywords are present in listing, execute the following
                        
                        reply_button = listing.find_element(By.CLASS_NAME, "btn-offer") #click reply button
                        driver.execute_script("arguments[0].scrollIntoView(true);", reply_button)
                        reply_button.click()

                        index = listings.index(listing)
                        
                        textarea= driver.find_element(By.XPATH, "(//textarea[@name='body'])["+str(index+1)+"]") # type message
                        driver.execute_script("arguments[0].scrollIntoView(true);", textarea)
                        textarea.send_keys("Hi, I'm interested!") #EDIT YOUR MESSAGE HERE#
                        
                        send_button = driver.find_element(By.XPATH, "(//input[@value='Send'])["+str(index+1)+"]") # send message
                        send_button.click()

                        try: # if the confirmation box pops up, execute the following
                            close_confirmation_button = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.XPATH, "(//button[@aria-label='Dismiss alert'])[1]"))
                            )
                            close_confirmation_button.click()
                        except: # if not, continue
                            pass

                        await channel.send(listing_info) # sends listing info to discord channel                        

            driver.quit()
            await asyncio.sleep(10) 

client = MyClient(command_prefix="!", intents=discord.Intents().all())
client.run(TOKEN)