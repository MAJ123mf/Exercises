import pgUtils

conn=pgUtils.pgConnect()
cursor=conn.cursor()

query_del='DELETE FROM d.buildings WHERE description = %s'
value=['Edificio 2']
cursor.execute(query_del, value)
n = cursor.rowcount
conn.commit()

print('Brisal si ', n,' zapisov.')
pgUtils.pgDisconnect(conn)
