from selenium import webdriver
from fake_useragent import UserAgent
from grabber import getLinks
from buyer import buyerProcess
from checker import checkAll
import mydb as db
from myMethods import cookie



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

getLinksFinished = False
buyerProcessFinished = False
try:
    skipIt = False
    if not skipIt:
        for i in range(3):
            getLinksFinished = getLinks(driver, connection, itemCount=50)
            if getLinksFinished:
                break
    else:
        getLinksFinished = True

    skipIt = False
    if not skipIt:
        if getLinksFinished:
            for i in range(3):
                buyerProcessFinished = buyerProcess(driver, connection, minMargin=5)
                if buyerProcessFinished:
                    break
    else:
        buyerProcessFinished = True

    if buyerProcessFinished:
        checkAll(driver, connection)

    print("all was good")


except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()