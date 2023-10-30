from selenium import webdriver
from fake_useragent import UserAgent
from grabber import getLinks
from buyer import buyerProcess
from checker import checkAll
import mydb as db
from myMethods import cookie


def fncGetLinks(driver, connection, itemCount):
    for i in range(3):
        getLinksFinished = getLinks(driver, connection, itemCount=itemCount)
        if getLinksFinished:
            return True
    return False

def fncBuy(driver, connection, minMargin):
    for i in range(3):
        buyerProcessFinished = buyerProcess(driver, connection, minMargin=minMargin)
        if buyerProcessFinished:
            return True
    return False

connection = db.createConnection()

# res = db.executeReadQuery(connection, "SELECT count(id), status FROM items  WHERE status = 0;    ")
# for item in res:
#     print(item)

useragent = UserAgent()
option = webdriver.ChromeOptions()
option.add_argument(f"-user-agent={useragent.random}")
option.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=option)
driver.set_window_rect(-20, 0, 940, 1000)

try:
    if fncGetLinks(driver, connection, 300):
        if fncBuy(driver, connection, 5):
            print("all was good")
            #checkAll()

    print("End program")
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()

