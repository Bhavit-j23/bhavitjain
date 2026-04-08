import sqlite3

DB = "database.db"


def create():

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
    username TEXT,
    password TEXT
    )
    """)

    con.commit()
    con.close()


create()


def signup_user(user, pw):

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("INSERT INTO users VALUES (?,?)", (user, pw))

    con.commit()
    con.close()


def login_user(user, pw):

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (user, pw)
    )

    data = cur.fetchone()

    con.close()

    return data is not None