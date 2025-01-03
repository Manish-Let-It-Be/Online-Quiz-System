from tabulate import tabulate

def manage_questions(cursor):
    while True:
        print("\nManage Questions")
        print("1. Add Question")
        print("2. Edit Question")
        print("3. Delete Question")
        print("4. View Questions")
        print("5. Back to Admin Dashboard")
        choice = input("Choose an option: ")

        if choice == '1':
            add_question(cursor)
        elif choice == '2':
            edit_question(cursor)
        elif choice == '3':
            delete_question(cursor)
        elif choice == '4':
            view_questions(cursor)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")


def add_question(cursor):
    quiz_id = input("Enter quiz ID for the question: ")
    
    # Validate if the quiz ID exists
    cursor.execute("SELECT id FROM quizzes WHERE id = %s", (quiz_id,))
    result = cursor.fetchone()
    
    if result:
        question_text = input("Enter question text: ")
        option_a = input("Enter option A: ")
        option_b = input("Enter option B: ")
        option_c = input("Enter option C: ")
        option_d = input("Enter option D: ")
        correct_option = input("Enter correct option (A/B/C/D): ")

        try:
            cursor.execute("""
                INSERT INTO questions (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option))
            cursor.connection.commit()
            print("Question added successfully!")
        except Exception as e:
            print(f"Error adding question: {e}")
    else:
        print("Invalid quiz ID. Question not added.")


def edit_question(cursor):
    question_id = input("Enter question ID to edit: ")
    
    # Check if question exists
    cursor.execute("SELECT * FROM questions WHERE id = %s", (question_id,))
    question = cursor.fetchone()

    if question:
        print(f"Editing question: {question[1]}")
        new_question_text = input("Enter new question text (or press Enter to keep the current one): ")
        new_option_a = input("Enter new option A (or press Enter to keep the current one): ")
        new_option_b = input("Enter new option B (or press Enter to keep the current one): ")
        new_option_c = input("Enter new option C (or press Enter to keep the current one): ")
        new_option_d = input("Enter new option D (or press Enter to keep the current one): ")
        new_correct_option = input("Enter new correct option (A/B/C/D, or press Enter to keep the current one): ")

        try:
            # Update question if new values are provided
            cursor.execute("""
                UPDATE questions
                SET 
                    question_text = COALESCE(NULLIF(%s, ''), question_text),
                    option_a = COALESCE(NULLIF(%s, ''), option_a),
                    option_b = COALESCE(NULLIF(%s, ''), option_b),
                    option_c = COALESCE(NULLIF(%s, ''), option_c),
                    option_d = COALESCE(NULLIF(%s, ''), option_d),
                    correct_option = COALESCE(NULLIF(%s, ''), correct_option)
                WHERE id = %s
            """, (new_question_text, new_option_a, new_option_b, new_option_c, new_option_d, new_correct_option, question_id))
            cursor.connection.commit()
            print("Question updated successfully!")
        except Exception as e:
            print(f"Error updating question: {e}")
    else:
        print("Question ID not found.")


def delete_question(cursor):
    question_id = input("Enter question ID to delete: ")
    
    # Check if question exists
    cursor.execute("SELECT * FROM questions WHERE id = %s", (question_id,))
    question = cursor.fetchone()

    if question:
        try:
            cursor.execute("DELETE FROM questions WHERE id = %s", (question_id,))
            cursor.connection.commit()
            print("Question deleted successfully!")
        except Exception as e:
            print(f"Error deleting question: {e}")
    else:
        print("Question ID not found.")


def view_questions(cursor):
    quiz_id = input("Enter quiz ID to view questions: ")
    
    try:
        cursor.execute("SELECT * FROM questions WHERE quiz_id = %s", (quiz_id,))
        questions = cursor.fetchall()
        
        if questions:
            table = [["ID", "Question Text", "Option A", "Option B", "Option C", "Option D", "Correct Option"]]
            table.extend(questions)
            print("\nQuestions:")
            print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))
        else:
            print("No questions found for this quiz.")
    except Exception as e:
        print(f"Error retrieving questions: {e}")
