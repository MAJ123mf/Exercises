import sys
import mySettings
import psycopg2

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

# SQL ukaz za vstavljanje podatka                 
query_ins="insert into d.buildings (description, geom) values (%s,st_geometryfromtext(%s,25830))"


# Vrednosti, ki jih želimo dodati
values1=["edificio 1", "POLYGON((727844 4373183,727896 4373187,727893 4373028,727873 4373018,727858 4372987,727796 4372988,727782 4373008,727844 4373183, 727844 4373183))"]
values2=["edificio 2", "POLYGON((727988 4373188,728054 4373192,728051 4373093,727983 4373093,727988 4373188))"]

# Izvedba SQL ukaza
cur.execute(query_ins, values1)
cur.execute(query_ins, values2)

# Potrditev sprememb
conn.commit()

# Zapri povezavo
cur.close()
conn.close()

print("Two buildings were inserted!")