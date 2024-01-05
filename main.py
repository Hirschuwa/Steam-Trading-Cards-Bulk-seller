from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import time

STEAM_URL = "https://steamcommunity.com/"
STEAM_ACC = "YOUR ACCOUNT"
STEAM_PW = "YOUR PASSWORT"

# Set up selenium
options = ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
# open steam
driver.get(STEAM_URL)
driver.maximize_window()
time.sleep(3)
# login to steam
driver.find_element(By.XPATH, '//*[@id="global_action_menu"]/a[2]').click()
time.sleep(3)
driver.find_element(By.XPATH, '//*[@id="responsive_page_template_content"]/div[1]/div[1]/div/div/div/div[2]/div/form/div[1]/input').send_keys(STEAM_ACC)
driver.find_element(By.XPATH, '//*[@id="responsive_page_template_content"]/div[1]/div[1]/div/div/div/div[2]/div/form/div[2]/input').send_keys(STEAM_PW)
driver.find_element(By.XPATH, '//*[@id="responsive_page_template_content"]/div[1]/div[1]/div/div/div/div[2]/div/form/div[4]/button').click()

# to get past the verification you need to go to your mail and manually input the code
# with some practice it should be easily accomplished in 15 seconds but you can add time if more is needed
time.sleep(15)

# go to inventar
driver.find_element(By.XPATH, '//*[@id="account_pulldown"]').click()
driver.find_element(By.XPATH, '//*[@class="popup_menu_item"]').click()
driver.find_element(By.XPATH, '//*[@id="responsive_page_template_content"]/div[1]/div[2]/div/div[1]/div[2]/div[3]/div[2]/a/span[1]').click()
driver.find_element(By.XPATH, '//*[@id="inventory_link_753"]').click()
time.sleep(2)


# get the item, sell it if not possible go to next item in row
item_num = 1
items_to_go = True
while items_to_go:
    inventory_item = driver.find_element(By.XPATH, f'//*[@id="inventory_76561198064895481_753_0"]/div[1]/div[{item_num}]')
    inventory_item.click()
    time.sleep(2)
    try:
        driver.find_element(By.XPATH, '//*[@id="iteminfo1_item_market_actions"]/a/span[2]').click()
        time.sleep(3)
    except (NoSuchElementException, ElementNotInteractableException):
        try:
            driver.find_element(By.XPATH, '//*[@id="iteminfo0_item_market_actions"]/a/span[2]').click()
            time.sleep(3)
        except NoSuchElementException:
            item_num += 1
            continue

    # find middel seel price
    mid_sell_price = driver.find_element(By.XPATH, '//*[@id="pricehistory"]/div[3]/div[2]').text.split("T")[0]

    # input sell price
    driver.find_element(By.XPATH, '//*[@id="market_sell_buyercurrency_input"]').send_keys(Keys.BACKSPACE, Keys.BACKSPACE, mid_sell_price)

    # check if already agreed if not click agree
    agree_check = driver.find_element(By.XPATH, '//*[@id="market_sell_dialog_accept_ssa"]')
    if agree_check.is_selected():
        pass
    else:
        agree_check.click()
        time.sleep(2)

    # sell button 2
    driver.find_element(By.XPATH, '//*[@id="market_sell_dialog_accept"]').click()
    time.sleep(2)

    # confirm_sell
    driver.find_element(By.XPATH, '//*[@id="market_sell_dialog_ok"]').click()
    time.sleep(2)


