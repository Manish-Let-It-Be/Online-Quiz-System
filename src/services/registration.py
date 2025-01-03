def register_admin(cursor):
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, 'admin')", (username, password))
        cursor.connection.commit()  # Commit the changes to the database
        print("Admin account created successfully!")
    except Exception as e:
        print(f"Error during registration: {e}")

def register_candidate(cursor):
    username = input("Enter candidate username: ")
    password = input("Enter candidate password: ")

    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, 'candidate')", (username, password))
        cursor.connection.commit()  # Commit the changes to the database
        print("Candidate account created successfully!")
    except Exception as e:
        print(f"Error during registration: {e}")
