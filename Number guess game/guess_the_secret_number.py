from random import randint


def welcome():
    """
    Simple welcome message to the user.
    :return: None
    """
    print('Welcome to Secret Number Guessing Game.\n'
          'I will think of a secret number between 1 and an upper limit defined by you.If no upper limit defined, \n'
          'default is 10.\nTry to figure out the number.\nIf you like you can use help, '
          'though you can try without it.\nGood luck. You have 10 guesses.\n')


def generate_secret_number(entered_number):
    """
    Generating a 'random' number, upper limit defined by user, default is 11.
    :param entered_number:
    :return:
    """
    return randint(1, entered_number)


def asking_user_for_upper_limit():
    """
    Input for the upper limit, if invalid entry return 11, else the entered limit.
    :return: 11 in case of invalid entry, entered number otherwise
    """
    try:
        upper_limit = int(input('Please enter an upper limit: '))
        if upper_limit <= 1:
            print('Invalid entry, upper limit must be greater than 1. Default limit applied')
            return 11
        else:
            return upper_limit
    except (TypeError, ValueError):
        print('Invalid entry. Default upper limit applied')
        return 11


def user_help_on():
    """
    User decision to use help or not.
    :return: bool value, True - help will be provided, False - not
    """
    help_needed = input('Would you like to have help in the guessing? (Y/N): ')

    if help_needed.upper() == "Y":
        return True
    else:
        return False


def main_guessing(secret_nr, guess_help):
    """
    Main program asking user for guesses, if help is turned on gives a hint if the guess is greater than or less then
    the secret number. When reaching guess number 5 automatic hint if the secret number is odd or even
    :param secret_nr: random generated secret number
    :param guess_help: bool help on or off
    :return:
    """
    user_guess = 0

    user_tries = 0

    while user_guess != secret_nr:

        try:
            user_guess = int(input('Please enter your guess: '))
        except (TypeError, ValueError):
            user_guess = 0
            print('Oh wrong format?!')
            continue

        if user_guess == secret_nr:
            print('Awesome, really the secret number was {}'.format(secret_number))
        elif guess_help:
            if user_guess > secret_nr:
                print('Your guess is {} which is greater than the secret number'.format(user_guess))
            else:
                print('Your guess is {} which is less than the secret number'.format(user_guess))

        user_tries += 1

        if user_tries == 10:
            print('You reached the maximum number of guesses')
            print('The secret number is {}'.format(secret_number))
            break
        elif user_tries == 5:
            print(
                'Ok you are far away let me give you a hint. Let\'s see if the secret number is even : {}'.format(
                    is_number_even(secret_number)))


def is_number_even(number):
    """
    Check if a number is even or odd
    :param number: number to check
    :return: True if the number is even, false if it is odd
    """
    return number % 2 == 0


# MAIN PROGRAM
# ----------------------------------------------

welcome()

user_upper_limit = asking_user_for_upper_limit()

secret_number = generate_secret_number(user_upper_limit)

show_help = user_help_on()

# Help during test, show the secret number
# print(str(secret_number))

main_guessing(secret_number, show_help)
