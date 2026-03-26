from database.db import get_connection
from exceptions import DuplicateException

def get_knowledge(id):
    con = get_connection()
    cur = con.cursor()
    cur.execute(
    "SELECT * FROM products WHERE id = ?",
    (id,)
    )
    row = cur.fetchone()
    if not row:
        return None
    con.close()
    data = {
        "id":row[0],
        "name":row[1],
        "price":row[2]
    }
    return data

def add_knowledge(name, price):
    con = get_connection()
    cur = con.cursor()

    cur.execute(
    "SELECT 1 FROM products WHERE LOWER(name) = LOWER(?)",
    (name,)
    )
    if cur.fetchone():
        raise DuplicateException("Product already exists")
    cur.execute(
    "INSERT INTO products (name, price) VALUES (?, ?)",
    (name, price)
    )
    new_id = cur.lastrowid
    con.commit()
    con.close()
    item = {
        "id": new_id,
        "name": name,
        "price": price
    }
    return item

