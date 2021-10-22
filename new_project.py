import os

from shutil import copyfile
from openpyxl import load_workbook


up_dir_num = 2

# changing working directory to work within the tracking folder
for i in range(0, up_dir_num):
    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)
print("Changed Directory to -->" + str(os.getcwd()))

# xlsx templates to copy
xlsx_template_loc = r'Projects\Template\Template.xlsx'
packingslip_template_loc = r'Projects\Template\_PACKING_SLIP.xlsx'

# getting project number
project = input("What is the new Project Number, dawg?: ")

# project folder locations
folder_path = r'Projects\\' + project
project_pathxlsx = folder_path + r'\\' + project + '.xlsx'
packingslip_pathxlsx = folder_path + r'\\' + project + '_PACKING_SLIP.xlsx'
src_folder = folder_path + '\\src'
purchase_folder = folder_path + '\\Purchase_Scans'

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

# copying the file
copyfile(packingslip_template_loc, packingslip_pathxlsx)
print("Made {}_PACKING_SLIP".format(project))

# making source file
os.mkdir(src_folder)
print("Made {} src Folder".format(project))

# making Invoce scan folder
os.mkdir(purchase_folder)
print("Made {} Purchase_Scans Folder".format(project))

input("All finished my dude.\nHope I did my job well.\nPress Enter to continue...")



