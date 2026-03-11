from database.db import get_connection

def get_knowledge(id):
    con = get_connection()
    cur = con.cursor()
    cur.execute(
    "SELECT * FROM products WHERE id = ?",
    (id,)
    )
    row = cur.fetchone()
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
    "INSERT INTO products (name, price) VALUES (LOWER(?), LOWER(?))",
    (name, price)
    )
    con.commit()
    con.close()

