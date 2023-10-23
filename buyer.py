import linecache
import random
import sys
import time

from myMethods import cookie, seleniumExists
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import mydb as db

COLOR_YELLOW = "\033[33m"
COLOR_GREEN = "\033[32m"


def buyerProcess(driver, connection, minMargin=10, isReg=False):
    print("start fnc buyerProcess")

    query = "SELECT tb_margin, name, link, id FROM items WHERE status = 0;"
    items = db.executeReadQuery(connection, query)

    url = "https://steamcommunity.com/login/home/"
    itemID = 0

    try:
        # driver.set_window_rect(-20, 0, 940, 1000)

        print(f"Перебор {len(items)} ссылок:")
        isFirst = True
        itemIndex = 0
        for item in items:
            itemIndex += 1
            itemID = item[3]
            itemStatus = 0
            # - errors
            # 0 none
            # 2 create order

            # открываем вкладку
            print(f"{item[2]}\n{itemIndex}: {item[1]}")
            driver.get(url=item[2])

            # загружаем куки если это первый айтем
            if isFirst == True:
                cookie(driver)
                driver.refresh()
                isFirst = False

            # проверяем наличие ошибки
            if seleniumExists(driver, By.CLASS_NAME, "market_listing_table_message"):
                printColor("ошибка загрузки страницы, перезагрузка страницы", COLOR_YELLOW)
                time.sleep(2)
                driver.refresh()
                driver.implicitly_wait(5)
                if seleniumExists(driver, By.CLASS_NAME, "market_listing_table_message"):
                    printColor("ошибка загрузки страницы второй раз, пропуск предмета", COLOR_YELLOW)
                    setItemStatus(connection, item[3], -1)
                    continue
            # собираем инфу
            # продаж в день
            # print(f"sold in a day: ")
            # driver.implicitly_wait(5)

            # цена покупки (автозакупка)
            buyPrice = ""
            # если за 10 попыток не удаётся получить цену автозакупки то предмет пропускается
            for i in range(1, 10):
                try:
                    buyPrice = driver.find_elements(By.CLASS_NAME, "market_commodity_orders_header_promote")[1].text
                    if buyPrice != "":
                        print(f"Цена авто покупки: {buyPrice}")
                        break
                except StaleElementReferenceException:
                    print(f"{i})StaleElementReferenceException for buyPrice")
            if buyPrice == "":
                printColor("пропуск, за 10 попыток не удаётся получить цену автозакупки", COLOR_YELLOW)
                setItemStatus(connection, item[3], -2)
                continue

            # цена продажи (цена первого лота)
            sellPrices = driver.find_elements(By.CLASS_NAME, "market_listing_price_with_fee")
            sellPrice = ""
            for price in sellPrices:
                if price.text != "Продано!":
                    sellPrice = price.text
                    break
            print(f"Цена продажи: {sellPrice}")

            # маржа
            if buyPrice.find("₸") == -1:
                printColor("Пропуск, валюта автопокупки не в тенге", COLOR_YELLOW)
                print(buyPrice)
                print(buyPrice.find("₸"))
                setItemStatus(connection, item[3], -3)
                continue

            buyPrice = float(
                buyPrice
                .replace("₸", "")
                .replace(" ", "")
                .replace(",", ".")
            )
            # sellPrice = float(sellPrice.split(" ")[0].replace(",", "."))
            sellPrice = float(
                sellPrice
                .replace("₸", "")
                .replace(" ", "")
                .replace(",", ".")
            )
            margin = round((((sellPrice - sellPrice * 0.15) / buyPrice) - 1) * 100)
            print(f"Маржа  ТБ : {item[0]}%")
            print(f"Маржа стим: {margin}%")

            if margin < minMargin:
                printColor("пропуск, Слишком маленькая маржа", COLOR_YELLOW)
                setItemStatus(connection, item[3], -4)
                continue

            # ордер на покупку
            myOrder = False
            # лот на продажу
            myLot = False
            myListings = driver.find_element(By.ID, "myListings")
            # если есть какой-то листинг
            if myListings.text != "":
                # то проверяем заголовок
                myListingsType = myListings.find_elements(By.CLASS_NAME, "my_listing_section")
                for listing in myListingsType:
                    header = listing.find_element(By.CLASS_NAME, "my_market_header_active")
                    if header.text == "Мои запросы на покупку":
                        # то оредер на покупку есть
                        myOrder = True
                    else:
                        # то есть лот на продажу
                        myLot = True
            else:
                # то ордера нет
                myOrder = False

            if myOrder:
                print("Есть ордер на покупку")
            else:
                print("Нет оредра на покупку")
            if myLot:
                print("Есть лот на продажу")
            else:
                print("Нет лота на продажу")
            # print(f"active lot: ")
            # id="tabContentsMyListings"
            # class market_listing_row market_recent_listing_row
            # id=mybuyorder_6568879107

            # если нет оредра на покупку
            if myOrder == False:
                # и нет лота на продажу
                if myLot == False:
                    # и маржа подходит под минимальные условия
                    if margin >= minMargin:
                        # создаём оредр
                        printColor(f"Установлен оредр на {buyPrice}", COLOR_GREEN)
                        driver.find_element(By.CLASS_NAME, "market_noncommodity_buyorder_button").click()
                        driver.implicitly_wait(3)
                        priceInput = driver.find_element(By.ID, "market_buy_commodity_input_price")
                        priceInput.clear()
                        priceInput.send_keys(buyPrice)
                        driver.find_element(By.ID, "market_buyorder_dialog_accept_ssa").click()
                        driver.implicitly_wait(3)
                        driver.find_element(By.ID, "market_buyorder_dialog_purchase").click()
                        driver.implicitly_wait(3)
                        setItemStatus(connection, item[3], 1)
                else:
                    setItemStatus(connection, item[3], -6)
            else:
                setItemStatus(connection, item[3], -5)
            time.sleep(random.randint(0, 2))

        return True
    except Exception as ex:
        print(ex)
        PrintException()
        setItemStatus(connection, itemID, -7)


def getItemsFromFile(path):
    with open(path, "r") as file:
        s = file.read()
        arr = s.split("\n")

        for i in range(len(arr)):
            arr[i] = arr[i].split("/#/")
        file.close()

    return arr



def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


def printColor(text, color):
    print(f"{color}{text}\033[0m")


def setItemStatus(connection, id, status):
    db.updateItem(connection, "status", status, f"id = {id}")
    print(f"setItemStatus {id} = {status}")
