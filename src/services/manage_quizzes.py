from tabulate import tabulate

def manage_quizzes(cursor):
    while True:
        print("\nManage Quizzes")
        print("1. Add Quiz")
        print("2. Edit Quiz")
        print("3. Delete Quiz")
        print("4. View Quizzes")
        print("5. Back to Admin Dashboard")
        choice = input("Choose an option: ")

        if choice == '1':
            add_quiz(cursor)
        elif choice == '2':
            edit_quiz(cursor)
        elif choice == '3':
            delete_quiz(cursor)
        elif choice == '4':
            view_quizzes(cursor)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")


def add_quiz(cursor):
    quiz_name = input("Enter quiz name: ")
    
    # Ask for a valid category ID
    while True:
        category_id = input("Enter category ID: ")
        
        # Check if the category ID exists in the quiz_categories table
        cursor.execute("SELECT id FROM quiz_categories WHERE id = %s", (category_id,))
        result = cursor.fetchone()
        
        if result:
            break
        else:
            print("Invalid category ID. Please try again with a valid category.")

    try:
        cursor.execute("INSERT INTO quizzes (name, category_id) VALUES (%s, %s)", (quiz_name, category_id))
        cursor.connection.commit()
        print(f"Quiz '{quiz_name}' added successfully!")
    except Exception as e:
        print(f"Error adding quiz: {e}")



def edit_quiz(cursor):
    quiz_id = input("Enter quiz ID to edit: ")
    new_name = input("Enter new quiz name: ")
    try:
        cursor.execute("UPDATE quizzes SET name = %s WHERE id = %s", (new_name, quiz_id))
        cursor.connection.commit()
        print("Quiz updated successfully!")
    except Exception as e:
        print(f"Error editing quiz: {e}")


def delete_quiz(cursor):
    quiz_id = input("Enter quiz ID to delete: ")
    try:
        cursor.execute("DELETE FROM quizzes WHERE id = %s", (quiz_id,))
        cursor.connection.commit()
        print("Quiz deleted successfully!")
    except Exception as e:
        print(f"Error deleting quiz: {e}")


def view_quizzes(cursor):
    try:
        cursor.execute("""
        SELECT quizzes.id, quizzes.name, quiz_categories.name AS category
        FROM quizzes
        INNER JOIN quiz_categories ON quizzes.category_id = quiz_categories.id
        """)
        quizzes = cursor.fetchall()
        if quizzes:
            table = [["ID", "Quiz Name", "Category"]]
            table.extend(quizzes)
            print("\nQuizzes:")
            print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))
        else:
            print("No quizzes found.")
    except Exception as e:
        print(f"Error retrieving quizzes: {e}")
