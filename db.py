import sqlite3, datetime
from zoneinfo import ZoneInfo
from config import DB_FILE

india_time = datetime.datetime.now(ZoneInfo("Asia/Kolkata"))

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS bus_loc(
              bus_no TEXT PRIMARY KEY,
              longitude REAL, 
              latitude REAL, 
              last_update DATETIME
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS bus_route(
              bus_no TEXT PRIMARY KEY, 
              route TEXT, 
              departure TEXT, 
              return_time TEXT          
    )""")
    conn.commit()
    conn.close()

def get_all():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM bus_route ORDER BY bus_no")
    rows = c.fetchall()
    conn.close()
    return rows

def add_bus(bus_no, route, departure, return_time):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO bus_route VALUES(?, ?, ?, ?)", (bus_no, route, departure, return_time))
    conn.commit()
    conn.close()

def update_bus(bus_no, route, departure, return_time):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE bus_route SET route=?, departure=?, return_time=? WHERE bus_no=?", (route, departure, return_time, bus_no))
    conn.commit()
    conn.close()

def delete_bus(bus_no):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM bus_route WHERE bus_no=?", (bus_no,)) 
    conn.commit()
    conn.close()

def get_route(bus_no):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT route, departure, return_time FROM bus_route WHERE bus_no=?", (bus_no,))
    row = c.fetchone()
    conn.close()
    return row

def update_location(bus_no, longitude, latitude):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO bus_loc VALUES(?, ?, ?, ?)", (bus_no, longitude, latitude, datetime.now(ZoneInfo("Asia/Kolkata"))))
    conn.commit()
    conn.close()
    
def get_location(bus_no):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM bus_loc WHERE bus_no=?",(bus_no,))
    rows = c.fetchall()
    conn.commit()
    conn.close()
    return rows
