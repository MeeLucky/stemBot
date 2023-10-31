from selenium import webdriver
from fake_useragent import UserAgent
from grabber import getLinks
from buyer import buyerProcess
from checker import checkAll
import mydb as db
from myMethods import cookie

DEBUG_MOD = False

def fncGetLinks(driver, connection, DEBUG_MOD, itemCount):
    for i in range(3):
        getLinksFinished = getLinks(driver, connection, DEBUG_MOD, itemCount=itemCount)
        if getLinksFinished:
            return True
    return False

def fncBuy(driver, connection, DEBUG_MOD, minMargin):
    for i in range(3):
        buyerProcessFinished = buyerProcess(driver, connection, DEBUG_MOD, minMargin=minMargin)
        if buyerProcessFinished:
            return True
    return False


connection = db.createConnection()

useragent = UserAgent()
option = webdriver.ChromeOptions()
option.add_argument(f"-user-agent={useragent.random}")
option.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=option)
driver.set_window_rect(-20, 0, 940, 1000)

try:
    if fncGetLinks(driver, connection, DEBUG_MOD, 300):
        if fncBuy(driver, connection, DEBUG_MOD, 5):
            if DEBUG_MOD:
                print("all was good")
                #checkAll()

    if DEBUG_MOD:
        print("End program")
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()

