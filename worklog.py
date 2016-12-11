"""
Author: Brian Weber
Date Created: December 11, 2016
Revision: 1.0
Title: Work Log with a Database
Description: The CSV timesheets were a huge success but some more features are
needed, including the ability for other developers to use the data without
worrying about file locking or availability. The managers have also asked for
a way to view time entries for each employee. Seems like a database would be a
better solution than a CSV file!

Create a command line application that will allow employees to enter their
name, time worked, task worked on, and general notes about the task into a
database. There should be a way to add a new entry, list all entries for a
particular employee, and list all entries that match a date or search term.
Print a report of this information to the screen, including the date, title of
task, time spent, employee, and general notes.
"""
from entry import Entry, initialize

import os, sys
from collections import OrderedDict


def clear_screen():
    """Clear the screen in the command prompt."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_employee_name():
    """Prompt the employee for their name."""
    employee_name = input("Enter your name: ")
    if len(employee_name) == 0:
        print("\nYou must enter your name!\n")
        get_employee_name()
    else:
        return employee_name


def get_task_name():
    """Prompt the employee for the task name."""
    task_name = input("Enter a task name: ")
    if len(task_name) == 0:
        print("\nYou must enter a task name!\n")
        get_task_name()
    else:
        return task_name


def get_time_spent():
    """Prompt the employee for the time spent on their task."""
    minutes = input("Enter number of minutes spent working on the task: ")
    try:
        int(minutes)
    except ValueError:
        print("\nNot a valid time entry! Enter time as a whole integer.\n")
        get_time_spent()
    else:
        return minutes


def get_notes():
    """Prompt employee to provide any additional notes."""
    notes = input("Notes for this task (ENTER if None): ")
    return notes


def add_entry():
    """Add work entry to database."""
    clear_screen()
    employee_name = get_employee_name()
    task_name = get_task_name()
    minutes = get_time_spent()
    notes = get_notes()

    if (employee_name and task_name and minutes):
        if input("\nSave entry? [Y/n] ").lower().strip() != 'n':
            Entry.create(
                employee_name=employee_name,
                task_name=task_name,
                minutes=minutes,
                notes=notes
            )
            print("\nEntry saved successfully!\n")
            input("Press any key to return to the main menu...")


def find_by_employee():
    """Find a previous work log entry by an employee's name."""
    pass


def find_by_date():
    """Find a previous work log entry by a date"""
    pass


def find_by_keyword():
    """Find a previous work log entry by a search term"""
    pass


def search_entries():
    """Lookup previous work entries"""
    choice = None

    while True:
        clear_screen()
        print("Search Menu\n")
        for key, value in search_menu.items():
            print("{}) {}".format(key, value.__doc__))
        choice = input("\nEnter a choice: ").lower().strip()

        if choice in search_menu:
            clear_screen()
            search_menu[choice]()


def quit_program():
    """Exit the work log program."""
    print("Thank you for using Work Log 4.0!")
    sys.exit()


def menu_loop():
    """Return to Main Menu"""
    choice = None

    while True:
        clear_screen()
        print("Main Menu\n")
        for key, value in main_menu.items():
            print("{}) {}".format(key, value.__doc__))
        choice = input("\nEnter a choice: ").lower().strip()

        if choice in main_menu:
            clear_screen()
            main_menu[choice]()


main_menu = OrderedDict([
    ('a', add_entry),
    ('s', search_entries),
    ('q', quit_program),
])


search_menu = OrderedDict([
    ('e', find_by_employee),
    ('d', find_by_date),
    ('k', find_by_keyword),
    ('q', menu_loop)
])


if __name__ == '__main__':
    initialize()
    clear_screen()
    input("Welcome to Work Log 4.0! Press any key to continue...")
    menu_loop()
