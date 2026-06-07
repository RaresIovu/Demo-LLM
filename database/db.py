import sqlite3
import os
from config import DB_PATH
from contextlib import contextmanager

@contextmanager
def get_connection(auto_create = False):
    con = None

    try:
        if not auto_create and not os.path.exists(DB_PATH):
            yield None
            return
        
        con = sqlite3.connect(DB_PATH)
        con.row_factory = sqlite3.Row
        yield con
        con.commit()
    except Exception as e:
        if(con):
            con.rollback()
        raise e
    finally:
        if(con):
            con.close()

