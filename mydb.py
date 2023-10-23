import sqlite3
from sqlite3 import Error
from datetime import datetime

WRAP_LINK = "link"
PATH = "dbmain.sqlite"
WRAP_AUTO = "auto"
WRAP_STRING = "string"
WRAP_REAL = "real"
WRAP_INT = "int"
TABLE_CREATE_ITEMS = (
    "CREATE TABLE IF NOT EXISTS items ("
    "id INTEGER PRIMARY KEY AUTOINCREMENT"
    ", name TEXT NOT NULL"
    ", link TEXT NOT NULL"
    ", tb_margin REAL NOT NULL"
    ", buy_price REAL"
    ", sell_price REAL"
    ", buy_order INTEGER"
    ", sell_lot INTEGER"
    ", margin REAL"
    ", status INTEGER DEFAULT 0"
    ", date_update DATE CURRENT_TIMESTAMP"
    ");"
)

TABLE_CREATE_CHECK_ITEMS = (
    "CREATE TABLE IF NOT EXISTS check_items ("
    "id INTEGER PRIMARY KEY AUTOINCREMENT"
    ", name TEXT NOT NULL"
    ", link TEXT NOT NULL"
    ", status INTEGER DEFAULT 0"
    ", date_update DATE CURRENT_TIMESTAMP"
    ");"
)


def createConnection():
    connection = None
    try:
        connection = sqlite3.connect(PATH)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    # создание таблиц если их нет
    executeQuery(connection, TABLE_CREATE_ITEMS)
    executeQuery(connection, TABLE_CREATE_CHECK_ITEMS)
    return connection

def executeQuery(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        # print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
        print(query)


def executeReadQuery(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def updateItem(connection, field, value, where):
    query = f"UPDATE items SET {field} = {wrap(value, WRAP_AUTO)}, date_update = '{datetime.now()}' WHERE {where}"
    executeQuery(connection, query)


def removeItem(connection, id = 0, name = ""):
    query = ""
    if id == 0:
        if name == "":
            raise Exeption("Неправильное использование функции removeItem, обязательно использовать один из аргументов")
        else:
            #remove by name
            query = f"DELETE FROM items WHERE name = {wrap(name, WRAP_STRING)}"
    else:
        #remove by id
        query = f"DELETE FROM items WHERE id = {wrap(id, WRAP_INT)}"

    executeQuery(connection, query)


def insertItem(connection, name, link, tb_margin,
    buy_price = None, sell_price = None, buy_order = None,
    sell_lot = None, margin = None, date_update = None):
    query = "INSERT INTO items (name, link, tb_margin"
    values = f" VALUES ({wrap(name, WRAP_STRING)}, {wrap(link, WRAP_LINK)}, {wrap(tb_margin, WRAP_REAL)}"

    if buy_price != None:
        query += ", buy_price"
        values += f", {wrap(buy_price, WRAP_REAL)}"

    if sell_price != None:
        query += ", sell_price"
        values += f", {wrap(sell_price, WRAP_REAL)}"

    if buy_order != None:
        query += ", buy_order"
        values += f", {wrap(buy_order, WRAP_INT)}"

    if sell_lot != None:
        query += ", sell_lot"
        values += f", {wrap(sell_lot, WRAP_INT)}"

    if margin != None:
        query += ", margin"
        values += f", {wrap(margin, WRAP_REAL)}"

    if date_update != None:
        query += ", date_update"
        values += f", {date_update}"

    query += ", date_update)"
    values += f", '{datetime.now()}');"
    # print(query+values)

    executeQuery(connection, query+values)

def wrap(item, wrapType):
    if(wrapType == WRAP_AUTO):
        if isinstance(item, str):
            wrapType = WRAP_STRING

        if isinstance(item, int):
            wrapType = WRAP_INT

        if isinstance(item, float):
            wrapType = WRAP_REAL

    if wrapType == WRAP_STRING:
        item = item.replace("'","")
        return f"'{item}'"

    if wrapType == WRAP_LINK:
        item = item.replace("'","%27")
        return f"'{item}'"

    if wrapType == WRAP_REAL:
        return float(item)

    if wrapType == WRAP_INT:
        return int(item)








