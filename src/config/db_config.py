import mysql.connector
from mysql.connector import Error
from tabulate import tabulate

class DatabaseConfig:
    @staticmethod
    def get_connection():
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='quizdb',
                user='root',
                password='manish'
            )
            return connection
        except Error as e:
            print(f"Error connecting to MySQL Database: {e}")
            return None

    @staticmethod
    def init_database():
        connection = DatabaseConfig.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Create users table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        role ENUM('admin', 'candidate') NOT NULL
                    )
                """)

                # Create categories table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS quiz_categories (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        description TEXT
                    )
                """)

                # Create quizzes table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS quizzes (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        category_id INT,
                        title VARCHAR(200) NOT NULL,
                        description TEXT,
                        time_limit INT,
                        FOREIGN KEY (category_id) REFERENCES quiz_categories(id)
                    )
                """)

                # Create questions table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS questions (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        quiz_id INT,
                        question_text TEXT NOT NULL,
                        option_a TEXT NOT NULL,
                        option_b TEXT NOT NULL,
                        option_c TEXT NOT NULL,
                        option_d TEXT NOT NULL,
                        correct_answer CHAR(1) NOT NULL,
                        FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
                    )
                """)

                # Create quiz_results table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS quiz_results (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT,
                        quiz_id INT,
                        score INT,
                        time_taken INT,
                        date_taken DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id),
                        FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
                    )
                """)

                # Insert default admin user
                cursor.execute("""
                    INSERT IGNORE INTO users (username, password, role)
                    VALUES ('manish', '9234', 'admin')
                """)

                connection.commit()
                print("Database initialized successfully!")
            except Error as e:
                print(f"Error initializing database: {e}")
            finally:
                cursor.close()
                connection.close()