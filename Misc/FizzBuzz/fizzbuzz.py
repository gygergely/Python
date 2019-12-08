def welcome():
    """
    Simple welcome message to the user.
    :return: None
    """
    print('Welcome to the \'fizzbuzz\' game')


def user_number_input():
    """
    Request a number from the user.
    :return: int
    """
    while True:
        try:
            nr = int(input('Please enter a number between 1 and 100: '))
            if nr < 1 or nr > 100:
                print('Range must be between 1 and 100')
                continue
            else:
                return nr
        except (TypeError, ValueError):
            print('Ups something went wrong')
            continue


def get_fizzbuzz(number):
    """
    In case the number is divisible with 3, it prints "fizz" instead of the number. If the number is divisible with 5,
    it prints "buzz". If it's divisible with both 3 and 5, it prints "fizzbuzz".
    :param number: end of number loop
    :return: None
    """
    for nr in range(1, number + 1):
        if nr % 5 == 0 and nr % 3 == 0:
            print('fizzbuzz')
        elif nr % 5 == 0:
            print('buzz')
        elif nr % 3 == 0:
            print('fizz')
        else:
            print(nr)


# PROGRAM STARTS HERE
# -------------------
welcome()
get_fizzbuzz(user_number_input())
