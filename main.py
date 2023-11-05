import time

from selenium import webdriver
from fake_useragent import UserAgent
from grabber import getLinks
from buyer import buyerProcess
from checker import checkAll
import mydb as db

DEBUG_MOD = False

def fncGetLinks(driver, connection, DEBUG_MOD):
    for i in range(3):
        getLinksFinished = getLinks(driver, connection, DEBUG_MOD)
        if getLinksFinished:
            return True
    return False

def fncBuy(driver, connection, DEBUG_MOD):
    for i in range(3):
        buyerProcessFinished = buyerProcess(driver, connection, DEBUG_MOD)
        if buyerProcessFinished:
            return True
    return False

try:
    connection = db.createConnection()

    # useragent = UserAgent()

    option = webdriver.ChromeOptions()
    # option.add_argument(f"-user-agent={useragent.random}")
    option.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=option)
    driver.set_window_rect(-20, 0, 940, 1000)

    if fncGetLinks(driver, connection, DEBUG_MOD):
        if fncBuy(driver, connection, DEBUG_MOD):
            if DEBUG_MOD:
                print("all was good")


    if DEBUG_MOD:
        print("End program")
except Exception as ex:
    print(ex)
    input("END PROGRAM error")
finally:
    driver.close()
    driver.quit()
    input("END PROGRAM good")

