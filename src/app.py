
from utils.browser import set_chrome_driver
from utils.tools import run_on_thread
from utils.logger import logger

import json
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

#TARGET_URL = "https://www.nike.com/tw/launch/t/air-force-1-skeleton-orange?cp=56135845539_search_%7Ctw%7CCore%2BBrand%2B-%2BGN%2B-%2BPure%2B-%2BXCategory%2B-%2BNike%2BTaiwan%2B-%2BTM%2B-%2BMen%2BTargeted%2B-%2BGN%2BLP%2BTest%2B-%2BEN_CH%2B-%2BExact%7CGOOGLE%7Cnike"
TARGET_URL = "https://www.nike.com/tw/launch/t/kybrid-2-what-the-pe-xa?cp=56135845539_search_%7Ctw%7CCore%2BBrand%2B-%2BGN%2B-%2BPure%2B-%2BXCategory%2B-%2BNike%2BTaiwan%2B-%2BTM%2B-%2BMen%2BTargeted%2B-%2BGN%2BLP%2BTest%2B-%2BEN_CH%2B-%2BExact%7CGOOGLE%7Cnike"
TARGET_SIZE = "CM 26.5"
USER_INFO_PATH = './user.json'
#COOKIE_PATH = './cookie.json'

def wait_element_located(
    element_name: str, 
    element_css: str, 
    driver: object, 
    timeout=3
) -> None:
    if not element_name:
        logger.error('missing element name')
        return
    if not driver:
        logger.error('missing driver')
        return

    element_obj = None
    element_exist = None
    try:
        element_exist = EC.presence_of_element_located((By.CSS_SELECTOR, element_css))
        element_obj = WebDriverWait(driver, timeout).until(element_exist)
    except TimeoutException:
        print(f'{element_name} timed out waiting for page to load')
    finally:
        print(f'{element_name} page loaded')
        return element_obj

def wait_element_clickable(
    element_name: str, 
    element_css: str, 
    driver: object, 
    timeout=3
) -> object:
    if not element_name:
        logger.error('missing element name')
        return
    if not driver:
        logger.error('missing driver')
        return

    element_exist = None
    element_obj = None
    try:
        element_exist = EC.element_to_be_clickable((By.CSS_SELECTOR, element_css))
        element_obj = WebDriverWait(driver, timeout).until(element_exist)
    except TimeoutException:
        print(f'{element_name} timed out, unable to click')
    finally:
        print(f'{element_name} ready to click')
        return element_obj

def run_purchase() -> None:
    driver = set_chrome_driver()
    driver.get(TARGET_URL)

    # start purchasing
    wait_element_clickable(
        element_name='Size Choice',
        element_css='button[class="size-grid-dropdown size-grid-button"]',
        driver=driver
    )
    size_choices = driver.find_elements(By.CSS_SELECTOR, 'button[class="size-grid-dropdown size-grid-button"]')
    for size in size_choices:
        if TARGET_SIZE == size.text:
            print(f'find target {size.text}')
            logger.info(f'find target {size.text}')
            size.click()
            break

    scroll_height = 350
    driver.execute_script('window.scrollTo(0, %s);' % (scroll_height))
    time.sleep(2)
    add_cart_btn = wait_element_clickable(
        element_name='Add Cart Btn',
        element_css='button[class="ncss-btn-primary-dark btn-lg"]',
        driver=driver
    )
    add_cart_btn.click()

    # go to cart
    driver.get('https://www.nike.com/tw/zh-Hant/cart')
    guest_checkout_btn = wait_element_clickable(
        element_name='Guest Checkout Btn',
        element_css='button[data-automation="guest-checkout-button"]',
        driver=driver
    )
    guest_checkout_btn.click()
    time.sleep(5)
    wait_element_clickable(
        element_name='Shipping LastName Btn',
        element_css='input[id="Shipping_LastName"]',
        driver=driver
    )
    start_payment(driver=driver)
    time.sleep(3600)
    return

def start_payment(driver: object) -> None:
    if not driver:
        logger.error('missing driver')
        return

    with open(USER_INFO_PATH, 'r+') as user_file:
        user_dict = json.load(user_file)
        print(user_dict)

    last_name_column = driver.find_element(By.CSS_SELECTOR, 'input[id="Shipping_LastName"]')
    last_name_column.send_keys(user_dict['last_name'])

    first_name_column = driver.find_element(By.CSS_SELECTOR, 'input[id="Shipping_FirstName"]')
    first_name_column.send_keys(user_dict['first_name'])

    post_code_column = driver.find_element(By.CSS_SELECTOR, 'input[id="Shipping_PostCode"]')
    post_code_column.send_keys(user_dict['post_code'])

    # select = driver.find_element(By.CSS_SELECTOR, 'select[id="Shipping_Territory"]')
    # select.click()
    # target_option = None

    select = Select(driver.find_element(By.CSS_SELECTOR, 'select[id="Shipping_Territory"]'))
    select.select_by_visible_text(user_dict['city'])

    area_column = driver.find_element(By.CSS_SELECTOR, 'input[id="Shipping_Address3"]')
    area_column.send_keys(user_dict['area'])

    address_column = driver.find_element(By.CSS_SELECTOR, 'input[id="Shipping_Address1"]')
    address_column.send_keys(user_dict['address'])
    
    phone_column = driver.find_element(By.CSS_SELECTOR, 'input[id="Shipping_phonenumber"]')
    phone_column.send_keys(user_dict['phone'])

    identity_column = driver.find_element(By.CSS_SELECTOR, 'input[id="governmentid"]')
    identity_column.send_keys(user_dict['identity'])

    email_column = driver.find_element(By.CSS_SELECTOR, 'input[id="shipping_Email"]')
    email_column.send_keys(user_dict['email'])

    agreement_check = wait_element_clickable(
        element_name='agreement_check checkbox',
        element_css=f'span[class="checkbox-checkmark"]',
        driver=driver
    )
    
    click_string = "sendForm('Billing')"
    shipping_submit_btn = wait_element_clickable(
        element_name='shipping_submit_btn',
        element_css=f'button[id="shippingSubmit"][ng-click="{click_string}"]',
        driver=driver
    )
    ActionChains(driver).move_to_element(shipping_submit_btn)
    agreement_check.click()
    time.sleep(1)
    shipping_submit_btn.click()

    click_string = "sendForm('Payment')"
    payment_submit_btn = wait_element_located(
        element_name='payment_submit_btn',
        element_css=f'button[id="billingSubmit"][ng-click="{click_string}"]',
        driver=driver,
    )
    ActionChains(driver).move_to_element(payment_submit_btn)
    time.sleep(1)
    print(payment_submit_btn.is_displayed())
    payment_submit_btn.click()


if __name__ == "__main__":
    print('start crawler')
    logger.info('start crawler')
    run_purchase()
    logger.info('end crawler')
