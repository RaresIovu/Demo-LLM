from database.db import get_connection

def get_allKnowledge():
    with get_connection() as con: #with deschide conexiunea catre database, si o comiteaza automat 
        cur = con.cursor() #cursor = pointer care tine cont unde ne aflam in lista(in cazul nostru de produse)
        #De asemenea executa operatii in baza de date
        cur.execute("SELECT * FROM products") # * - all. Se selecteaza toate obiectele si se introduc in cursor
        rows = cur.fetchall() # Toate obiectele sunt transmise din cursor in variabila rows
        if not rows:
            return [] # Nu exista obiecte
        
        content = []
        for row in rows:
            content.append({
                "id": row[0],
                "name":row[1],
                "price":row[2]
            }) # Se adauga cate un obiect de tip produs

        return content
        
        
def get_knowledge(id):
    with get_connection() as con:
        cur = con.cursor()
        cur.execute(
        "SELECT * FROM products WHERE id = ?", (id,)) #se selecteaza fiecare produs din products unde id-ul este cel transmit prin parametru
         #Metoda accepta ca parametru doar tuple, "," transforma parametrul in unul
        row = cur.fetchone() # Se transmite un singur obiect din cursor catre variabila row(un singur produs)
        if not row:
            return None

        data = {
            "id":row[0],
            "name":row[1],
            "price":row[2]
        }
        return data

def add_knowledge(name, price):
    with get_connection() as con:
        cur = con.cursor()
        cur.execute(
        "SELECT 1 FROM products WHERE LOWER(name) = LOWER(?)",
        (name,)
        ) #Selectam orice element(indiferent de care ar fi acesta) din baza de date, unde numele este acelasi
        # Ca cel transmis prin parametru. Duplicate checking
        if cur.fetchone():
            raise Exception("Product already exists") #Se ridica o exceptie, efectiv se returneaza si se instantiaza un obiect
        # de tip DuplicateException cu mesajul de mai sus
        cur.execute("INSERT INTO products (name, price) VALUES (?, ?) RETURNING id, name, price", (name, price))
        row = cur.fetchone()
        item = {
            "id": row[0],
            "name": row[1],
            "price": row[2]
        }
        return item #Se returneaza obiectul adaugat, pentru confirmare, integritate a datelor, pentru ca clientul sa primeasca id-ul, etc

def update_product_price(produs_id, new_price):
    with get_connection() as con:
        cur = con.cursor()
        cur.execute("SELECT 1 FROM products WHERE id = ?", (produs_id,))
        if not cur.fetchone():
            return None
        
        cur.execute("UPDATE products SET price = ? WHERE id = ? RETURNING id, name, price", (new_price, produs_id))
        row = cur.fetchone()
        return {
            "id": row[0],
            "name": row[1],
            "price": row[2]
        }

