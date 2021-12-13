from os import getcwd, path, chdir




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



general_file_loc = []
purchase_order_vars = []
new_proj_loc_var = []


def GoToTracking():
    current_dir = getcwd().split('\\', -1)[-1]
    print(f'<{__name__}> Current Directory: {current_dir}')
    if 'TRACKING' == current_dir:
        # print(f'In Master Directory: {getcwd()}\n'
        #       f'        (Should be TRACKING)')
        return
    elif current_dir != 'TRACKING':
        # changing working directory to work within the tracking folder
        path_parent = path.dirname(getcwd())
        chdir(path_parent)
        print(f'<{__name__}> Changed Directory: {getcwd()}\n')
        GoToTracking()

    else:
        print(f'<{__name__}> ERROR, UNPREDICTABLE BEHAVIOUR\n'
              f'{current_dir}')
        return

GoToTracking()

general_file_loc = GetVar(var_file_loc="Python_Source\\!variables\\file_locations.txt", edit_q=False)
purchase_order_vars = GetVar('Python_Source\\!variables\\purchase_input_var.txt', edit_q=False)
new_proj_loc_var = GetVar('Python_Source\\!variables\\new_project_var.txt', edit_q=False)

