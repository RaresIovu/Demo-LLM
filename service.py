from database.db import get_connection
from exceptions import DuplicateException

def get_allKnowledge():
    with get_connection() as con: #with deschide conexiunea catre database, si o inchide automat cand se iese din blocul indentat
        cur = con.cursor() #cursor = pointer care tine cont unde ne aflam in lista(in cazul nostru de produse)
        #De asemenea executa operatii in baza de date
        cur.execute(
            "SELECT * FROM products" # * - all. Se selecteaza toate obiectele si se introduc in cursor
        )
        rows = cur.fetchall() # Toate obiectele sunt transmise din cursor in variabila rows
        if not rows:
            return None # Nu exista obiecte
        
        content = []
        for row in rows:
            content.append({
                "id": row[0],
                "name":row[1],
                "price":row[2]
            }) # Se adauga cate un obiect de tip produs

        return content
        
def get_knowledge(id):
    con = get_connection() #Se deschide conexiunea la db
    cur = con.cursor()
    cur.execute(
    "SELECT * FROM products WHERE id = ?", #se selecteaza fiecare produs din products unde id-ul este cel transmit prin parametru
    (id,) #Metoda accepta ca parametru doar tuple, "," transforma parametrul in unul
    )
    row = cur.fetchone() # Se transmite un singur obiect din cursor catre variabila row(un singur produs)
    con.close() #Se inchide conexiunea la db, INAINTE de return
    if not row:
        return None

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
    ) #Selectam orice element(indiferent de care ar fi acesta) din baza de date, unde numele este acelasi
    # Ca cel transmis prin parametru. Duplicate checking
    if cur.fetchone():
        con.close() #Ca sa nu ramanem cu conexiunea deschisa mereu
        raise DuplicateException("Product already exists") #Se ridica o exceptie, efectiv se returneaza si se instantiaza un obiect
    # de tip DuplicateException cu mesajul de mai sus
    cur.execute(
    "INSERT INTO products (name, price) VALUES (?, ?)",
    (name, price)
    )
    new_id = cur.lastrowid
    con.commit() #Salvam schimbarile in db
    con.close()
    item = {
        "id": new_id,
        "name": name,
        "price": price
    }
    return item #Se returneaza obiectul adaugat, pentru confirmare, integritate a datelor, pentru ca clientul sa primeasca id-ul, etc

