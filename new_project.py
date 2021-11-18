import os

from shutil import copyfile
from openpyxl import load_workbook
from tkinter import messagebox
from datetime import datetime

from pandas import ExcelWriter, DataFrame

from general_funcs import *



def CreateNewProject(shop_q=False):
    # make sure that it is in the proper master directory
    GoToTracking()
    # getting variables
    file_loc_var = GetVar('Python_Source\\!variables\\new_project_var.txt', False)
    d2_loc = GetVar('Python_Source\\!variables\\Quality_Control_Files\\QC-D2-Locations.txt', False)

    tracking_stats_loc = 'Python_source\\!working_files\\dws_tracking_vals.txt'
    tracking_stats_all = GetVar(tracking_stats_loc, True)
    tracking_comment_line = tracking_stats_all[0]
    tracking_stats = tracking_stats_all[1]
    tracking_alllines = tracking_stats_all[-1]

    print(file_loc_var)
    print(tracking_stats)

    # xlsx templates to copy
    # Python_Source\!working_files\Template.xlsx
    xlsx_template_loc = file_loc_var[0]
    text_stats_temp_loc = file_loc_var[1]
    # Quality_Control\\!D - Documents\\D2 - Documentation\\D2-7.0 - Packing Slip.xlsx
    packingslip_template_loc = d2_loc[6]


    # getting amount of previously created projects
    projects_t_date = tracking_stats[0]

    # getting the month of the previous project creation to automatically start the count from 0 in the next year
    prev_proj_mont = tracking_stats[1]

    # getting date info
    now_is_time = datetime.now()
    date_string = now_is_time.strftime('%m%y')
    month_int = now_is_time.strftime('%m')
    print(f'Month: {month_int}')
    if month_int == '01' and prev_proj_mont == '12':
        projects_t_date = '01'

    new_project_num = date_string + projects_t_date

    title = f'New Project w/{new_project_num}?'
    message = f'Do you want "{new_project_num}" to be the Project Number?\n\n' \
              f'Press "Yes" to Continue\n' \
              f'Press "Cancel" to cancel'

    yes = messagebox.askokcancel(title=title, message=message)

    # print(f'Yes: {yes}')

    if yes is None:
        return

    elif not shop_q:
        new_num = int(projects_t_date) + 1
        with open(tracking_stats_loc, 'w') as file:
            tracking_alllines[0+int(tracking_comment_line)] = f'0Projects Created This Year: {new_num:02d}\n'
            tracking_alllines[1+int(tracking_comment_line)] = f'1Month of Last Create Project: {month_int}\n'
            file.writelines(tracking_alllines)
        if yes:
            project = new_project_num
        elif not yes:
            # could add "put your own number in" func with it checking all current projects to make sure no dupe
            return

        # project folder locations
        folder_path = f'Projects\\{project}'
        project_pathxlsx = f'{folder_path}\\{project}-master.xlsx'
        packingslip_pathxlsx = f'{folder_path}\\D2-7.0-{project} - Packing Slip.xlsx'
        src_folder = f'{folder_path}\\!src'
        purchase_folder = f'{folder_path}\\Purchase_Scans'
        certs_folder = f'{folder_path}\\Material_Cert_Scans'
        general_scans = f'{folder_path}\\General_Scans'

    else:
        year = now_is_time.year

        # project folder locations
        folder_path = f'Shop\\{year}'
        project_pathxlsx = f'{folder_path}\\{year}-master.xlsx'
        src_folder = f'{folder_path}\\!src'
        purchase_folder = f'{folder_path}\\Purchase_Scans'
        certs_folder = f'{folder_path}\\Material_Cert_Scans'
        general_scans = f'{folder_path}\\General_Scans'

        project = year

    if path.isdir(folder_path):
        warning_message = f'Error Creating Project: {project}\n' \
                          f'Project {folder_path} already exists\n' \
                          f'Try again, dumbo...smh'
        messagebox.showwarning(title='Cannot Create Project', message=warning_message)
        return

    # making new project folder
    os.mkdir(folder_path)

    # copying the file
    copyfile(xlsx_template_loc, project_pathxlsx)
    print('Creating {}.xlsx @ {}, yo'.format(project, project_pathxlsx))

    # opening workbook
    ss = load_workbook(project_pathxlsx)

    # new names of sheets
    sheet_name_lst = [
        project + "_dataSheet",
        project + "_purchases",
        project + "_financing"
    ]

    j = 0

    sheet_lst = ss.sheetnames
    # print("List of Template Sheets: {}".format(sheet_lst))
    # renaming the sheets
    for sheet in sheet_lst:
        # print("Sheet Renaming Cycle: {}. Should be {}.".format(i + 1, len(sheet_lst)))
        # declaring what sheet to rename
        ss_sheet = ss[sheet]
        # creating default sheet name variable
        sheet_name = sheet_name_lst[j]
        # renaming sheet
        ss_sheet.title = sheet_name
        j += 1
    print('Sheets Renamed')
    # saving sheet
    ss.save(project_pathxlsx)

    # # copying the file
    # copyfile(packingslip_template_loc, packingslip_pathxlsx)
    # print(f"Made {project} Packing Slip Folder")
    # AddDataToExcel(
    #     excel_loc=packingslip_pathxlsx,
    #     sheet_name='INPUT',
    #     col_loc=[1],
    #     row_list_data=[str(project)],
    #     place_loc=(0, 0),
    #     scan_max=(2, 2)
    # )

    # making source file
    os.mkdir(src_folder)
    print(f"Made {project} src Folder")

    # making the project stats file to check if packing slips or certain purchases have been made
    stats_text_loc = f'{src_folder}\\stats.txt'
    copyfile(text_stats_temp_loc, stats_text_loc)
    print(f"Made {project} Stats File")

    # making general/other scan folder
    os.mkdir(general_scans)
    print(f"Made {project} General_Scans Folder")

    # making purchase scan folder
    os.mkdir(purchase_folder)
    print(f"Made {project} Purchase_Scans Folder")

    # making cert scan folder
    os.mkdir(certs_folder)
    print(f"Made {project} Material_Cert_Scans Folder")

    return project
