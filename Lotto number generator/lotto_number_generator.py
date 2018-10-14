from random import randint


def welcome():
    """
    Simple welcome message
    """
    print()
    print('Welcome and thank you for using this amazing Hungarian random lottery number generator')


def lottery_types():
    """
    List of lottery types
    """
    print()
    print('1 - 5s\n2 - 6s\n3 - Scandinavian\n4 - Euro Jackpot\n5 - Exit\n0 - Help')
    print()


def generate_random_number(upper_limit):
    """
    Generate a random number between 1 and upper limit -1
    :param upper_limit: upper limit of the number range
    :return: generated random number
    """
    return randint(1, upper_limit)


def is_number_in_a_list(src_list, number):
    """
    Check if a number is in a list or not
    :param src_list: source list
    :param number: number to check
    :return: True if number is in the list, False if not
    """
    return number in src_list


def add_lottery_number_to_list(src_list, number):
    """
    Add a number to a list
    :param src_list: list to expand
    :param number: number to add
    :return: list with the extra number
    """
    return src_list.append(number)


def generate_lotto_numbers_list(numbers_required, upper_limit):
    """
    Generate a fixed length list with random numbers
    :param numbers_required: items count in the list
    :param upper_limit: max of the list items
    :return: a list with numbers_required nr of elements
    """
    lotto_numbers_list = list()

    while len(lotto_numbers_list) < numbers_required:
        random_number = generate_random_number(upper_limit)
        if not is_number_in_a_list(lotto_numbers_list, random_number):
            add_lottery_number_to_list(lotto_numbers_list, random_number)

    return lotto_numbers_list


def main():
    """
    Lotto number generator, random number of list is generated based on the lottery type
    :return: list of unique random numbers
    """
    while True:
        try:
            selected_lottery_type = int(input('Please select a lottery type (1-4): '))

            if selected_lottery_type == 1:
                upper_limit = 91
                numbers_required = 5
                lotto_type = '5s'
            elif selected_lottery_type == 2:
                upper_limit = 46
                numbers_required = 6
                lotto_type = '6s'
            elif selected_lottery_type == 3:
                upper_limit = 36
                numbers_required = 7
                lotto_type = 'Scandinavian'
            elif selected_lottery_type == 4:
                upper_limit = 51
                numbers_required = 5
                upper_limit_extra = 11
                numbers_required_extra = 2
                lotto_type = 'Euro Jackpot'
            elif selected_lottery_type == 5:
                break
            elif selected_lottery_type == 0:
                lottery_types()
                continue

            if 1 <= selected_lottery_type < 5:
                lotto_numbers = generate_lotto_numbers_list(numbers_required, upper_limit)
                lotto_numbers.sort()

                if selected_lottery_type == 4:
                    lotto_numbers_extra = generate_lotto_numbers_list(numbers_required_extra, upper_limit_extra)
                    lotto_numbers_extra.sort()
                    print('Your lucky numbers for {} lottery are: {}'.format(lotto_type, str(lotto_numbers +
                                                                                             lotto_numbers_extra)))
                else:
                    print('Your lucky numbers for {} lottery are: {}'.format(lotto_type, str(lotto_numbers)))

                break
        except TypeError:
            print('Invalid input. Please try again.')


# MAIN PROGRAM STARTS HERE
# ------------------------
welcome()
lottery_types()

while True:
    main()
    rerun = input('Would you like to re-run? (y/n): ')
    if rerun.upper() == 'N':
        break
