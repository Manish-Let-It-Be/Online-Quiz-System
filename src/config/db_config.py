# import mysql.connector

# class ConnectToDb:
#      def create_connection(self):
#          connection = mysql.connector.connect(
#              user="root",
#              password="manish",
#              host="localhost",
#              database="quizdb"
#          )
#          if connection.is_connected():
#              cursor=connection.cursor()
#              print("Connection Established :)")
#              return cursor
#          else:
#              print("Something Wrong")

# # # Example usage
# # db = ConnectToDb()
# # connection = db.create_connection()




import mysql.connector
from mysql.connector import Error

class ConnectToDb:
    def __init__(self):
        self.connection = None

    def create_connection(self):
        try:
            self.connection = mysql.connector.connect(
                user="root",
                password="manish",
                host="localhost",
                database="quizdb"
            )
            if self.connection.is_connected():
                cursor = self.connection.cursor()
                print("Connection Established :)")
                return cursor
        except Error as e:
            print(f"Error: {e}")
            return None

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Connection Closed.")

# # Example usage (optional)
# if __name__ == "__main__":
#     db = ConnectToDb()
#     cursor = db.create_connection()
#     # Perform database operations...
#     db.close_connection()
