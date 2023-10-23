from buyer import PrintException
from myMethods import cookie, seleniumExists
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import mydb as db



def checkAll(driver, connection):
    url = "https://steamcommunity.com/market/"
    try:
        driver.get(url=url)
        cookie(driver)
        driver.refresh()

        if seleniumExists(driver, By.ID, "myListings") == True:
            if seleniumExists(driver, By.ID, "tabContentsMyListings") == True:
                rows = driver.find_elements(By.CLASS_NAME, "market_recent_listing_row")
                #10 строк добавляется из маркета
                if len(rows) <= 10:
                    return
                rows = rows[0:len(rows)-10]
                print(len(rows))

                for item in rows:
                    type = 0
                    id = item.get_attribute("id")
                    #mylisting_6428383844993325711
                    if id[2] == 'l':
                        # лот на продажу
                        type = 1
                    #mybuyorder_6574627952
                    elif id[2] == 'b':
                        # ордер на покупку
                        type = 2

                    link = item.find_element(By.CLASS_NAME, "market_listing_item_name_link").get_attribute("href")


            else:
                print("не найден контейнер #tabContentsMyListings")
        else:
            print("не найден контейнер #myListings")

    except Exception as ex:
        print(ex)
        PrintException()


