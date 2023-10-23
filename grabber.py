import time
from selenium.webdriver.common.by import By
import mydb as db
from buyer import seleniumExists
from myMethods import cookie

def getLinks(driver, connection, week_sells = "15", itemCount = 500):
    result = False
    url = "https://tradeback.io/ru/comparison"

    try:
        print("get url")
        driver.get(url=url)
        driver.set_window_rect(0,0,900,1000)
        driver.implicitly_wait(5)

        print("cookie")
        cookie(driver)
        driver.implicitly_wait(5)

        print("refresh page")
        driver.refresh()
        driver.implicitly_wait(5)

        print("click green button")
        driver.find_element(By.CLASS_NAME, "btn_green_white_innerfade").click()
        driver.implicitly_wait(5)

        print("get url again")
        url = "https://tradeback.io/ru/comparison"
        driver.get(url=url)
        driver.implicitly_wait(5)
        time.sleep(1)

        # установка настроек трейд бека и проверка их корректности


        # отключаем автообновление
        # ставим игру дота 2
        # первый сервис стим автопокупка
        # второй сервис стим обычная
        # доп фильтры
        # сортировка
        # загрузка предметов


        # отключаем автообновление
        isFine = False
        for i in range(3):
            #проверка значения
            if driver.find_element(By.ID, "auto-update-status-title").text == "(выкл.)":
                #правильно, к следующему пункту
                isFine = True
                break
            else:
                #неправильно, меняем значение
                seleniumClickCheckboxByID(driver, "auto-update-live")
                driver.implicitly_wait(3)
        #если предыдущая проверка не удалась, то выкидыаем ошибку
        checkIsFine(isFine, "Неудалось отключить автообновление данных")



        # ставим игру дота 2
        isFine = False
        for i in range(3):
            #проверка значения
            if (driver
                    .find_element(By.CLASS_NAME, "dropdown-select")
                    .find_element(By.CLASS_NAME, "title")
                    .text == "Dota 2"):
                #правильно, к следующему пункту
                isFine = True
                break
            else:
                #неправильно, меняем значение
                gameDropdown = driver.find_elements(By.CLASS_NAME, "dropdown-select")[0]
                gameDropdown.click()
                driver.implicitly_wait(3)
                gameDropdown.find_elements(By.CLASS_NAME, "option")[2].click()
                driver.implicitly_wait(3)
        #если предыдущая проверка не удалась, то выкидыаем ошибку
        checkIsFine(isFine, "Неудалось изменить поле 'Игра'")

        # первый сервис стим
        isFine = False
        for i in range(3):
            #проверка значения
            if (driver
                    .find_elements(By.CLASS_NAME, "dropdown-select")[4]
                    .find_element(By.CLASS_NAME, "title")
                    .text == "SteamCommunity.com"):
                #правильно, к следующему пункту
                isFine = True
                break
            else:
                #неправильно, меняем значение
                firstServisContainer = driver.find_elements(By.CLASS_NAME, "dropdown-select")[4]
                firstServisContainer.click()
                driver.implicitly_wait(3)
                firstServisContainer.find_elements(By.CLASS_NAME, "option")[0].click()
                driver.implicitly_wait(3)
        #если предыдущая проверка не удалась, то выкидыаем ошибку
        checkIsFine(isFine, "Неудалось установить на первый сервис SteamCommunity.com")

        # первый сервис стим (галочка автопокупка)
        isFine = False
        for i in range(3):
            # проверка значения
            if driver.find_element(By.ID, "first-service-orders").is_selected():
                # правильно, к следующему пункту
                isFine = True
                break
            else:
                # неправильно, меняем значение
                seleniumClickCheckboxByID(driver, "first-service-orders")
                driver.implicitly_wait(3)
        # если предыдущая проверка не удалась, то выкидыаем ошибку
        checkIsFine(isFine, "Неудалось поставить галку автопокупка для первого сервиса SteamCommunity.com")

        # второй сервис стим
        isFine = False
        for i in range(3):
            #проверка значения
            if (driver
                    .find_elements(By.CLASS_NAME, "dropdown-select")[5]
                    .find_element(By.CLASS_NAME, "title")
                    .text == "SteamCommunity.com"):
                #правильно, к следующему пункту
                isFine = True
                break
            else:
                #неправильно, меняем значение
                firstServisContainer = driver.find_elements(By.CLASS_NAME, "dropdown-select")[5]
                firstServisContainer.click()
                driver.implicitly_wait(3)
                firstServisContainer.find_elements(By.CLASS_NAME, "option")[0].click()
                driver.implicitly_wait(3)
        #если предыдущая проверка не удалась, то выкидыаем ошибку
        checkIsFine(isFine, "Неудалось установить на второй сервис SteamCommunity.com")

        # второй сервис стим (галочка обычный)
        isFine = False
        for i in range(3):
            # проверка значения
            if driver.find_element(By.ID, "second-service-normal").is_selected():
                # правильно, к следующему пункту
                isFine = True
                break
            else:
                # неправильно, меняем значение
                seleniumClickCheckboxByID(driver, "second-service-normal")
                driver.implicitly_wait(3)
        # если предыдущая проверка не удалась, то выкидыаем ошибку
        checkIsFine(isFine, "Неудалось поставить галку обычные для второго сервиса SteamCommunity.com")

        # доп фильтры
        isFine = False
        driver.find_element(By.ID, "more-filters").click()
        time.sleep(1)
        salesFilter = (driver
             .find_element(By.CLASS_NAME, "comparison-popup-container")
             .find_element(By.CLASS_NAME, "comparison-sales-block")
             .find_element(By.CLASS_NAME, "sales-filter"))
        for i in range(3):
            if salesFilter.get_attribute('value') == week_sells+"0":
                isFine = True
                break
            else:
                # в инпуте salesFilter уже есть ноль, получиться 15 + 0 = 150
                salesFilter.send_keys(week_sells)

        driver.find_element(By.CLASS_NAME, "iziModal-button-close").click()
        # если предыдущая проверка не удалась, то выкидыаем ошибку
        checkIsFine(isFine, "Неудалось установить фильтр 'продаж в неделю' для SteamCommunity.com")

        # сортировка
        isFine = False
        for i in range(3):
            columnProfit = driver.find_element(By.CLASS_NAME, "column-profit")
            if seleniumExists(driver, By.CLASS_NAME, "fa-sort-amount-desc"):
              isFine = True
              break
            else:
                columnProfit.click()
                driver.implicitly_wait(5)
        # если предыдущая проверка не удалась, то выкидыаем ошибку
        checkIsFine(isFine, "Неудалось сортировку по столбцу SM1 > SM2")

        # загрузка предметов

        enough = True
        lines = None
        while enough:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            lines = driver.find_element(By.ID, "table-body").find_elements(By.XPATH, "tr")
            if len(lines) > itemCount:
                enough = False

        print(f"Выбрано {len(lines)} предметов")

        # очищаем таблицу для новых предметов
        db.executeQuery(connection, "DELETE FROM items")
        print("Загрузка предметов в БД:")
        t1 = time.time()
        i = 0
        max = len(lines)
        print(f"  {i}/{max}")
        for line in lines:
            i += 1
            #       25%                 50%             75%
            if round(max / 4) == i or  round(max / 2) == i or round(max / 4 * 3) == i:
                print(f"  {i}/{max}")

            name = line.find_element(By.CLASS_NAME, "copy-name")
            steamLink = line.find_element(By.CLASS_NAME, "field-link").find_element(By.XPATH, "a").get_attribute("href")
            profit = line.find_element(By.CLASS_NAME, "field-profit")
            # добавление предмета в бд
            db.insertItem(connection, name.text, steamLink, profit.text)
        print(f"  {i}/{max}")
        t2 = time.time()
        print(f"Загрузка {max} предметов заняла {t2 - t1} сек")
        print("End fnc getLinks")
        result = True
    except Exception as ex:
        print(ex)
    finally:
        return result

def checkIsFine(isFine, raiseText):
    if not isFine:
        raise Exception(raiseText)

def seleniumClickCheckboxByID(driver, id):
    driver.execute_script(f"document.getElementById('{id}').click()")
