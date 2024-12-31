import mysql.connector


class ConnectionToDB:
    def create_connection(self):  # create connection to database
        connection = mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="manish", 
            database="demo_user"
        )
        if connection.is_connected():
            cursor=connection.cursor()
            print("Connection established")
            return cursor
        else:
            print("Connection failed")
