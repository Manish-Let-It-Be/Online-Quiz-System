import os
import time
from typing import List, Optional
from tabulate import tabulate

class ConsoleHelper:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def print_header(title: str):
        ConsoleHelper.clear_screen()
        print("=" * 50)
        print(f"{title:^50}")
        print("=" * 50)
        print()

    @staticmethod
    def get_menu_choice(options: List[str]) -> int:
        while True:
            print("\nPlease select an option:")
            menu_items = [[i, option] for i, option in enumerate(options, 1)]
            print(tabulate(menu_items, headers=['CHOICE', 'OPTION'], tablefmt='grid'))
            try:
                choice = int(input("\nEnter your choice (1-{}): ".format(len(options))))
                if 1 <= choice <= len(options):
                    return choice
                print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    @staticmethod
    def display_table(headers: List[str], data: List[List], title: str = None):
        if title:
            print(f"\n{title}")
        print(tabulate(data, headers=headers, tablefmt='grid'))

    @staticmethod
    def get_input(prompt: str, required: bool = True) -> Optional[str]:
        while True:
            value = input(prompt).strip()
            if value or not required:
                return value
            print("This field is required. Please try again.")

    @staticmethod
    def confirm_action(prompt: str = "Are you sure? (y/n): ") -> bool:
        return input(prompt).lower().startswith('y')

    @staticmethod
    def pause(message: str = "Press Enter to continue..."):
        input(message)

class QuizTimer:
    def __init__(self, time_limit: int):
        self.time_limit = time_limit
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()

    def get_time_taken(self) -> int:
        if self.start_time and self.end_time:
            return int(self.end_time - self.start_time)
        return 0

    def is_time_up(self) -> bool:
        if not self.start_time or not self.time_limit:
            return False
        return (time.time() - self.start_time) >= self.time_limit