from .logger import logger

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import time
import os
import traceback
import random

CHROME_LOCAL_DRIVER_PATH = './chromedriver'
def set_chrome_driver(cookie=None):
    """set up chrome driver by local driver's file or selenium container"""
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(CHROME_LOCAL_DRIVER_PATH, chrome_options=options)
        if not driver:
            return None
        return driver
    except Exception as e:
        logger.exception(f'set chrome driver failed, {e}')
        # if failed, the most possible reason is the version of driver is not correct

def get_cookie(driver):
    """get driver's cookie"""
    if not driver:
        return
    cookies_list = driver.get_cookies()   
    return cookies_list