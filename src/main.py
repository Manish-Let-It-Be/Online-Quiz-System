# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

from config.db_config import ConnectToDb

if __name__ == "__main__":
    db_object=ConnectToDb()
    db_object.create_connection()