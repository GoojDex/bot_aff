import os, random
from selenium import webdriver
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from time import sleep

options = Options()
# Specifying where the cookies will be stored.
options.add_argument("--user-data-dir=C:\\Users\\Tahmid\\Programming\\telegram_bot\\cookies")
# Silences logs on terminal and keeps terminal looking clean.
os.environ['WDM_LOG_LEVEL'] = '0'
# Saves driver on project directory.
os.environ['WDM_LOCAL'] = '1'
# Downloads and installs necessary driver version if already not done so.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
actions = action_chains.ActionChains(driver)

# Setting window position and size.
driver.set_window_size(1260, 905) # Resizes the window to a specific size.
driver.set_window_position(250, 70, windowHandle='current')

# print('Driver instantiated successfully')

def launch_deals_page():
    # Launches the today's deal page.
    driver.get("https://www.amazon.it/")
    deals_page = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#nav-xshop > a:nth-child(2)')
        )
    )
    # print("deals page found")
    deals_page.click()

def all_deals(pages_to_retrieve_upto=1):
    try:
        # retrieve all the product information from the deals page.
        for page_number in range(pages_to_retrieve_upto):
            deals = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, 'DealGridItem-module__dealItemContent_1vFddcq1F8pUxM8dd9FW32')
                )
            ) # All the items listed for sale.
            # Repeatedly obtains affiliate link for each product.
            deals_page = driver.current_url
            for item in range(len(deals)):
                try:
                    deals_second_time = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.CLASS_NAME, 'DealGridItem-module__dealItemContent_1vFddcq1F8pUxM8dd9FW32')
                    )
                )
                    deals_second_time[item].click()
                    sleep(random.uniform(1.5, 2.5))
                    multiple_deals_to_one_deal() # When there is a cluster of deals, it will select the first one.
                    retrieve_affiliate_link() # Copies the affiliate short link and saves on deals.txt file.
                except Exception as e:
                    # print(e)
                    pass
                driver.get(str(deals_page)) # Goes back to the deals page after obtaining the affiliate link.
                sleep(random.uniform(1.5, 2.5))
            go_next_page() # Goes to the next page in today's deal page.
        driver.quit() # Ends the selenium session.
    except Exception as e:
        # print(e)
        driver.quit() # Ends the selenium session

def retrieve_affiliate_link():
    # Copies the affiliate short link and saves on deals.txt file.
    try:
        produce_short_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#amzn-ss-text-link > span > strong > a')
            )
        )
        produce_short_link.click()
        sleep(random.uniform(.5, 1.1))
        short_link_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, 'amzn-ss-text-shortlink-textarea')
            )
        )
        short_link = short_link_element.text
        with open('deals.txt', 'a') as notebook:
            notebook.write(short_link + "\n")
    except Exception as e:
        # print(e)
        pass
    
    
# Goes to the next page in today's deal page.
def go_next_page():
    old_link = driver.current_url
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, 'a-last')
        )
    )

    next_button.click()
    sleep(random.uniform(.9, 1.4))
    # print('went to the next page')
    while True: # This while loop is to ensure the change of page.
        if old_link == driver.current_url:
            sleep(random.uniform(1.9, 2.4))
            continue
        else:
            break

# When there is a cluster of deals, it will select the first one.
def multiple_deals_to_one_deal():
    try:
        items = WebDriverWait(driver, 4).until(
                    EC.presence_of_all_elements_located(
                        (By.CLASS_NAME, 'a-size-base.a-color-base')
                    )
                )

        for i in range(1):
            items[1].click()
            sleep(random.uniform(.5, 1.1))
    except TimeoutException:
        return None # The page is a normal item page, does not contain cluster of items. Continue with the rest of the code.


    

if __name__ == "__main__":
    launch_deals_page()
    all_deals(pages_to_retrieve_upto=2)
    

