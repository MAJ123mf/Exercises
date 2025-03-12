import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import psycopg2
from mylib import settings
from mylib.db import Db

db = Db()   # ustvarimo instanco objekta db

# conn=psycopg2.connect(                              To naredi že zgornja vrstica! objekt db ima konstruktor, kjer se to naredi !
#                 host=settings.POSTGRES_HOST,   
#                 port=settings.POSTGRES_PORT,
#                 dbname=settings.POSTGRES_DB,
#                 user=settings.POSTGRES_USER,
#                 password=settings.POSTGRES_PASSWORD
#                 )
#
# TA DEL BOM ZAKOMENTIRAL, NEKAKO NE PAŠE V CELO ZGODBO,  ni objekta db v igri, ampak zadeva deluje - je preprost primer vstavljanja.
# VES TA ZAKOMENTIRAN DEL BI LAHKO BIL SVOJ PROGRAMČEK vstavi.py
#-------------------------------------------------------------------------
# cursor=conn.cursor()
# cons="""INSERT INTO d.buildings ("descripcion", "area") values (%s,%s)"""
# cursor.execute(cons, ['First building', 200])
# conn.commit()
# cursor.close()
# conn.close()
# print("Done")
#-------------------------------------------------------------------------

def insert():
    geometry= 'POLYGON((0 0, 100 0, 100 100, 0 100, 0 0))'
    cons="INSERT INTO d.buildings (descripcion, area, geom) values (%s,%s, st_geometryfromtext(%s,25830)) returning gid"    # gid imamo v bazi ne id
    values=['Second building 2', 200, geometry]
    db.query(cons, values)                               # tu prvič kličemo funkcijo iz db.py

def update():
    geometry= 'POLYGON((0 0, 100 0, 100 100, 0 100, 0 0))'
    cons="UPDATE d.buildings SET (descripcion, area, geom) = ROW(%s,%s, st_geometryfromtext(%s,25830)) WHERE gid=%s"
    values=['Building 2', 177, geometry, 2]    # Popravljamo zapis 2, stavba se bo imenovala Building 2, njena površina bo 177, ...
    db.query(cons, values)

# Zbrišeš vse stavbe, ki imajo površino manjšo  od 300
def delete():
    cons="DELETE FROM d.buildings WHERE area < %s"
    values=[300]
    db.query(cons, values)

# Zbrišeš stavbo katere gID=2
def delete2():
    cons="DELETE FROM d.buildings WHERE gid = %s"
    values=[2]
    db.query(cons, values)

 # Zbrišeš stavbo katere gID=poljuben določen v galvnem programu
def deleteX(rec_num):
    cons="DELETE FROM d.buildings WHERE gid = %s"
    values=[rec_num]
    db.query(cons, values)   

# Izpišemo vsa polja stavb za eno stavbi, in sicer za tisto, ki ima gid=1    
def SelectAsTuples():
    cons="SELECT gid, descripcion, area, st_astext(geom) FROM d.buildings WHERE gid = %s"
    values=[1]
    db.query(cons, values)
# ne z zvezdico ali le z geom, da ne dobimo poligon v binarni obliki,  lahko bi napisali tudi kot: st_asgeojson(geom) --> ST_ASTEXT vrne čitljive podatke

# Select v obliki DICTIONARY podatkovne strukture.
def SelectAsDicts():
    cons=""" 
        select array_to_json(array_agg(filas)) FROM (
            SELECT gid, descripcion, area, st_astext(geom) FROM d.buildings WHERE gid = %s
        ) as filas 
        """
    values=[1]
    db.query(cons, values)

def checkIntersectionBeforeInsert():
    polygon= "POLYGON((0.00001 0.00001, 100.00001 0.00001, 100.00001 100.00001, 0.00001 100.00001, 0.00001 0.00001))"
    
    query="""
        select gid from d.buildings where
        st_intersects
        (
            geom,
            st_snaptogrid(
                st_geometryfromtext(
                    %s,
                    25830
                    ),
                0,001
            )
        )
        """
    db.query(query, [polygon])
    if len(db.results)>0:
        print('The new polygon intersects with the others in the table: {db.result}')
        return

    query="""select st_isvalid(st_snapgrid(%s,%s))"""
    db.query(query, [polygon, settings.ST_SNAPTOGRID_DISTANCE])
    if not db.result[0][0]: #true o false
        print('The new polygon is not valid after st_snapToGrid')
        return
                                                        
    query="""
        INSERT INTO d.buildings (descripcion, area, geom)
        values (%s,
        st_area(
            st_snaptogrid(
                st_geometryfromtext(%s,25830),
                %s
            )    
        )
        ,
            st_snaptogrid(
                st_geometryfromtext(%s,25830),
                %s
            )    
        ) returning gid
        """

    db.query(query,['Con snap',polygon, settings.ST_SNAPTOGRID_DISTANCE, polygon, settings.ST_SNAPTOGRID_DISTANCE])


if __name__ == '__main__':
    # To je glavni program. Sedaj bomo klicali metode. Najprej vstavljanje v bazo:
    # ODKOMENTIRAŠ SKLOP; KI BI GA RAD TESTIRAL (VSTAVLJANJE; BRISANJE; POPRAVLJANJE; SELEKTIRANJE)
    
    # print('INSERTING records:')
    # insert()
    # # Zahtevnejše vstavljanje brez vnaprej pripravljene metode...
    # query = "insert into d.buildings (descripcion, geom) values (%s, st_geometryfromtext(%s,25830)) returning gid"
    # values1=["edificio 3", "POLYGON((727844 4373183,727896 4373187,727893 4373028,727873 4373018,727858 4372987,727796 4372988,727782 4373008,727844 4373183, 727844 4373183))"]
    # values2=["edificio 4", "POLYGON((727988 4373188,728054 4373192,728051 4373093,727983 4373093,727988 4373188))"]
    # db.query(query, values1)
    # db.query(query, values2)

    # print('DELETING records:')
    # deleteX(12)       # brišemo zapis ki ima gid=12   (prej v PgAdmin pogledamo kakšne zapise imamo, in poiščemo id tistega ki ga bomo brisali), dobimo vrnjeno število zapisov, ki smo jih brisali 

    # print('UPDATING records:')
    # update()    #  Kliče zgornjo metodo... vrstica 36   Rezultat, ki se izpiše pove koliko zapisov smo spremenili. Spremembo vidiš v PgAdmin
    # # še en update:
    # query="update d.buildings set (descripcion, geom) = row(%s, st_geometryfromtext(%s,25830)) where gid=%s"  # spreminjamo stavbo z gid=5
    # values=["Edificio actualizado - posodobljena stavba", "POLYGON((727988 4373188, 728054 4373192, 728095.84297791088465601 4373142.83781164418905973, 728051 4373093, 727983 4373093, 727988 4373188))",5]
    # db.query(query, values)

    # izpis as Tuples [ , , ]
    print('SELECTING records:')    # SELECTING ROWS as  Tuples [ , , ]
    print('as Tuples:')
    SelectAsTuples()    # izpiše stavbo 1
    query="select gid, descripcion, st_astext(geom) from d.buildings where gid= %s "
    values=[9]                # izpisali si bomo zapis, ki ima gid=9
    db.query(query, values)
    # izpis as Dictionary {gid: .., descripcion: .., geom: ..}
    print('as Dictionary:')
    SelectAsDicts()    # pogledali si bomo zapis z gid=1
    query="select array_to_json(array_agg(filas)) FROM (select gid, descripcion, st_astext(geom) from d.buildings where gid=%s) as filas"  # as filas = as vrstice
    values=[16]         # pogledali si bomo zapis 16 še enkrat
    db.query(query, values)