# ONLINE QUIZ SYSTEM

if __name__ == '__main__':
    print("Hii")


from config.db_config import ConnectionToDB

if __name__ == '__main__':
    db_obj=ConnectionToDB()
    db_obj.create_connection()