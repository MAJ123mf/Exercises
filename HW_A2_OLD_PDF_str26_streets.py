
""" 
PREJ NAREDIMO:
docker exec -it postgres psql -U postgres
# CREATE DATABASE training;
#exit
docker exec -it postgres psql -U postgres -d training
# CREATE extension postgis;
# create schema d;
# CREATE TABLE d.streets(gid serial primary key, name varchar, length double precision, geom geometry("LINESTRING",25830)); 
  psql -U postgres -d training
# SELECT table_name FROM information_schema.tables WHERE table_schema = 'd';
# GRANT ALL PRIVILEGES ON TABLE d.osebe TO postgres;
# CREATE TABLE d.osebe(id serial primary key, ime varchar(25), priimek varchar(25) not null);
# exit;
"""
import sys
import psycopg2

try:
    # Povezava na PostgreSQL
    conn = psycopg2.connect(
        dbname="training",
        user="postgres",      # iz .env.dev zbirke za postgres instalacijo
        password="postgres",  # iz zbirke env.dev za postgres instalacijo
        host="localhost",     # Ali 'postgres' ce je localhost omrezje
        port="5432"           # Vrata iz .env datoteke za postgres instalacijo
    )

    # Ustvari cursor
    cur = conn.cursor()

    # Nastavi shemo, če ni "public"
    # cur.execute("SET search_path TO d;")

    # SQL ukaz za vstavljanje podatka                 
    
    sql="INSERT INTO d.streets (name, length, geom) VALUES ('Avinguda d`Emilio Attard', 317.83, ST_GeomFromText('LINESTRING(728651.17 4373398.12, 728752.70 4373699.30)', 25830 ) )"
    cur.execute(sql)
    conn.commit()

    query_ins="""INSERT INTO d.streets (name, length, geom) VALUES (%s, %s, ST_GeomFromText(%s, 25830))"""

    # Vrednosti, ki jih zelimo dodati
    values1=["Cami de Vera", 2015.18, "LINESTRING(729404.51 4373515.56, 729324.99 4373542.63, 729313.14 4373554.47, 729307.85 4373565.90, 729305.10 4373573.93, 729302.99 4373584.30, 729297.28 4373590.22, 729294.11 4373599.31, 729292.84 4373611.79, 729296.64 4373626.39, 729324.77 4373708.87, 729345.92 4373774.02, 729335.35 4373812.09, 729323.08 4373834.09, 729320.12 4373853.55, 729328.16 4373864.12, 729329.43 4373875.54, 729324.77 4373886.54, 729315.47 4373891.62, 729302.78 4373893.73, 729288.81 4373886.12, 729285.01 4373881.47, 729267.24 4373878.50, 729237.21 4373881.47, 729199.98 4373885.70, 729149.65 4373891.19, 729131.46 4373890.35, 729098.46 4373881.89, 729066.31 4373875.54, 729036.70 4373873.01, 728952.94 4373864.97, 728897.95 4373857.35, 728847.19 4373851.01, 728800.66 4373842.97, 728739.32 4373831.13, 728674.18 4373847.20, 728615.80 4373869.20, 728479.59 4373919.96, 728366.22 4373954.65, 728329.84 4373958.88, 728297.69 4373948.72, 728202.94 4373875.97, 728131.87 4373811.67, 728121.72 4373798.13, 728108.81 4373787.56, 728101.20 4373780.79, 728100.14 4373772.33, 728103.32 4373764.71, 728109.87 4373758.16, 728102.89 4373750.96, 728092.95 4373742.08, 728069.26 4373739.12, 728041.34 4373734.68, 727976.20 4373674.61, 727928.82 4373636.54)"]
    values2=["Avinguda d'Emilio Attard", 317.83, "LINESTRING(728651.17 4373398.12, 728752.70 4373699.30)"]
    values3=["Carrer de Vicente Enrique Tarancon", 619.82, "LINESTRING(728847.14 4373488.01, 728839.52 4373485.89, 728314.98 4373664.41, 728302.29 4373632.26, 728685.97 4373500.70)"]
    values4=["Carrer de Belisario Beatancur", 1304.77, "LINESTRING(729250.32 4373275.92, 729215.64 4373287.34, 729116.65 4373288.19, 729037.97 4373295.38, 728976.21 4373319.49, 728901.33 4373352.48, 728826.46 4373388.44, 728788.81 4373410.44, 728715.21 4373458.24, 728679.25 4373481.50)"]

    # Izvedba SQL ukaza
    cur.execute(query_ins, values1)
    cur.execute(query_ins, values2)
    cur.execute(query_ins, values3)
    cur.execute(query_ins, values4)

    # Potrditev sprememb
    conn.commit()

    print("Four streets were inserted :) !")

except psycopg2.Error as e:
    print("Napaka pri povezavi ali izvajanju poizvedbe:", e)    

# Zapri povezavo
finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
