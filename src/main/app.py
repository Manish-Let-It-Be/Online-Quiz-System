# import sys
# import os

# # Add the parent directory to the system path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from config.db_config import ConnectToDb

# if __name__ == "__main__":
#     db_object=ConnectToDb()
#     db_object.create_connection()



# src/main/app.py

import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db_config import ConnectToDb
from services.manage_categories import manage_categories
from services.manage_quizzes import manage_quizzes
from services.manage_questions import manage_questions
from services.candidate_dashboad import candidate_dashboard
from services.authentication import user_login
from services.registration import register_admin, register_candidate


def main():
    db_object = ConnectToDb()
    cursor = db_object.create_connection()

    if cursor:
        while True:
            print("\nWelcome to the Online Quiz System!")
            print("1. Admin Login")
            print("2. Candidate Login")
            print("3. Admin Registration")
            print("4. Candidate Registration")
            print("5. Exit")
            choice = input("Choose an option: ")

            if choice == '1':
                admin = user_login(cursor, 'admin')
                if admin:
                    admin_dashboard(cursor)
            elif choice == '2':
                candidate = user_login(cursor, 'candidate')
                if candidate:
                    candidate_dashboard(cursor)
            elif choice == '3':
                register_admin(cursor)
            elif choice == '4':
                register_candidate(cursor)
            elif choice == '5':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

        db_object.close_connection()

def admin_dashboard(cursor):
    while True:
        print("\nAdmin Dashboard")
        print("1. Register Admin")
        print("2. Register Candidate")
        print("3. View Categories")
        print("4. Manage Quizzes")
        print("5. Manage Questions")
        print("6. Logout")
        
        choice = input("Choose an option: ")

        if choice == '1':
            register_admin(cursor)
        elif choice == '2':
            register_candidate(cursor)
        elif choice == '3':
            manage_categories(cursor)
        elif choice == '4':
            manage_quizzes(cursor)
        elif choice == '5':
            manage_questions(cursor)
        elif choice == '6':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")



if __name__ == "__main__":
    main()

