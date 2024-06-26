from general_funcs import *

from tkinter import messagebox
from os import listdir, remove, path, mkdir
from pandas import read_excel, DataFrame, ExcelWriter
from datetime import datetime
from shutil import copyfile
from csv import writer


# random edit


class IGS_Generate_Update_Logs:
    """Handles logging file management and Packing Slip creation"""
    def __init__(self, proj, shipping_loc, qtys: list, itms: list):
        super().__init__()
        current_dir = getcwd().split('\\', -1)[-1]
        if current_dir != 'TRACKING':
            GoToTracking()
        self.igs_vars = GetVar('Python_Source\!variables\igs_tracking_var.txt', False)
        self.excel_back_up = self.igs_vars[0]
        self.inventory_loc = self.igs_vars[2]

        # location of IGS inventory tracking
        self.shipping_loca = shipping_loc
        # project number that it is for
        self.project = proj
        # indexes of the items chosen

        self.items = itms
        # self.part_numbers = prt_nums ---- prt_nums: list,
        self.quantitties = qtys
        self._i = len(self.items)

        self.description, self.part_num, self.igs_inv, self.dws_inv = LoadData(self.inventory_loc)

        self.indexes = [self.description.index(item) for item in self.items]

        # self.CheckPreviousSlips()
        # self.CheckandUpdate()

    def CheckPreviousSlips(self):
        pass

    def CheckandUpdate(self):
        """Will check IGS and DWS inventories to make sure what action to take and if it is alright."""

        if path.exists('Customers\\IGS\\Inventory\\~$IGS_Inventory_Tracking.xlsx'):
            messagebox.showwarning(
                title='Please Close File',
                message='Please close the IGS_Inventory_Tracking.xlsx file before continuing.'
            )
            return True

        comment_lst = []

        # cycling through the indexes of items chosen to get condition
        for i, given_chosen_index in enumerate(self.indexes):
            # getting a given line's quntities: amount asked, amount igs has amount dws has
            amount_shipping = int(self.quantitties[i])
            igs_amnt = self.igs_inv[given_chosen_index]
            dws_amnt = self.dws_inv[given_chosen_index]
            product = self.description[given_chosen_index]

            approved, checked_message, changed_amnts = self.check_inventory(amount_shipping, igs_amnt, dws_amnt, product)

            # if the changes are approved from the check_inventory func then it will amend the current numbers
            if approved:
                self.igs_inv[given_chosen_index] = changed_amnts[0]
                self.dws_inv[given_chosen_index] = changed_amnts[1]

                comment_lst.append(checked_message)

            if not approved:
                messagebox.showinfo(title='', message='No information has been changed or edited\n'
                                                      'Press "Okay" to continue')
            if approved is None:
                return

        self.Update_Excel_Backup()

        self.UpdateLogs(comment_lst)

        self.Generate_Packing_Slip()

    def check_inventory(self, a_s, i_a, d_a, prod):
        """Checks the inventories of IGS and DWS. It outputs a string message declaring what will be done with the
        current amount in both inventories."""
        a = ''
        b = ''

        # if igs has nothing in their inventory
        if i_a == "":
            a = f'>IGS has no inventory for ct. {a_s}: \n' \
                f'>> {prod} \n' \
                f'>They currently have {i_a}. They are {a_s} over.\n'

        # if igs has some inventory, but not enough to complete the order
        elif i_a < a_s:
            # the amount in igs inventory is subtracted from the amount being sent
            a_s = a_s - i_a
            a = f'>IGS does not have enough inventory for {a_s + i_a}:\n' \
                f'  >> {prod}\n' \
                f'>They currently have {i_a}. They are {a_s} over.\n'
            i_a = 0

            # since igs did not have enough, it is checking it against how much we have in our inventory
            # if we do not have enough in our inventory, calculating how much we need to build
            if d_a < a_s:
                need_to_build = a_s - d_a
                b = f'>We do not have enough in our inventory either.\n' \
                    f'>We will need to build {need_to_build} more for this job.\n' \
                    f'>We have {d_a} currently in our inventory.'
                d_a = 0

            # if we do have enough in our inventory and igs does not
            else:
                a = a + f'\n>We will need to use {a_s} of our own inventory.\n'
                b = f'>We have {d_a} currently in our inventory.\n'
                d_a = d_a - a_s

        # if igs has enough in their inventory
        else:
            i_a = i_a - a_s

        # summary comment after figuring out what needs to be taken out of who's inventory
        c = f'\n>After completing this order for: \n' \
            f'    >>>{a_s}ct. {prod}\n' \
            f'  >>IGS will have: {i_a}\n' \
            f'  >>DWS will have: {d_a}'

        output_message = a + b + c

        title = f'Add {a_s}ct. {prod} to Slip?'
        print(f'{title}\n{output_message}')
        approve = messagebox.askyesnocancel(title=title, message=output_message)

        changed_nums = [i_a, d_a]

        return approve, output_message, changed_nums


    def Update_Excel_Backup(self):
        import_df = DataFrame(
            {
                'Description': self.description,
                'IGS Part Num': self.part_num,
                'IGS Inventory': self.igs_inv,
                'DWS Inventory': self.dws_inv
            }
        )

        current_date_time = datetime.now()
        date_slip = current_date_time.strftime("%m%d%Y-%H%M")

        new_backup_loc = f'{self.excel_back_up}\\{date_slip}-BeforeProject_{self.project}.xlsx'

        # making backup before making changed
        copyfile(self.inventory_loc, new_backup_loc)

        # inputting new part changes
        with ExcelWriter(self.inventory_loc, mode='w') as writer:
            import_df.to_excel(writer, sheet_name='IGS_DWS_INVENTORY', index=False)

        # getting list of backups in the backup folder
        # 'Customers\IGS\Inventory\Backups'
        file_lst = listdir(path=self.excel_back_up)
        # getting rid of the log folder
        file_lst.pop(file_lst.index('LOG'))

        # creating list of the backups to check for the oldest out of 11 and deleting the oldest to get 10
        full_path = [self.excel_back_up + '\\' + str(x) for x in file_lst]

        # checking the length for more than 10 and deleting it
        if len(file_lst) > int(self.igs_vars[1]):
            oldest = min(full_path, key=path.getctime)
            remove(oldest)


    def UpdateLogs(self, comment_list):
        log_folder = f'{self.excel_back_up}\\LOG'
        now = datetime.now()
        date_time = now.strftime('%m/%d/%Y - %H:%M:%S')
        year = now.year
        month = now.strftime('%B')

        date_dir = f'{log_folder}\\{year}'

        if not path.isdir(date_dir):
            print(f'Made {year} log folder')
            mkdir(date_dir)

        month_csv_path = f'{date_dir}\\{month}.csv'
        if not path.isfile(month_csv_path):
            a = True
        else:
            a = False

        with open(month_csv_path, 'a+', newline='') as write_obj:
            csv_writer = writer(write_obj)

            if a:
                first_line = ['Comment', 'Date\\Time']
                csv_writer.writerow(first_line)

            for row in comment_list:
                output_row = [row, date_time]

                csv_writer.writerow(output_row)

    def Generate_Packing_Slip(self):
        packing_slip_loc = f'Projects\\{self.project}\\D2-7-{self.project} - Packing Slip.xlsx'

        AddDataToExcel(
            excel_loc=packing_slip_loc,
            sheet_name='INPUT',
            col_loc=[2, 3, 4],
            row_list_data=[self.shipping_loca, self.quantitties, self.items],
            place_loc=(0, 0),
            scan_min=(0, 0),
            scan_max=(20, 5)
        )

        now = datetime.now()
        year = now.year

        general_year_ps_loc = f"Finance\\Yearly_Packing_Slips\\{year}"
        ps_year_loc = f"{general_year_ps_loc}\\D2-7-{self.project} - Packing Slip.xlsx"

        if not path.isdir(general_year_ps_loc):
            mkdir(general_year_ps_loc)

            copyfile(packing_slip_loc, ps_year_loc)


def LoadData(inventory_loc):
    """Loads the information from the IGS inventory file"""
    # Gettting the info from the file
    inv_data = read_excel(inventory_loc)
    # print(inv_data)

    description = inv_data['Description'].values.tolist()
    part_num = inv_data['IGS Part Num'].values.tolist()
    igs_inv = inv_data['IGS Inventory'].values.tolist()
    dws_inv = inv_data['DWS Inventory'].values.tolist()

    return [description, part_num, igs_inv, dws_inv]
