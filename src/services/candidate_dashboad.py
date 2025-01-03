from tabulate import tabulate
from time import time

def candidate_dashboard(cursor):
    while True:
        print("\nCandidate Dashboard")
        print("1. View Categories")
        print("2. View Quizzes")
        print("3. Take Quiz")
        print("4. View Scoreboard")
        print("5. Logout")
        choice = input("Choose an option: ")

        if choice == '1':
            view_categories(cursor)
        elif choice == '2':
            view_quizzes(cursor)
        elif choice == '3':
            take_quiz(cursor)
        elif choice == '4':
            view_scoreboard(cursor)
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")


def view_categories(cursor):
    try:
        cursor.execute("SELECT * FROM quiz_categories")
        categories = cursor.fetchall()
        if categories:
            table = [["ID", "Category Name"]]
            table.extend(categories)
            print("\nCategories:")
            print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))
        else:
            print("No categories found.")
    except Exception as e:
        print(f"Error retrieving categories: {e}")


def view_quizzes(cursor):
    category_id = input("Enter category ID to view quizzes: ")
    try:
        cursor.execute("SELECT * FROM quizzes WHERE category_id = %s", (category_id,))
        quizzes = cursor.fetchall()
        if quizzes:
            table = [["ID", "Quiz Name"]]
            table.extend(quizzes)
            print("\nQuizzes:")
            print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))
        else:
            print("No quizzes found in this category.")
    except Exception as e:
        print(f"Error retrieving quizzes: {e}")


def take_quiz(cursor):
    quiz_id = input("Enter quiz ID to start the quiz: ")
    # Validate if quiz exists
    cursor.execute("SELECT id FROM quizzes WHERE id = %s", (quiz_id,))
    quiz = cursor.fetchone()
    
    if quiz:
        start_time = time()
        print("Starting quiz...")

        # Fetch questions for the quiz
        cursor.execute("SELECT * FROM questions WHERE quiz_id = %s", (quiz_id,))
        questions = cursor.fetchall()
        
        if questions:
            score = 0
            for question in questions:
                print(f"\n{question[1]}")
                print(f"A. {question[2]}")
                print(f"B. {question[3]}")
                print(f"C. {question[4]}")
                print(f"D. {question[5]}")
                
                answer = input("Your answer (A/B/C/D): ").upper()
                if answer == question[7]:  # Check if the answer is correct
                    score += 1

            time_taken = time() - start_time
            print(f"\nQuiz Completed! Your score is {score}/{len(questions)}")
            print(f"Time taken: {time_taken:.2f} seconds")
            
            # Save score to scoreboard
            save_score_to_scoreboard(cursor, quiz_id, score)
        else:
            print("No questions found for this quiz.")
    else:
        print("Invalid quiz ID. Quiz not started.")


def save_score_to_scoreboard(cursor, quiz_id, score):
    # Assuming you have a scoreboard table where scores are stored
    # Add a function to save the candidate's score to the database.
    try:
        # For simplicity, assume candidate_id is a fixed value (replace with actual candidate logic)
        candidate_id = 1
        cursor.execute("INSERT INTO scoreboard (quiz_id, candidate_id, score) VALUES (%s, %s, %s)", 
                       (quiz_id, candidate_id, score))
        cursor.connection.commit()
        print("Your score has been recorded.")
    except Exception as e:
        print(f"Error saving score: {e}")


def view_scoreboard(cursor):
    quiz_id = input("Enter quiz ID to view scoreboard: ")
    try:
        cursor.execute("""
        SELECT u.username, s.score
        FROM scoreboard s
        INNER JOIN users u ON s.candidate_id = u.id
        WHERE s.quiz_id = %s
        ORDER BY s.score DESC
        """, (quiz_id,))
        scores = cursor.fetchall()
        
        if scores:
            table = [["Username", "Score"]]
            table.extend(scores)
            print("\nScoreboard:")
            print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))
        else:
            print("No scores found for this quiz.")
    except Exception as e:
        print(f"Error retrieving scoreboard: {e}")
