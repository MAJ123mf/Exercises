# Program vstavi grafiko v WKT formatu v tabelo desveb.d.buildings
# to je primer v PDF skripti na strani 25
import sys
import psycopg2

# Podatki za povezavo na PostgreSQL
try:
    conn = psycopg2.connect(
        dbname="desweb",
        user="postgres",      # iz .env.dev zbirke za postgres instalacijo
        password="postgres",  # iz zbirke env.dev za postgres instalacijo
        host="localhost",     # Ali 'postgres' če je localhost omrežje
        port="8440"           # Vrata iz .env datoteke za postgres instalacijo
    )

    # Ustvari cursor - vzpostavi povezavo na bazo na podlagi zgornjih podatkov 
    cursor = conn.cursor()

    # cursor.execute("SELECT current_database();")
    # print("Povezan sem na bazo:", cursor.fetchone()[0])
    # print("Povezan sem na:", conn.get_dsn_parameters())

    query_ins="INSERT INTO d.buildings (description, geom) VALUES (%s,st_geometryfromtext(%s,25830))"
    values1=["edificio 1", "POLYGON((727844 4373183,727896 4373187,727893 4373028,727873 4373018,727858 4372987,727796 4372988,727782 4373008,727844 4373183, 727844 4373183))"]
    values2=["edificio 2", "POLYGON((727988 4373188,728054 4373192,728051 4373093,727983 4373093,727988 4373188))"]
    cursor.execute(query_ins, values1)
    cursor.execute(query_ins, values2)                 # naredimo 2 inserta in 
    conn.commit()                                      # en comit   (dejansko zapiše v bazo)    

    print("Dva poligona sta uspešno vstavljena!")

# Če lahko naredi, sicer izpiši napako...
except psycopg2.Error as e:
    print("Napaka pri povezavi ali izvajanju poizvedbe:", e)    

# Zapri povezavo
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()