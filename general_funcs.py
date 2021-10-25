from os import path, getcwd, chdir


def getVar(var_file_loc: str):
    # getting opening and reading the file
    with open(var_file_loc, 'r') as write:
        vars_ = write.readlines()
    # getting the amount of lines to skip
    # getting the 0th (first) line . getting rid of \n . splitting the number in two at the ': '
    split_amnt = vars_[0].rstrip().split(': ')
    lines_skipped = int(split_amnt[1])
    # getting rid of "\n"
    for k in range(0, len(vars_)):
        temp = vars_[k].rstrip()
        # running through the lines that are considered commented to get to the varibales
        if k > lines_skipped - 1:
            # splitting the line at the ": " to get the amount of lines to skip
            temp = temp.split(': ')
            vars_[k] = temp[1]
        else:
            vars_[k] = temp
    return vars_[lines_skipped:]


def gotoTracking():
    current_dir = getcwd().split('\\', -1)[-1]
    print(f'Current Directory: {current_dir}')

    if current_dir != 'TRACKING':
        # changing working directory to work within the tracking folder
        path_parent = path.dirname(getcwd())
        chdir(path_parent)
        print(f'Changed Directory: {getcwd()}\n')
        gotoTracking()
    elif 'TRACKING' == current_dir:
        print(f'In Master Directory: {getcwd()}\n'
              f'        (Should be TRACKING) Fin')
        return
    else:
        print(f'ERROR, UNPREDICTABLE BEHAVIOUR\n'
              f'{current_dir}')
        return

