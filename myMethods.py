import time
import pickle
from os import remove as removeFile
from os.path import isfile as fileExists
from os.path import getmtime as fileTime

from selenium.common import NoSuchElementException

COOKIE_MODE_LOAD = "load"
COOKIE_MODE_REG = "reg"
COOKIE_MODE_AUTO = "auto"
COOKIE_FILE_NAME = "tb_stem_auth_cookies"

def cookie(driver, mode = COOKIE_MODE_AUTO, DEBUG_MOD = False):
    if DEBUG_MOD:
        print(f"cookie mode: {mode}")
    if mode == COOKIE_MODE_AUTO:
        if fileExists(COOKIE_FILE_NAME):
            fileCreateTime = fileTime(COOKIE_FILE_NAME)
            currentTime = time.time()
            timeSpend = (currentTime - fileCreateTime) / 60 / 60
            if timeSpend > 20:
                mode = COOKIE_MODE_REG
            else:
                mode = COOKIE_MODE_LOAD
        else:
            mode = COOKIE_MODE_REG

    if mode == COOKIE_MODE_LOAD:
        if DEBUG_MOD:
            print("\033[35mload cookie\033[0m")
        for cookie in pickle.load(open(COOKIE_FILE_NAME, "rb")):
            driver.add_cookie(cookie)
    elif mode == COOKIE_MODE_REG:
        if DEBUG_MOD:
            print("\033[35mRemove old cookie\033[0m")
        if fileExists(COOKIE_FILE_NAME):
            removeFile(COOKIE_FILE_NAME)
        input("Pause; Log in and press enter...")
        if DEBUG_MOD:
            print("\033[35msave cookie\033[0m")
        pickle.dump(driver.get_cookies(), open(COOKIE_FILE_NAME, "wb"))

    driver.implicitly_wait(5)



def seleniumExists(driver, by, target):
    try:
        driver.find_element(by, target)
    except NoSuchElementException:
        return False
    return True
