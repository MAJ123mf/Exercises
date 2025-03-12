# import sys
import mySettings
import psycopg2
import psycopg2.extensions          # This imports extensions from psycopg2, which provides additional utilities for handling PostgreSQL connections and data types.
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)        # This ensures that any text retrieved from the database is returned as Python Unicode string
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)   # This ensures that PostgreSQL arrays of text are handled correctly as Python Unicode strings.

# Povezava na PostgreSQL
conn = psycopg2.connect(
    dbname=mySettings.DATABASE,
    user=mySettings.USER,      
    password=mySettings.PASSWORD, 
    host=mySettings.HOST,  
    port=mySettings.PORT
)

# Ustvari cursor
cur = conn.cursor()

# SQL ukaz za spreminjanje podatkov v enem zapisu                
query_upd="""UPDATE d.buildings SET (description, area, geom) = row(%s, st_area(geom), st_geometryfromtext(%s, 25830))  WHERE description = %s"""

# Vrednosti, ki jih želimo popraviti
values=["Edificio 2", "POLYGON((727988 4373188, 728054 4373192, 728095.842 4373142.837, 728051 4373093, 727983 4373093, 727988 4373188))","edificio 2"]

# Izvedba SQL ukaza
cur.execute(query_upd, values)
n = cur.rowcount
# Potrditev sprememb
conn.commit()

# Zapri povezavo
cur.close()
conn.close()

print('Popravil si ', n,' zapisov.')