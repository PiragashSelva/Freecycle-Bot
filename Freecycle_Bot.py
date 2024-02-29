########################################################################################################
# THIS BOT NOTIFIES THE USER WHEN NEW LISTINGS HAVE BEEN CREATED #
########################################################################################################

# importing discord-related dependencies
import discord
from discord.ext import commands, tasks
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


class MyClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        self.bg_task = self.loop.create_task(self.web_scraper())

    async def on_ready(self):
        print("Success: Bot is connected!")
        print("-----------------------------------")

    async def web_scraper(self):
        await self.wait_until_ready()
        channel = client.get_channel(1162765234281398345)

        listings_dictionary = defaultdict(
            int
        )  # initialising a dictionary of listings we've already seen
        first_loop = 1  # initialising a variable so we can tell if it's the first loop

        s = Service(r"C:\Program Files (x86)\chromedriver.exe")
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

            counter = 0  # initialising a counter/ resetting the counter
            parent = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='fc-data']"))
            )
            child = parent.find_elements(By.XPATH, "./child::*")
            listings = child[
                1:-1
            ]  # removing the first and last element as these are non-listing elements and therefore not of interest

            for (
                listing
            ) in (
                listings
            ):  # for all the listings, check if it's already in the dictionary
                if listing.get_attribute("data-id") in listings_dictionary:
                    pass  # if in the dictionary, do nothing
                else:
                    counter += 1
                    listings_dictionary[listing.get_attribute("data-id")] = (
                        1  # if it's not in the dictionary, add it to the dictionary and increase the counter
                    )

            if (
                counter != 0 and first_loop != 1
            ):  # if the counter is non-zero and it's not our first loop, we let the user know
                if counter == 1:
                    await channel.send("THERE'S 1 NEW LISTING!!!")
                else:
                    await channel.send("THERE ARE " + str(counter) + " NEW LISTINGS!!!")

            first_loop = 0
            driver.quit()
            await asyncio.sleep(10)


client = MyClient(command_prefix="!", intents=discord.Intents().all())
client.run(TOKEN)