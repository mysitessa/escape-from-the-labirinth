import sqlite3

def connect():
    CON = sqlite3.connect('Base_Date.sqlite')
    CUR = CON.cursor()
    return CON, CUR