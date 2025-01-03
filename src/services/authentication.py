def user_login(cursor, role):
    username = input(f"Enter your {role} username: ")
    password = input(f"Enter your {role} password: ")

    try:
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s AND role = %s", (username, password, role))
        user = cursor.fetchone()
        
        if user:
            print(f"{role.capitalize()} logged in successfully!")
            return user  # Return user details if login is successful
        else:
            print(f"Invalid {role} credentials. Please try again.")
            return None
    except Exception as e:
        print(f"Error during login: {e}")
        return None


def save_quiz_score(cursor, user_id, quiz_id, score):
    try:
        cursor.execute("INSERT INTO scores (user_id, quiz_id, score) VALUES (%s, %s, %s)", (user_id, quiz_id, score))
        cursor.connection.commit()  # Commit the changes to the database
        print(f"Your score of {score} has been saved!")
    except Exception as e:
        print(f"Error saving score: {e}")
