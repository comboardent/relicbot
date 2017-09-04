import sqlite3
import time
import datetime
import random

def connectcustom():
    conn = sqlite3.connect("custom.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS custom (guildid text, prefix text, name text, content text, combined text)")
    conn.commit()
    conn.close()


def connectprofile():
    conn = sqlite3.connect("profile.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS profile (userid text, reputation int, balance text)")
    conn.commit()
    conn.close()

def connect():
    conn = sqlite3.connect("settings.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS prefix (guildid text, prefix string)")
    conn.commit()
    conn.close()

def connecttags():
    conn = sqlite3.connect("tags.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS tag (guildid text, name string, content text)")
    conn.commit()
    conn.close()


def getTime():
    currenttime = time.time()
    datetim = datetime.datetime.fromtimestamp(currenttime).strftime('%c')
    return datetim

def checkIfChanged(id):
    conn = sqlite3.connect("settings.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM prefix WHERE guildid=?", (id,))
    rows=cur.fetchall()
    conn.close()
    if rows:
        return True
    else:
        return False

def getPrefix(id):
    connect()
    conn = sqlite3.connect("settings.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM prefix WHERE guildid=?", (id,))
    rows = cur.fetchall()
    conn.close()
    return str(rows[0][1])



def balance(id1):
    conn = sqlite3.connect("money.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM bank WHERE user=?", (id1,))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return (str(rows[0][1]))

def hasAccount(userid):
    connect()
    uid = userid
    conn = sqlite3.connect("money.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM bank")
    rows = cur.fetchall()
    conn.close()
    if any(uid in s for s in rows):
        return True
    else:
        return False

def hasProfile(userid):
    connect()
    uid = userid
    conn = sqlite3.connect("profile.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM profile")
    rows = cur.fetchall()
    conn.close()
    if any(uid in s for s in rows):
        return True
    else:
        return False


def flip():
    randint = random.randint(0, 1)
    if randint == 0:
        return "heads"
    else:
        return "tails"


def connectbank():
    conn = sqlite3.connect("money.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS bank (user text, balance integer)")
    conn.commit()
    conn.close()

def addmoney(id2, amount):
    connect()
    conn = sqlite3.connect("money.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM bank WHERE user=?", (id2,))
    rows = cur.fetchall()
    bal = rows[0][1]
    total = str(int(amount) + bal)
    cur.execute("UPDATE bank SET balance=? WHERE user=?", (total, id2))
    conn.commit()
    conn.close()


def removemoney(id3, amount):
    connect()
    conn = sqlite3.connect("money.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM bank WHERE user=?", (id3,))
    rows = cur.fetchall()
    bal = rows[0][1]
    total = str(bal - int(amount))
    if int(total) < 0:
        return "Balance can't be negative"
    else:
        cur.execute("UPDATE bank SET balance=? WHERE user=?", (total, id3))
        conn.commit()
        conn.close()