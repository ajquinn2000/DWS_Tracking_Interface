from os import path, getcwd, chdir


from appending_funcs import append_df_to_excel


from pandas import read_excel, read_csv


def GetVar(var_file_loc: str, edit_q):
    working_output = []
    # getting opening and reading the file
    with open(var_file_loc, 'r') as write:
        vars_ = write.readlines()
        # print(vars_)
    # getting the amount of lines to skip
    # getting the 0th (first) line . getting rid of \n . splitting the number in two at the ': '
    split_amnt = vars_[0].rstrip().split(': ')
    lines_skipped = int(split_amnt[1])

    # print(f'Length of var_ {len(vars_)}')
    # print(f'{len(vars_)}, {lines_skipped}\n{vars_}')
    if len(vars_) != lines_skipped:
        for k in range(0, len(vars_)):
            # running through the lines that are considered commented to get to the varibales
            if k > lines_skipped - 1:
                # getting rid of "\n"l
                temp = vars_[k].rstrip()
                # splitting the line at the ": " to get the amount of lines to skip

                temp = temp.split(': ')
                working_output.append(temp[1])
    else:
        working_output = []

    if edit_q:
        returner = (lines_skipped, working_output, vars_)

    elif not edit_q:
        returner = working_output

    else:
        returner = None

    return returner


def GoToTracking():
    current_dir = getcwd().split('\\', -1)[-1]
    print(f'Current Directory: {current_dir}')
    if 'TRACKING' == current_dir:
        # print(f'In Master Directory: {getcwd()}\n'
        #       f'        (Should be TRACKING)')
        return
    elif current_dir != 'TRACKING':
        # changing working directory to work within the tracking folder
        path_parent = path.dirname(getcwd())
        chdir(path_parent)
        print(f'Changed Directory: {getcwd()}\n')
        GoToTracking()

    else:
        print(f'ERROR, UNPREDICTABLE BEHAVIOUR\n'
              f'{current_dir}')
        return


def AddDataToExcel(
        excel_loc: str,
        sheet_name: str,
        # what column names am I appending the data i am giving to
        col_loc: list,
        row_list_data: list,
        scan_min: tuple,
        scan_max: tuple,
        place_loc: tuple,
):

    GoToTracking()
    # reads the info from the excel to get the column names
    df = read_excel(excel_loc, sheet_name=sheet_name)

    column_list = df.columns.tolist()
    print(f'Columns extracted: \n{column_list}')
    col_name_loc = [column_list[i] for i in col_loc]

    for column_name, row_list in zip(col_name_loc, row_list_data):
        if type(row_list) != list:
            df.loc[0, column_name] = row_list
        else:
            for i, row in enumerate(row_list):
                df.loc[i, column_name] = row

    append_df_to_excel(
        excel_loc,
        df=df,
        sheet_name=sheet_name,
        # where the top left corner will be when dumping the df
        startrow=place_loc[0],
        startcol=place_loc[1],
        # -----
        # smallest index of SOURCE worksheet (for copy func)
        copy_min_row=scan_min[0],
        copy_min_col=scan_min[1],
        # largest index of SOURCE worksheet (for copy func)
        max_row=scan_max[0],
        max_col=scan_max[1],
        # -----

        index=False,
    )
    # print(f'Sending to: {excel_loc}\n{df}')


def IncrementGivenStat(
        stat_file: str,
        stat_str: str,
        increment: int,
        comment_lines: int,
        working_vars: list,
        var_vars: list
):
    # getting the names from the text file that have ': ' to check
    # if a given stat var exists yet
    var_vars_concat = var_vars[comment_lines:]
    var_names = [element.split(': ')[0] for element in var_vars_concat]

    # checking to see if a given stat name is in the var_names
    if stat_str in var_names:
        # finding at which location in the var names
        var_index = var_names.index(stat_str)
        # adding given increment to that specific stat index
        new_inc = str(int(working_vars[var_index]) + increment)
        # combining the newly incremented stat back into var list
        # so that it can be saved to the text file
        var_vars[var_index + comment_lines] = f'{stat_str}: {new_inc}\n'
    else:
        # if the stat does not exist yet, get len, since 0 will put in
        # first line if there are no elements

        # adding given increment to that specific stat index
        new_inc = increment
        # combining the newly incremented stat back into var list
        # so that it can be saved to the text file
        # print(f'Befor\n{var_vars}')
        last_in_lst = var_vars[-1]
        # print(f'lBefor {last_in_lst}')
        if not '\n' in last_in_lst:
            var_vars[-1] = f'{var_vars[-1]}\n'
            # print(f'afta {last_in_lst}')
        var_vars.append(f'{stat_str}: {increment}\n')
        # print(f'After\n{var_vars}')

    with open(stat_file, 'w') as file:
        file.writelines(var_vars)

    return new_inc


def LoadVendors(col_count=7):
    """Gets the first n [col_count](base-0) columns of the vendor sheet"""
    file_locs_data = GetVar('Python_Source\\!variables\\file_locations.txt', False)
    df = read_csv(file_locs_data[6], encoding='ISO-8859-1')

    vendor_col_name = [
        'Company Name',
        'Short Company Name',
        'Description',
        'Contactor',
        'Location',
        'Phone Number',
        'Email',
        'Additional Emails',
        'Paint',
        'Hydraulics',
        'Pneumatic Stuffs',
        'Coatings',
        'Hardware',
        'IT',
        'Electronics',
        'Steel Broker',
        'Piping',
        'Gaskets',
        'Non-ferrous',
        'Solenoids'
    ]

    vendor_list = []

    for i in range(col_count):
        vendor_list.append(df[vendor_col_name[i]].tolist())

    return vendor_list


def CheckIfOpen(file):
    pass
