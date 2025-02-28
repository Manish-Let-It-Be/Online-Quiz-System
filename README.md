# Quiz On CLI
- Mentor : [Mr. Jeet Kumar](https://github.com/jeetjha11)

Quiz On CLI is a command-line interface application that allows users to take quizzes, manage categories, quizzes, and questions, and view their scores. This project is designed for both administrators and candidates, providing a user-friendly experience for managing quizzes.

## Features
- **Admin Login**: Admins can manage categories, quizzes, and questions.
- **Candidate Registration**: Candidates can register and log in to take quizzes.
- **Quiz Management**: Admins can create, view, and manage quizzes and their associated questions.
- **Scoreboard**: Candidates can view their scores after completing quizzes.
- **Time Limits**: Quizzes have time limits, and scores are calculated based on performance.

## Libraries Used
- `mysql.connector`: For MySQL database connections.
- `tabulate`: For displaying tables in the CLI.
- `typing`: For type hints and annotations.
- `datetime`: For handling date and time.
- `dataclass`: For creating data classes.

## Screenshots

### Main Menu
![Main Menu](visuals/MainMenu.jpg)

### Admin Dashboard
![Admin](visuals/AdminDash.jpg)

### Candidate Dashboard
![Candidate](visuals/CandidateDash.jpg)

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Manish-Let-It-Be/Quiz-On-CLI.git
   cd Quiz-On-CLI
   ```

2. **Install Dependencies**
   Make sure you have `pip` installed, then run:
   ```bash
   pip install mysql-connector-python tabulate
   ```

## Usage

1. **Run the Application**
   ```bash
   python main.py
   ```

2. **Navigate the Menu**
- Admin Login
- Candidate Login
- Candidate Registration
- Exit

3. **Admin Dashboard**
- Manage Categories
- Manage Quizzes
- Manage Questions
- View Candidates
- Reset Database (!)
- Logout

4. **Candidate Dashboard**
- Take Quiz
- View Scoreboard
- Logout
  

## Database Initialization
The database will be automatically initialized when you run the application for the first time. It will create the necessary tables and insert default admin credentials.

<!--
[View on Eraser![](https://app.eraser.io/workspace/pHxhnZoGxiOtSZp0ke2k/preview?elements=CPituBc6SslSNolUcePKLA&type=embed)](https://app.eraser.io/workspace/pHxhnZoGxiOtSZp0ke2k?elements=CPituBc6SslSNolUcePKLA)
-->

## Flow Chart
<p align="center">
  <img src="https://app.eraser.io/workspace/pHxhnZoGxiOtSZp0ke2k/preview?elements=CPituBc6SslSNolUcePKLA&type=embed">
</p>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&color=39FF14&center=true&width=435&lines=Thank+You+For+Checking+!">
</p>
