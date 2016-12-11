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
from datetime import datetime


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


def get_date():
    """
    Prompt employee for date in the format of MM/DD/YYYY. Check if valid entty.
    """
    date = input("Enter date of task in the format MM/DD/YYYY: ").strip()
    try:
        date = datetime.strptime(date, "%m/%d/%Y")
    except ValueError:
        print("\nNot a valid date entry! Enter the date in the format "
            "MM/DD/YYYY.\n")
        get_date()
    else:
        return date


def display_temp_entry(date, employee_name, task_name, minutes, notes):
    """Print task to user before writing to database."""
    clear_screen()
    print("Date: {}\nEmployee Name: {}\nTask Name: {}\nMinutes: {}\nNotes: {}"
        "".format(date, employee_name, task_name, minutes, notes))


def add_entry():
    """Add work entry to database."""
    clear_screen()
    date = get_date()
    employee_name = get_employee_name()
    task_name = get_task_name()
    minutes = get_time_spent()
    notes = get_notes()

    if (employee_name and task_name and minutes and date):
        display_temp_entry(date, employee_name, task_name, minutes, notes)
        if input("\nSave entry? [Y/n] ").lower().strip() != 'n':
            Entry.create(
                date=date,
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
    """Find a previous work log entry by date"""
    clear_screen()
    # Select distinct dates from all entries
    dates = get_all_distinct_dates_list()
    print("Search by Date\n")
    print("Here are the dates we have entries for: \n")
    for date in dates:
        print(convert_datetime_to_string(date))
    print("\n")
    user_input = get_date()

    # Find and display all entries.

    entries = Entry.select().where(Entry.date == user_input)

    if entries:
        display_entries(entries)
    else:
        print("\nNo matches found for {}!".format(user_input))
        response = input("\nDo you want to search something else? Y/[n] ")
        if response.lower().strip() != 'y':
            menu_loop()
        else:
            clear_screen()
            search_entries()


def get_all_distinct_dates_list():
    """Find a distinct dates in the databse. Returns a list of strings."""
    dates = []
    for entry in Entry.select().order_by(Entry.date.desc()):
        date = entry.date
        if date not in dates:
            dates.append(date)
    return dates


def convert_dates_string_to_datetime(entries):
    """
    Converts all dates from a list of entries from the database to datetime
    objects.
    """
    for entry in entries:
        entry.date = convert_string_to_datetime(entry.date)
        entry.save()
    return entries


def convert_datetime_to_string(date):
    """Converts a datetime object to a string."""
    date_string = date.strftime("%m/%d/%Y")
    return date_string


def convert_string_to_datetime(date):
    """Converts a string to a datetime object."""
    date_datetime = datetime.strptime(date, "%m/%d/%Y")
    return date_datetime


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


def display_entries(entries):
    """Displays entries to the screen."""
    index = 0

    while True:
        clear_screen()
        print_entries(index, entries)

        if len(entries) == 1:
            input("\nPress ENTER to continue to Main Menu.")
            menu_loop()

        display_nav_options(index, entries)

        user_input = input("\nSelect option from above: ").lower().strip()

        if index == 0 and user_input == 'n':
            index += 1
            clear_screen()
        elif index > 0 and index < len(entries) - 1 and user_input == 'n':
            index += 1
            clear_screen()
        elif index == len(entries) - 1 and user_input == 'p':
            index -= 1
            clear_screen()
        elif user_input == 'q':
            menu_loop()
        else:
            input("\n{} is not a valid command! Please try again."
                "".format(user_input))


def display_nav_options(index, entries):
    """Displays a menu that let's the user page through the entries."""
    p = "[P] - Previous entry"
    n = "[N] - Next entry"
    q = "[Q] - Return to Main Menu"
    menu = [p, n, q]

    if index == 0:
        menu.remove(p)
    elif index == len(entries) - 1:
        menu.remove(n)

    print("\n")
    for option in menu:
        print(option)


def print_entries(index, entries, display=True):
    """Print entries to screen."""
    if display:
        print("Showing {} of {} entry(s)".format(index + 1, len(entries)))

    print("\n" + "=" * 50 + "\n")
    print("Date: {}\nEmployee Name: {}\nTask Name: {}\nMinutes: {}\nNotes: {}"
        "".format(
            entries[index].date,
            entries[index].employee_name,
            entries[index].task_name,
            entries[index].minutes,
            entries[index].notes))


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
