from tabulate import tabulate


def manage_categories(cursor):
    while True:
        print("\nManage Categories")
        print("1. Add Category")
        print("2. Edit Category")
        print("3. Delete Category")
        print("4. View All Categories")
        print("5. Back to Admin Dashboard")
        choice = input("Choose an option: ")

        if choice == '1':
            add_category(cursor)
        elif choice == '2':
            edit_category(cursor)
        elif choice == '3':
            delete_category(cursor)
        elif choice == '4':
            view_all_categories(cursor)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")


def add_category(cursor):
    category_name = input("Enter new category name: ")
    try:
        cursor.execute("INSERT INTO quiz_categories (name) VALUES (%s)", (category_name,))
        cursor.connection.commit()
        print(f"Category '{category_name}' added successfully!")
    except Exception as e:
        print(f"Error adding category: {e}")


def edit_category(cursor):
    category_id = input("Enter category ID to edit: ")
    new_name = input("Enter new category name: ")
    try:
        cursor.execute("UPDATE quiz_categories SET name = %s WHERE id = %s", (new_name, category_id))
        cursor.connection.commit()
        print("Category updated successfully!")
    except Exception as e:
        print(f"Error editing category: {e}")


def delete_category(cursor):
    category_id = input("Enter category ID to delete: ")
    try:
        cursor.execute("DELETE FROM quiz_categories WHERE id = %s", (category_id,))
        cursor.connection.commit()
        print("Category deleted successfully!")
    except Exception as e:
        print(f"Error deleting category: {e}")


def view_all_categories(cursor):
    try:
        cursor.execute("SELECT * FROM quiz_categories")
        categories = cursor.fetchall()
        if categories:
            table = [["ID", "Name"]]
            table.extend(categories)
            print("\nQuiz Categories:")
            print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))
        else:
            print("No categories found.")
    except Exception as e:
        print(f"Error retrieving categories: {e}")
