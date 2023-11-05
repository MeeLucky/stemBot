from buyer import PrintException
from myMethods import cookie, seleniumExists
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import mydb as db



def checkAll(driver, connection, DEBUG_MOD):
    url = "https://steamcommunity.com/market/"
    try:
        driver.get(url=url)
        cookie(driver)
        driver.refresh()

        if seleniumExists(driver, By.ID, "myListings") == True:
            if seleniumExists(driver, By.ID, "tabContentsMyListings") == True:
                # получаем строки с предметами со страницы маркета
                rows = driver.find_elements(By.CLASS_NAME, "market_recent_listing_row")
                # в конец добавляется 10 строк с торговой плащадки (самы популярные предметы)
                if len(rows) <= 10:
                    return
                rows = rows[0:len(rows)-10]
                print(len(rows))

                # перебераем оставшиеся предметы
                for item in rows:
                    # тип строки с маркета; 0 ничего, 1 лот на продажу, 2 ордер на покупку
                    type = 0
                    # тип определяем по ид
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

                    # ид, есть ссылка, есть тип
                    # заходим сверяем цену,

            else:
                print("не найден контейнер #tabContentsMyListings")
        else:
            print("не найден контейнер #myListings")

    except Exception as ex:
        print(ex)
        PrintException()


