import datetime as dt
import os
import time
import win32com.client


# FUNCTIONS
def get_file_extension(src_file_path):
    """
    Returning file extension
    :param src_file_path: str - file path
    :return: str - the file extension
    """
    try:
        if len(os.path.splitext(src_file_path)[1]) != 0:
            return os.path.splitext(src_file_path)[1]

    except FileNotFoundError:
        print('File not found, please re-run')


def xl_file_to_csv(xl_file_file_path, sh_index):
    """
    Open a workbook, get the index of the worksheet (sh_index) and save sheet(s) as csv files
    :param xl_file_file_path: workbook path
    :param sh_index: index of the worksheet (0 - all worksheets)
    :return: generated csv file names
    """
    start_time = time.process_time()
    start_clock = time.perf_counter()

    xl_app = win32com.client.Dispatch("Excel.Application")
    xl_app.Visible = 0
    xl_app.DisplayAlerts = 0

    work_book = xl_app.Workbooks.Open(xl_file_file_path)

    if work_book.Worksheets.count >= sh_index:
        csv_file_list = list()
        if sh_index == 0:
            for sheet in work_book.Worksheets:
                work_sheet = sheet
                csv_file_list = save_csv_file(work_sheet, csv_file_list)
        else:
            work_sheet = work_book.Worksheets(sh_index)
            csv_file_list = save_csv_file(work_sheet, csv_file_list)

        work_book.Close(SaveChanges=0)
        xl_app.Quit()

        # Print runtime
        print('win32com process: {}'.format(time.process_time() - start_time))
        print('win32com counter: {}'.format(time.perf_counter() - start_clock))

        return csv_file_list
    else:
        print('There is not a tab in the workbook with index: {}'.format(sh_index))


def save_csv_file(work_sheet, file_name_list):
    """
    Saving a worksheet to a csv file and add the csv file name to a list, naming convention applied
    :param work_sheet: worksheet to save csv (type: win32com.client.CDispatch)
    :param file_name_list: list holding csv file names
    :return: list of csv file names
    """

    work_sheet_name = work_sheet.name
    output_csv_name = work_sheet_name + '_' + time_stamp_generator() + '.csv'
    work_sheet.SaveAs(os.path.join(os.getcwd(), output_csv_name), 6)
    file_name_list.append(output_csv_name)

    return file_name_list


def time_stamp_generator():
    """
    Generate a timestamp
    :return: a timestamp (str)
    """
    time_stamp = str(dt.datetime.now())
    time_stamp = time_stamp.replace(':', '_')
    time_stamp = time_stamp.replace(' ', '_')
    return time_stamp


# PROGRAM STARTS HERE
file_path = input('Please enter file path: ')
file_extension = get_file_extension(file_path)

if file_extension in [".xlsb", ".xlsx"]:
    try:
        sheet_index = int(input('Please enter the index number of a sheet to convert to .csv (0 - all sheets): '))
        src_csv = xl_file_to_csv(file_path, sheet_index)
        if src_csv is not None:
            print('')
            print('CSV file(s) created: ')
            print('-----------------------\n')
            print(*src_csv, sep="\n")
    except ValueError:
        print('Sheet index number must be an integer.')
else:
    print("Program can only process '.xlsb' or '.xlsx' files.")
