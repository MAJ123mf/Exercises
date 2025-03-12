import pgUtils

conn=pgUtils.pgConnect()
cursor=conn.cursor()

# izpiši vse stavbe
query_sel="SELECT gid, description, st_astext(geom) FROM d.buildings"; 
cursor.execute(query_sel)

# ali izpiši le tiste, ki se začnejo na building 82...
# query_sel="SELECT gid, description, st_astext(geom) FROM d.buildings WHERE description LIKE %s ORDER BY description"
# cursor.execute(query_sel,["building 82%"])

listOfRows=cursor.fetchall()
for row in listOfRows:
    print(row, "\n");

pgUtils.pgDisconnect(conn)