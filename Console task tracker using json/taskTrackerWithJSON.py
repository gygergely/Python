import json
import os.path


# Simple text print functions
# ---------------------------

def welcome():
    """
    Simple welcome message
    """
    print('Welcome to the Python task tracker')


def list_options():
    """
    Listing options in the program
    """
    print()
    print('The following options are available: \n1 - Add new task\n2 - List tasks\n3 - Delete/Remove task\n'
          '4 - Change status\n5 - Exit')

# Task tracker open, update, exists functions
# --------------------------------------------


def update_task_tracker_json_file(task_list, filename):
    """
    Update the json file
    :param task_list: task list
    :param filename: json filename
    """
    with open(filename, 'w') as taskTracker:
        json.dump(task_list, taskTracker)


def is_json_file_exists(filename):
    """
    Check if a file exists
    :param filename: file name to check in this program a json file
    :return: True if exists, False if does not
    """
    return os.path.isfile(filename)


def open_task_tracker_file_read(filename):
    """
    Open a json file and assign it contents to a variable
    :param filename: json file name to open
    :return: a variable with the json file content
    """
    with open(filename, 'r') as json_file:
        task_list = json.load(json_file)
    return task_list


# Options functions
# -----------------

def add_new_task():
    """
    Asking task description and status from the user
    :return: the task description and status or None if invalid values were entered
    """
    new_task_description = input('Please enter a short description of the task: ')
    if len(new_task_description) > 0:
        while True:
            try:
                task_complete_status = int(input('Please enter the status of the task (1 - completed / '
                                                 '0 - not completed: '))
                if task_complete_status > 1 or task_complete_status < 0:
                    print('Invalid entry, use only 1 or 0. Try again')
                    continue
                return new_task_description, task_complete_status
            except (ValueError, TypeError):
                print('Invalid input. Select between 1 and 0')
                continue
    else:
        print('No description has been specified, task is not registered')
        return None, None


def task_status_enum(status):
    """
    Status enumeration, user can only enter 1 or 0
    :param status: user input
    :return: 1 - Completed / 0 - Not completed
    """
    if status == 1:
        return 'Completed'
    else:
        return 'Not Completed'


def register_new_task(task_description, status, filename):
    """
    Update the json file with a new task
    :param task_description: user input - short description
    :param status: user input (1 - Completed / 0 - Not completed)
    :param filename: json file name to update
    """
    status = task_status_enum(status)

    file_exists = is_json_file_exists(filename)

    if file_exists:

        content = open_task_tracker_file_read(filename)

        task_id = len(content)

        new_task = {
            "TaskID": task_id + 1,
            "Description": task_description,
            "Status": status
        }

        content.append(new_task)
        update_task_tracker_json_file(content, filename)

    else:
        new_task = [
            {
                "TaskID": 1,
                "Description": task_description,
                "Status": status
            }
        ]
        update_task_tracker_json_file(new_task, filename)


def task_list_filter(task_list):
    """
    Filter the task based on user selection
    :param task_list: task list
    """
    print('   Please select what tasks you would like to see:\n1 - All\n2 - Completed\n3 - Not Completed')

    while True:
        try:
            user_choice = int(input('List type: '))
            if user_choice == 1:
                filter_criteria = 'None'
            elif user_choice == 2:
                filter_criteria = 'Completed'
            elif user_choice == 3:
                filter_criteria = 'Not Completed'
            else:
                filter_criteria = 'None'

            print_filtered_list(task_list, filter_criteria)
            break

        except (ValueError, TypeError):
            print('Ups. Seems you selection is invalid. Please try again.')


def print_filtered_list(task_list, criteria):
    """
    Print the filtered task list to console
    :param task_list: task list
    :param criteria: user input: None or Completed or Not Completed
    """
    if criteria == 'None':
        for item in task_list:
            print()
            print(item)

    else:
        filtered_list = filter(lambda x: x['Status'] == criteria, task_list)
        for item in filtered_list:
            print()
            print(item)


def remove_task(task_list, item):
    """
    Remove the given item from the task list
    :param task_list: task list
    :param item: task ID
    :return: task list without the deleted item
    """
    del task_list[item - 1]
    return task_list


def renumber_task(task_list):
    """
    Renumbering the task IDs after an item is deleted from the list
    :param task_list: task list
    :return: task list with renumbered task IDs
    """
    renumbering = 1
    for item in task_list:
        item['TaskID'] = renumbering
        renumbering += 1

    return task_list


def select_task_to_delete(task_list):
    """
    User selects the task to delete
    :param task_list: task list
    :return: task list without the deleted item and with renumbered task IDs
    """
    if len(task_list) > 0:
        while True:
            try:
                task_selector = int(input('Please select a task to remove (between 1 and {} ): '
                                          .format(len(task_list))))
                if 1 <= task_selector <= len(task_list):
                    print('The selected task:\n')
                    print(task_list[task_selector - 1])
                    confirm = input('Would you like to delete the task (y/n): ')
                    if confirm.upper() == 'Y':
                        task_list = remove_task(task_list, task_selector)
                        task_list = renumber_task(task_list)
                        print('Task {} is deleted.'.format(task_selector))
                        return task_list
                    else:
                        print('Funny... Nothing happened. Try again')
                        return None
                else:
                    print('Invalid selection')
                    continue
            except TypeError:
                print('Invalid selection. Try again')
                continue
    else:
        print('No task in the list')
        return None


def update_task_status(task_list, item):
    """
    Update the status of a task, if it is completed changes to not completed and vice versa
    :param task_list: task list
    :param item: user input task ID of the task
    :return: task list with the updated status
    """
    status = task_list[item - 1]['Status']

    if status == 'Completed':
        task_list[item - 1]['Status'] = 'Not Completed'
    else:
        task_list[item - 1]['Status'] = 'Completed'

    return task_list


def select_task_to_update_status(task_list):
    """
    User selects the task for status update
    :param task_list: task list
    :return: task list with updated status or none if invalid input was entered
    """
    if len(task_list) > 0:
        while True:
            try:
                task_selector = int(input('Please select a task to update (between 1 and {} ): '
                                          .format(len(task_list))))
                if 1 <= task_selector <= len(task_list):
                    print('The selected task:\n')
                    print(task_list[task_selector - 1])
                    confirm = input('Would you like to change the status the task (y/n): ')
                    if confirm.upper() == 'Y':
                        task_list = update_task_status(task_list, task_selector)
                        print('Task {} status is updated.'.format(task_selector))
                        return task_list
                    else:
                        print('Funny... Nothing happened. Try again')
                        return None
                else:
                    print('Invalid selection')
                    continue
            except TypeError:
                print('Invalid selection. Try again')
                continue
    else:
        print('No task in the list')
        return None


def main_program():
    """
    Task list program with several options
    """
    list_options()

    while True:
        try:
            print()
            user_selected_option = int(input('Please select from the above options (1-5 / 0 - for help): '))
            filename = 'taskTracker.json'

            if user_selected_option == 1:

                new_task_description, task_complete_status = add_new_task()

                if new_task_description is None or task_complete_status is None:
                    print('No new task registered')
                    continue
                else:
                    register_new_task(new_task_description, task_complete_status, filename)

            elif user_selected_option == 2 or user_selected_option == 3 or user_selected_option == 4:

                file_exists = is_json_file_exists(filename)

                if file_exists:
                    task_list = open_task_tracker_file_read(filename)

                    if user_selected_option == 2:
                        task_list_filter(task_list)

                    elif user_selected_option == 3 or user_selected_option == 4:
                        if user_selected_option == 3:
                            task_list = select_task_to_delete(task_list)

                        elif user_selected_option == 4:
                            task_list = select_task_to_update_status(task_list)

                        if task_list is not None:
                            update_task_tracker_json_file(task_list, filename)
                else:
                    print('Task tracker file not found.')
                    continue

            elif user_selected_option == 5:
                break

            elif user_selected_option == 0:
                list_options()

            else:
                print('Invalid selection. Try again.')
                continue

        except TypeError:
            print('Invalid input. Please select an available option')
            continue


# MAIN PROGRAM STARTS HERE

welcome()
main_program()
