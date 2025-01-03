import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from helper.__init__ import ConsoleHelper
from services.__init__ import UserService, CategoryService, QuizService, QuestionService, QuizResultService
from models.__init__ import User, Category, Quiz, Question, QuizResult
from services.database_service import DatabaseService

class QuizApp:
    def __init__(self):
        self.main_menu_options = [
            "Admin Login",
            "Candidate Login",
            "Candidate Registration",
            "Exit"
        ]

    def start(self):
        while True:
            ConsoleHelper.print_header("Quiz Management System")
            choice = ConsoleHelper.get_menu_choice(self.main_menu_options)
            
            if choice == 1:
                self.admin_login()
            elif choice == 2:
                self.candidate_login()
            elif choice == 3:
                self.candidate_registration()
            else:
                print("\nThank you for using the Quiz Management System!")
                break


    def reset_database(self):
        """Reset the entire database after confirmation."""
        ConsoleHelper.print_header("Reset Database")
        print("WARNING: This will delete ALL data from the database!")
        print("This includes all users, categories, quizzes, questions, and results.")
        print("This action cannot be undone!")
        
        if ConsoleHelper.confirm_action("\nAre you absolutely sure you want to reset the database? (y/n): "):
            if DatabaseService.reset_database():
                print("\nDatabase reset successfully!")
            else:
                print("\nFailed to reset database. Please try again.")
        else:
            print("\nDatabase reset cancelled.")
        
        ConsoleHelper.pause()



    def admin_login(self):
        ConsoleHelper.print_header("Admin Login")
        # print("Default admin credentials - Username: admin, Password: admin123")
        username = ConsoleHelper.get_input("Username: ")
        password = ConsoleHelper.get_input("Password: ")
        
        user = UserService.authenticate(username, password, 'admin')
        if user:
            self.current_user = user
            self.admin_dashboard()
        else:
            print("Invalid credentials!")
            ConsoleHelper.pause()

    def admin_dashboard(self):
        while True:
            ConsoleHelper.print_header(f"Admin Dashboard - Welcome {self.current_user.username}")
            choice = ConsoleHelper.get_menu_choice([
                "Manage Categories",
                "Manage Quizzes",
                "Manage Questions",
                "View Candidates",
                "Reset Database ( ! )",
                "Logout"
            ])

            if choice == 1:
                self.manage_categories()
            elif choice == 2:
                self.manage_quizzes()
            elif choice == 3:
                self.manage_questions()
            elif choice == 4:
                self.view_candidates()
            elif choice == 5:
                self.reset_database()
            else:
                self.current_user = None
                break

    def manage_categories(self):
        while True:
            ConsoleHelper.print_header("Manage Categories")
            choice = ConsoleHelper.get_menu_choice([
                "Add Category",
                "View Categories",
                "Back"
            ])

            if choice == 1:
                name = ConsoleHelper.get_input("Category Name: ")
                description = ConsoleHelper.get_input("Description: ")
                if CategoryService.create(name, description):
                    print("Category added successfully!")
                else:
                    print("Failed to add category.")
                ConsoleHelper.pause()
            elif choice == 2:
                self.view_categories()
            else:
                break

    def view_categories(self):
        ConsoleHelper.print_header("Categories")
        categories = CategoryService.get_all()
        if not categories:
            print("No categories found.")
        else:
            # Convert categories to table format
            headers = ['ID', 'Name', 'Description']
            data = [[cat.id, cat.name, cat.description] for cat in categories]
            ConsoleHelper.display_table(headers, data, "Available Categories")
        ConsoleHelper.pause()    

    def manage_quizzes(self):
        while True:
            ConsoleHelper.print_header("Manage Quizzes")
            choice = ConsoleHelper.get_menu_choice([
                "Add Quiz",
                "View Quizzes",
                "Back"
            ])

            if choice == 1:
                self.add_quiz()
            elif choice == 2:
                self.view_quizzes()
            else:
                break

    def add_quiz(self):
        categories = CategoryService.get_all()
        if not categories:
            print("No categories available. Please create a category first.")
            ConsoleHelper.pause()
            return

        print("\nAvailable Categories:")
        for category in categories:
            print(f"{category.id}: {category.name}")

        try:
            category_id = int(ConsoleHelper.get_input("Enter Category ID: "))
            title = ConsoleHelper.get_input("Quiz Title: ")
            description = ConsoleHelper.get_input("Description: ")
            time_limit = int(ConsoleHelper.get_input("Time Limit (in minutes): "))

            quiz = Quiz(None, category_id, title, description, time_limit)
            if QuizService.create(quiz):
                print("Quiz added successfully!")
            else:
                print("Failed to add quiz.")
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
        ConsoleHelper.pause()

    def view_quizzes(self):
        categories = CategoryService.get_all()
        if not categories:
            print("No categories found.")
            ConsoleHelper.pause()
            return

        # Display categories in table format
        headers = ['ID', 'Name']
        data = [[cat.id, cat.name] for cat in categories]
        ConsoleHelper.display_table(headers, data, "Select a category to view quizzes:")

        try:
            category_id = int(ConsoleHelper.get_input("Enter Category ID: "))
            quizzes = QuizService.get_by_category(category_id)
        
            if not quizzes:
                print("No quizzes found in this category.")
            else:
                # Display quizzes in table format
                headers = ['ID', 'Title', 'Description', 'Time Limit']
                data = [[q.id, q.title, q.description, f"{q.time_limit} minutes"] for q in quizzes]
                ConsoleHelper.display_table(headers, data, "Available Quizzes")
        except ValueError:
            print("Invalid input. Please enter a valid category ID.")
        ConsoleHelper.pause()

    def manage_questions(self):
        while True:
            ConsoleHelper.print_header("Manage Questions")
            choice = ConsoleHelper.get_menu_choice([
                "Add Question",
                "View Questions",
                "Back"
            ])

            if choice == 1:
                self.add_question()
            elif choice == 2:
                self.view_questions()
            else:
                break

    def add_question(self):
        # First select a quiz
        categories = CategoryService.get_all()
        if not categories:
            print("No categories available.")
            ConsoleHelper.pause()
            return

        print("\nSelect a category:")
        for category in categories:
            print(f"{category.id}: {category.name}")

        try:
            category_id = int(ConsoleHelper.get_input("Enter Category ID: "))
            quizzes = QuizService.get_by_category(category_id)
            
            if not quizzes:
                print("No quizzes found in this category.")
                ConsoleHelper.pause()
                return

            print("\nSelect a quiz:")
            for quiz in quizzes:
                print(f"{quiz.id}: {quiz.title}")

            quiz_id = int(ConsoleHelper.get_input("Enter Quiz ID: "))
            question_text = ConsoleHelper.get_input("Question Text: ")
            option_a = ConsoleHelper.get_input("Option A: ")
            option_b = ConsoleHelper.get_input("Option B: ")
            option_c = ConsoleHelper.get_input("Option C: ")
            option_d = ConsoleHelper.get_input("Option D: ")
            correct_answer = ConsoleHelper.get_input("Correct Answer (A/B/C/D): ").upper()

            if correct_answer not in ['A', 'B', 'C', 'D']:
                print("Invalid correct answer. Must be A, B, C, or D.")
                ConsoleHelper.pause()
                return

            question = Question(None, quiz_id, question_text, option_a, option_b, 
                              option_c, option_d, correct_answer)
            
            if QuestionService.add_question(question):
                print("Question added successfully!")
            else:
                print("Failed to add question.")
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
        ConsoleHelper.pause()

    def view_questions(self):
        categories = CategoryService.get_all()
        if not categories:
            print("No categories available.")
            ConsoleHelper.pause()
            return

        # Display categories in table format
        headers = ['ID', 'Name']
        data = [[cat.id, cat.name] for cat in categories]
        ConsoleHelper.display_table(headers, data, "Select a category:")

        try:
            category_id = int(ConsoleHelper.get_input("Enter Category ID: "))
            quizzes = QuizService.get_by_category(category_id)
        
            if not quizzes:
                print("No quizzes found in this category.")
                ConsoleHelper.pause()
                return

            # Display quizzes in table format
            headers = ['ID', 'Title']
            data = [[q.id, q.title] for q in quizzes]
            ConsoleHelper.display_table(headers, data, "Select a quiz:")

            quiz_id = int(ConsoleHelper.get_input("Enter Quiz ID: "))
            questions = QuestionService.get_quiz_questions(quiz_id)
        
            if not questions:
                print("No questions found in this quiz.")
            else:
                for i, question in enumerate(questions, 1):
                    print(f"\nQuestion {i}:")
                    # Display question in table format
                    headers = ['Options', 'Text']
                    data = [
                        ['Question', question.question_text],
                        ['A', question.option_a],
                        ['B', question.option_b],
                        ['C', question.option_c],
                        ['D', question.option_d],
                        ['Correct', question.correct_answer]
                    ]
                    ConsoleHelper.display_table(headers, data)
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
        ConsoleHelper.pause()

    def view_candidates(self):
        ConsoleHelper.print_header("View Candidates")
        candidates = UserService.get_all_candidates()
        if not candidates:
            print("No candidates found.")
        else:
            # Display candidates in table format
            headers = ['Username', 'Role']
            data = [[c.username, c.role] for c in candidates]
            ConsoleHelper.display_table(headers, data, "Registered Candidates")
        ConsoleHelper.pause()

    def candidate_registration(self):
        ConsoleHelper.print_header("Candidate Registration")
        username = ConsoleHelper.get_input("Choose username: ")
        password = ConsoleHelper.get_input("Choose password: ")
        
        if UserService.register(username, password, 'candidate'):
            print("Registration successful!")
        else:
            print("Registration failed. Username might be taken.")
        ConsoleHelper.pause()

    def candidate_login(self):
        ConsoleHelper.print_header("Candidate Login")
        username = ConsoleHelper.get_input("Username: ")
        password = ConsoleHelper.get_input("Password: ")
        
        user = UserService.authenticate(username, password, 'candidate')
        if user:
            self.current_user = user
            self.candidate_dashboard()
        else:
            print("Invalid credentials!")
            ConsoleHelper.pause()

    def candidate_dashboard(self):
        while True:
            ConsoleHelper.print_header(f"Candidate Dashboard - Welcome {self.current_user.username}")
            choice = ConsoleHelper.get_menu_choice([
                "Take Quiz",
                "View Scoreboard",
                "Logout"
            ])
            if choice == 1:
                self.take_quiz()
            elif choice == 2:
                self.view_scoreboard()
            else:
                self.current_user = None
                break

    def take_quiz(self):
        # First select a quiz
        categories = CategoryService.get_all()
        if not categories:
            print("No categories available.")
            ConsoleHelper.pause()
            return

        print("\nSelect a category:")
        for category in categories:
            print(f"{category.id}: {category.name}")

        try:
            category_id = int(ConsoleHelper.get_input("Enter Category ID: "))
            quizzes = QuizService.get_by_category(category_id)
            
            if not quizzes:
                print("No quizzes found in this category.")
                ConsoleHelper.pause()
                return

            print("\nSelect a quiz:")
            for quiz in quizzes:
                print(f"{quiz.id}: {quiz.title}")

            quiz_id = int(ConsoleHelper.get_input("Enter Quiz ID: "))
            questions = QuestionService.get_quiz_questions(quiz_id)
            
            if not questions:
                print("No questions found in this quiz.")
                ConsoleHelper.pause()
                return

            score = 0
            total_questions = len(questions)

            for i, question in enumerate(questions, 1):
                ConsoleHelper.print_header(f"Question {i}/{total_questions}")
                print(f"\n{question.question_text}")
                print(f"A) {question.option_a}")
                print(f"B) {question.option_b}")
                print(f"C) {question.option_c}")
                print(f"D) {question.option_d}")

                answer = ConsoleHelper.get_input("Your answer (A/B/C/D): ").upper()
                if answer == question.correct_answer:
                    score += 1

            # Calculate percentage
            percentage = (score / total_questions) * 100
            print(f"\nQuiz completed!")
            print(f"Your score: {score}/{total_questions} ({percentage:.2f}%)")

            # Save result
            result = QuizResult(None, self.current_user.id, quiz_id, score, 0, None)
            if QuizResultService.save_result(result):
                print("Result saved successfully!")
            else:
                print("Failed to save result.")

        except ValueError:
            print("Invalid input. Please enter valid numbers.")
        ConsoleHelper.pause()

    def view_scoreboard(self):
        categories = CategoryService.get_all()
        if not categories:
            print("No categories available.")
            ConsoleHelper.pause()
            return

        # Display categories in table format
        headers = ['ID', 'Name']
        data = [[cat.id, cat.name] for cat in categories]
        ConsoleHelper.display_table(headers, data, "Select a category:")

        try:
            category_id = int(ConsoleHelper.get_input("Enter Category ID: "))
            quizzes = QuizService.get_by_category(category_id)
        
            if not quizzes:
                print("No quizzes found in this category.")
                ConsoleHelper.pause()
                return

            # Display quizzes in table format
            headers = ['ID', 'Title']
            data = [[q.id, q.title] for q in quizzes]
            ConsoleHelper.display_table(headers, data, "Select a quiz:")

            quiz_id = int(ConsoleHelper.get_input("Enter Quiz ID: "))
            results = QuizResultService.get_scoreboard(quiz_id)
        
            if not results:
                print("No results found for this quiz.")
            else:
                # Display scoreboard in table format
                headers = ['Username', 'Score', 'Time Taken', 'Date']
                data = [[r['username'], r['score'], f"{r['time_taken']}s", r['date_taken']] 
                   for r in results]
                ConsoleHelper.display_table(headers, data, "Scoreboard")
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
        ConsoleHelper.pause()