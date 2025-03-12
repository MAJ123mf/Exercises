import os, sys
import psycopg2
import psycopg2.extensions          # This imports extensions from psycopg2, which provides additional utilities for handling PostgreSQL connections and data types.
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)        # This ensures that any text retrieved from the database is returned as Python Unicode string
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)   # This ensures that PostgreSQL arrays of text are handled correctly as Python Unicode strings.
import mySettings

def pgConnect():        # vzpostavljamo povezavo z postgres bazo
    conn = psycopg2.connect(          # konkretni podatki so v mySettings.py. PREDNOST:  Če spremenimo geslo na bazi, ga popravimo samo na enem mestu v kodi... v mySettings.py
        dbname=mySettings.DATABASE,
        user=mySettings.USER,      
        password=mySettings.PASSWORD, 
        host=mySettings.HOST,  
        port=mySettings.PORT )
    return conn

def pgDisconnect(conn):       # odklop z baze postgres 
    cursor=conn.cursor()
    cursor.close()
    conn.close()
