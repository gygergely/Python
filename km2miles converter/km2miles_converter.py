def welcome():
    """
    Simple welcome message to the user.
    :return: None
    """
    print('Welcome my friend, \nThis is unit converter helping you to convert kms to miles or miles to kms.\n')


def goodbye():
    """
    Simple goodbye message to the user.
    :return: None
    """
    print('Thank you for using our software. Hope to see you again soon')


def conversion_type_selection():
    """
    Asking for conversion type
    :return: m2k - miles to kilometers OR k2m - kilometers to miles
    """
    while True:
        conversion_type = input('To convert miles to kms enter: m2k, to convert kms to miles enter: k2m: ')
        if conversion_type == 'm2k' or conversion_type == 'k2m':
            return conversion_type
        else:
            print('Invalid selection.\n')
            continue


def get_value_to_convert():
    """
    User input value to convert
    :return: float
    """
    while True:
        try:
            user_input = float(input('Please enter the value to convert: '))
            return user_input
        except (TypeError, ValueError):
            print('Hmm... something went wrong or entered an invalid value.\n')
            continue


def km_convert_to_miles(user_input):
    """
    Convert a km value to miles
    :param user_input: value to convert
    :return: converted value
    """
    return user_input * 0.621371


def mile_convert_to_km(user_input):
    """
   Convert a mile value to kilometers
   :param user_input: value to convert
   :return: converted value
   """
    return user_input * 1.60934


def print_result(value, conversion_type):
    """
    Print converted value, text depending on the conversion type
    :param value: converted value
    :param conversion_type: type of conversion
    :return: None
    """
    if conversion_type == 'm2k':
        print('{} miles is exactly {} km.\n'.format(value, mile_convert_to_km(value)))
    elif conversion_type == 'k2m':
        print('{} km is exactly {} miles.\n'.format(value, km_convert_to_miles(value)))


def main_program():
    """
    Main program, asking conversion type from the user, value to convert, print the result. Repeat while user enters Y
    :return: None
    """
    user_choice_to_do_another_conversion = "Y"

    while user_choice_to_do_another_conversion.upper() == "Y":
        conversion_type = conversion_type_selection()
        value_to_convert = get_value_to_convert()
        print_result(value_to_convert, conversion_type)
        user_choice_to_do_another_conversion = input('Would you like to do another conversion? (Y/N): ')
        print('')


# PROGRAM STARTS HERE
# -------------------
welcome()

main_program()

goodbye()
