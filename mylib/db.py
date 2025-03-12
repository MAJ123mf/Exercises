import psycopg2
from mylib import settings

class Db:
    def __init__(self, autoCommit=True, autoPrintResults=True):   # Tej metodi pravimo CONSTRUCTOR 
        self.conn = psycopg2.connect(
                    host=settings.POSTGRES_HOST,
                    port=settings.POSTGRES_PORT,
                    dbname=settings.POSTGRES_DB,
                    user=settings.POSTGRES_USER,
                    password=settings.POSTGRES_PASSWORD
                    )
        self.cursor = self.conn.cursor()
        self.autoCommit = autoCommit
        self.autoPrintResults = autoPrintResults
        self.result = None
        if self.autoPrintResults:                  # To je vedno res, ker je tako nastavljeno v atributih konstruktorja
            print ('Connected to database')

    def query(self, query, params=None):
        #    Execute a query and return the results                                         
        #    eg. query("SELECT * FROM table WHERE area > %s and owner
        #        like %s", [100], [’%Smith%’]))
        #
        #    query: the query to execute. Use %s as a placeholder for 
        #        parameters. Eg. "SELECT * FROM table WHERE area > %s
        #        and owner like %s"
        #    params: the parameters to pass to the query in a list.
        #        Eg. [100, ’%Smith%’]
        #    return: the results of the query in a list. Eg. [(1, ’
        #        Smith’, 200), (2, ’Smith’, 300)]
        #
        self.cursor.execute(query, params)
        if self.autoCommit:
            self.conn.commit()
        # INPUT ali SELECT vrneta rezultat v: cursor.fetchall(),
        # UPDATE in DELETE pa tega ne vračata
        # UPDATE in DELETE vrneta rezultat operacije v cursor.rowcount
        # INSERT in SELECT pa tega ne naredita
        # So we have to manage this:
        if 'insert' in query.lower() or 'select' in query.lower():    # Python ukaz: lower SQL ukaz spremeni v same male črke, npr "Select" ali "SELECT" --> "select"
            self.result = self.cursor.fetchall()
        else:
            # operations update and delete
            self.result = self.cursor.rowcount     # preštejemo na koliko zapisov sta vplivala ukaza UPDATE ali DELETE
        if self.autoPrintResults:
            self.printResult()            

    def commit(self):
        self.conn.commit()              # poknjižimo spremembe iz "začasne tabele" v bazo
        if self.autoPrintResults:
            print('Changes commited')

    def disconnect(self):
        # Disconnect from the database. This should be called when
        # the connection is no longer needed.
        # There is a maximum number of connections that can be
        # made to the database, so it is important to
        # disconnect when the connection is no longer needed.
        self.cursor.close()
        self.conn.close()
        if self.autoPrintResults:
            print('Disconnected from database') 
            
    def printResult(self):
        print(self.result)

    def __del__(self):                  # tej metodi pravimo DESTRUCTOR
        # Destructor. Disconnect from the database.
        # On destruction of the object, disconnect from the database.
        # This is automatically called when
        # the object is deleted, eg. when the program ends.
        self.disconnect()               # samo kliče zgorno metodo
        print('I am beeing destroyed')        