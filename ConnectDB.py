import psycopg2
class ConnectDB:
    def __init__(self, dbname, dbuser, dbpass, host, port):
        self.__dbname = dbname
        self.__dbuser = dbuser 
        self.__dbpass = dbpass
        self.__host = host  
        self.__port = port

    def ConnectDB(self):
        print("Conectando...")

        try:
            conn = psycopg2.connect(database= self.__dbname,
                                user = self.__dbuser, 
                                password = self.__dbpass, 
                                host = self.__host, 
                                port = self.__port)

            print("Conectado!")
            return conn
            
        except psycopg2.DatabaseError as e:
            print("Um erro ocorreu:", e)
            return None