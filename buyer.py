import linecache
import random
import sys
import time

from myMethods import cookie, seleniumExists
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import mydb as db


def buyerProcess(driver, connection, DEBUG_MOD):
    minMargin = 5
    isReg = False
    if DEBUG_MOD:
        print("start fnc buyerProcess")

    query = "SELECT tb_margin, name, link, id FROM items WHERE status = 0;"
    items = db.executeReadQuery(connection, query)
    itemID = 0

    try:
        itemsLen = len(items)
        print(f"Перебор {itemsLen} предметов:")
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
            print(f"\n{itemIndex}/{itemsLen}: {item[1]}\n{item[2]}")
            driver.get(url=item[2])

            # загружаем куки если это первый айтем
            if isFirst == True:
                cookie(driver, DEBUG_MOD=DEBUG_MOD)
                driver.refresh()
                isFirst = False

            # проверяем наличие ошибки, загрузился ли контент стима
            if seleniumExists(driver, By.CLASS_NAME, "market_listing_table_message"):
                print("ошибка загрузки страницы, перезагрузка страницы")
                time.sleep(2)
                driver.refresh()
                driver.implicitly_wait(5)
                if seleniumExists(driver, By.CLASS_NAME, "market_listing_table_message"):
                    print("ошибка загрузки страницы во второй раз, пропуск предмета")
                    setItemStatus(connection, item[3], -1, DEBUG_MOD)
                    continue

            # собираем инфу
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
                print("пропуск, за 10 попыток не удаётся получить цену автозакупки")
                setItemStatus(connection, item[3], -2, DEBUG_MOD)
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
            # проверка правильная ли валюта используется
            if buyPrice.split(" ")[1] != "pуб.":
                if DEBUG_MOD:
                    print(buyPrice)
                    print(buyPrice.split(" ")[1])
                print("Пропуск, валюта автопокупки не в рублях")
                setItemStatus(connection, item[3], -3, DEBUG_MOD)
                continue

            # проверка правильная ли валюта используется
            if sellPrice.split(" ")[1] != "pуб.":
                if DEBUG_MOD:
                    print(sellPrice)
                    print(sellPrice.split(" ")[1])
                print("Пропуск, валюта автопокупки не в рублях")
                setItemStatus(connection, item[3], -3, DEBUG_MOD)
                continue

            # форматируем цены для расчётов
            buyPrice = float(
                buyPrice
                .replace(" pуб.", "")
                .replace(",", ".")
            )
            sellPrice = float(
                sellPrice
                .replace(" pуб.", "")
                .replace(",", ".")
            )
            # находим маржу в стиме
            margin = round((((sellPrice - sellPrice * 0.15) / buyPrice) - 1) * 100)
            print(f"Маржа  ТБ : {item[0]}%")
            print(f"Маржа стим: {margin}%")

            if margin < minMargin:
                print("пропуск, маленькая маржа")
                setItemStatus(connection, item[3], -4, DEBUG_MOD)
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
                        print(f"Установлен оредр на {buyPrice}")
                        driver.find_element(By.CLASS_NAME, "market_noncommodity_buyorder_button").click()
                        driver.implicitly_wait(3)
                        priceInput = driver.find_element(By.ID, "market_buy_commodity_input_price")
                        priceInput.clear()
                        priceInput.send_keys(buyPrice)
                        quantityInput = driver.find_element(By.ID, "market_buy_commodity_input_quantity")
                        quantityInput.clear()
                        quantityInput.send_keys("3")
                        driver.find_element(By.ID, "market_buyorder_dialog_accept_ssa").click()
                        driver.implicitly_wait(3)
                        driver.find_element(By.ID, "market_buyorder_dialog_purchase").click()
                        driver.implicitly_wait(3)
                        setItemStatus(connection, item[3], 1, DEBUG_MOD)
                else:
                    setItemStatus(connection, item[3], -6, DEBUG_MOD)
            else:
                setItemStatus(connection, item[3], -5, DEBUG_MOD)
                print("пропуск, уже есть активный оред")

            # time.sleep(random.randint(0, 2))

        return True
    except Exception as ex:
        print(ex)
        PrintException()
        setItemStatus(connection, itemID, -7, DEBUG_MOD)


def getItemsFromFile(path):
    with open(path, "r") as file:
        s = file.read()
        arr = s.split("\n")

        i: int
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


def setItemStatus(connection, id, status, DEBUG_MOD):
    db.updateItem(connection, "status", status, f"id = {id}")
    if DEBUG_MOD:
        print(f"setItemStatus {id} = {status}")
