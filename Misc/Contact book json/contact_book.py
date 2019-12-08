import os.path
import json


# CONTACT CLASS
# ---------------------------

class Contact(object):
    def __init__(self, first_name, last_name, email, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_email_and_phone(self):
        return '{} / {}'.format(self.email, self.phone)

    def print_full_contact_details(self):
        print('First name: {}\nLast name: {}\nEmail: {}\nPhone: {}'.format(self.first_name, self.last_name, self.email,
                                                                           self.phone))


# SIMPLE PRINT FUNCTIONS
# --------------------------

def welcome():
    """
    Simple welcome message
    """
    print('Welcome to the Contact List application')


def print_option_list():
    """
    Print out user options
    """
    print()
    print('Please choose one the following options:\n1 - List all contacts\n2 - Add new contact\n3 - Edit a contact\n'
          '4 - Delete a contact\n5 - Exit program\n0 - Help')
    print()


# FILE FUNCTIONS
# --------------------------

def is_json_file_exists(filename):
    """
    Check if a file exists
    :param filename: file name to check in this program a json file
    :return: True if exists, False if does not
    """
    return os.path.isfile(filename)


def open_contact_file_read(filename):
    """
    Open a json file and assign it contents to a variable
    :param filename: json file name to open
    :return: a variable with the json file content
    """
    with open(filename, 'r') as json_file:
        contact_list = json.load(json_file)
    return contact_list


def load_existing_contacts(filename):
    """
    Load existing contacts from json file to a list
    :param filename: source file name
    :return: a list
    """
    contact_list = list()
    if is_json_file_exists(filename):
        contact_src = open_contact_file_read(filename)
        if len(contact_src) > 0:
            for contact in contact_src:
                existing_contact = Contact(first_name=contact['First Name'], last_name=contact['Last Name'],
                                           email=contact['Email'], phone=contact['Phone'])
                contact_list.append(existing_contact)
    return contact_list


def update_json_file(input_list, filename):
    """
    Update the json file
    :param input_list: list to write to the json file
    :param filename: json filename
    """
    with open(filename, 'w') as json_file:
        json.dump(input_list, json_file)


def save_changes(contact_list, filename):
    """
    Save changes in a json file / always called at exit
    :param contact_list: source contact list
    :param filename: json file name
    """
    contact_list_to_write = list()
    if len(contact_list) > 0:
        for person in contact_list:
            contact_to_file = {
                'First Name': person.first_name,
                'Last Name': person.last_name,
                'Email': person.email,
                'Phone': person.phone
            }
            contact_list_to_write.append(contact_to_file)
    update_json_file(contact_list_to_write, filename)


# USER OPTION FUNCTIONS
# ---------------------------
def list_all_contacts(contact_list):
    """
    List every contact from a contact list
    :param contact_list: source contact list
    """
    if len(contact_list) > 0:
        for index, person in enumerate(contact_list, 1):
            print('ID: ' + str(index))
            print(person.get_full_name())
            print(person.get_email_and_phone())
            print('-' * 20)
    else:
        print('Nobody listed in the contact list file.')


def add_new_contact(contact_list):
    """
    Add new contact to a contact list
    :param contact_list: source contact list
    """
    first_name = input("Please enter contact's first name: ")
    last_name = input("Please enter contact's last name: ")
    email = input("Please enter contact's email address: ")
    phone = input("Please enter contact's phone number: ")

    new_contact = Contact(first_name=first_name, last_name=last_name, email=email, phone=phone)
    contact_list.append(new_contact)
    print('')
    print('New contact: {} added to your contact list'.format(new_contact.get_full_name()))


def edit_contact(contact_list):
    """
    Edit a contact detail in the contact book
    :param contact_list: source contact list
    """
    if len(contact_list) > 0:
        print('Select the number of the contact you would like to edit:')

        for index, person in enumerate(contact_list, 1):
            print(str(index) + ') ' + person.get_full_name())

        print('')
        selected_id_str = input('What contact would you like to edit? (enter ID number): ')

        try:
            selected_id = int(selected_id_str) - 1

            if 0 <= selected_id <= len(contact_list) - 1:
                selected_contact = contact_list[int(selected_id)]

                detail_to_edit = int(input('Which details would you like to edit?\n1 - First name\n2 - Last name\n'
                                           '3 - Email\n4 - Phone\n5 - Exit\n\nPlease select: '))

                if 1 <= detail_to_edit <= 5:
                    if detail_to_edit == 1:
                        new_first_name = input('Please enter a new first name: ')
                        selected_contact.first_name = new_first_name
                        change_type = 'First name'
                    elif detail_to_edit == 2:
                        new_last_name = input('Please enter a new last name: ')
                        selected_contact.last_name = new_last_name
                        change_type = 'Last name'
                    elif detail_to_edit == 3:
                        new_email = input('Please enter a new email: ')
                        selected_contact.email = new_email
                        change_type = 'Email'
                    elif detail_to_edit == 4:
                        new_phone = input('Please enter a new phone: ')
                        selected_contact.phone = new_phone
                        change_type = 'Phone'

                    print('')
                    print('{} is changed.'.format(change_type))
                else:
                    print('Invalid selection. Try again.')
            else:
                print('Invalid ID selection')

        except TypeError:
            print('Invalid input')
    else:
        print('There is nobody in your contact list. So sad... Add some contacts :). Using option 2.')


def delete_contact(contact_list):
    """
    Deleting a contact from the contact list
    :param contact_list: source contact list
    """
    if len(contact_list) > 0:
        print('Select the number of the contact you would like to delete:')

        for index, person in enumerate(contact_list, 1):
            print(str(index) + ") " + person.get_full_name())

        selected_id_str = input('What contact would you like to delete? (enter ID number): ')

        try:
            selected_id = int(selected_id_str) - 1
            if 0 <= selected_id <= len(contact_list) - 1:
                selected_contact = contact_list[int(selected_id)]
                contact_list.remove(selected_contact)
                print('Contact was successfully removed from your contact list.')
            else:
                print('Invalid selection.')

        except TypeError:
            print('Invalid input. Try again.')
    else:
        print('There is nobody in your contact list. So sad... Add some contacts :). Using option 2.')


# MAIN FUNCTION
# ----------------------------

def main():
    """
    Contact book program collect and edit contact details and store them in a json file
    """

    filename = 'contact_book.json'
    contact_list = load_existing_contacts(filename)

    print_option_list()

    while True:
        try:
            user_option = int(input('Please select an option (1-5 / 0 - for help): '))

            if user_option == 1:
                list_all_contacts(contact_list)
                continue
            elif user_option == 2:
                add_new_contact(contact_list)
                continue
            elif user_option == 3:
                edit_contact(contact_list)
                continue
            elif user_option == 4:
                delete_contact(contact_list)
                continue
            elif user_option == 5:
                save_changes(contact_list, filename)
                break
            elif user_option == 0:
                print_option_list()
                continue
            else:
                print('Invalid selection. Try again.')
                continue

        except TypeError:
            print('Invalid input. Please select an available option')
            continue


# MAIN PROGRAM STARTS HERE
welcome()
main()
