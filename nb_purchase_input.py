from tkinter import StringVar, messagebox, N, W, E, S
from tkinter.ttk import Frame, Label, Entry, Button, LabelFrame, Combobox

from datetime import datetime
from shutil import copyfile
from os import path, mkdir
from csv import writer
from pandas import read_csv

from globalz import purchase_order_vars
from appending_funcs import append_df_to_excel
from general_funcs import GetVar, AddDataToExcel, IncrementGivenStat, LoadVendors, XLCheckIfOpen, CSVCheckIfOpen
from new_project import CreateNewProject

global vendor_list


class PurchaseInputPage(Frame):

    def __init__(self, master=None, from_project=False, top_level=None):
        Frame.__init__(self, master)
        self.grid()
        self.top_level = top_level

        # purchase_order_vars = GetVar('Python_Source\\!variables\\purchase_input_var.txt', False)
        self.payment_options = purchase_order_vars[0].split(',')
        #  (self.payment_options)
        self.purchase_order_loc = purchase_order_vars[1]
        self.purchase_order_short = purchase_order_vars[2]

        self.entry_width = 23

        self.parent_flabel_pad = (5, 5)

        self.date_now = self.GetCurrentDate(seconds=False)

        # Quote Specific Frame stuffs -----
        self.quote_spec_frame = LabelFrame(
            self,
            text='Quote Info',
            padding=self.parent_flabel_pad
        )
        self.quote_spec_frame.grid(row=0, rowspan=3, column=0)

        self.date_var = StringVar()
        self.expected_del_var = StringVar()
        self.quote_id_var = StringVar()
        self.short_descript_var = StringVar()
        self.charged_to_var = StringVar()
        self.estimated_del_var = StringVar()
        self.vendor_name_var = StringVar()
        self.shrt_vendor_var = StringVar()
        self.shrt_vendor_var.set('')
        self.vendor_contact_var = StringVar()
        self.vendor_number_var = StringVar()
        self.vendor_email_var = StringVar()
        self.vendor_loc_var = StringVar()

        # if the class is called without a projuct number being supplied to it
        self.proj_var = StringVar()
        if not from_project:
            project_num_frame = LabelFrame(
                self.quote_spec_frame,
                text='Project Number',
                padding=self.parent_flabel_pad
            )
            project_num_frame.grid(row=2, column=1, sticky=N+W)

            proj_entry = Combobox(
                project_num_frame,
                textvariable=self.proj_var,
                width=self.entry_width,
                values="Shop"
            )
            proj_entry.grid()
            proj_entry.bind("<Key>", lambda key: self.UpdateFNP(key))
            proj_entry.bind("<<ComboboxSelected>>", self.UpdateFNP)

        else:
            self.proj_var.set(from_project)


        # Vendor Specific Frame stuffs -----
        self.vendor_frame = LabelFrame(
            self,
            text='Vendor Information',
            padding=self.parent_flabel_pad
        )
        self.vendor_frame.grid(row=4, column=0, rowspan=2, sticky=W+E)

        short_name_lframe = LabelFrame(
            self.vendor_frame,
            text='Short Vendor Name',
            padding=self.parent_flabel_pad
        )
        short_name_lframe.grid(row=3, column=1)

        self.short_name_entry = Entry(short_name_lframe, textvariable=self.shrt_vendor_var, width=self.entry_width)
        self.short_name_entry.grid()
        self.short_name_entry.bind("<Key>", lambda key: self.UpdateFNsd(key))



        self.vendor_list, self.short_vendor, self.vendor_contact, self.vendor_mail, self.vendor_num, self.vendor_location = \
            self.GetVendorInfor()
        print(f'<{__name__}> Looking for Vendor CSV File Location in: {self.vendor_location}')

        add_sub_file_prev_frame = Frame(self)
        add_sub_file_prev_frame.grid(row=0, column=1, sticky=N+W+S)


        # Input frame for inputting shid
        self.input_frame = LabelFrame(
            self,
            text='Items Purchasing',
            padding=self.parent_flabel_pad
        )
        self.input_frame.grid(row=1, column=1, rowspan=5, columnspan=2, sticky=N+W+E+S)

        # add/sub line -----
        self.add_sub_line_frame = LabelFrame(
            add_sub_file_prev_frame,
            text='Add/Sub Line',
            padding=self.parent_flabel_pad
        )
        self.add_sub_line_frame.grid(row=0, column=0, sticky=N+W)
        self.line_count = -1
        self.line_array = []

        # file name preview -----
        self.file_preview = LabelFrame(
            add_sub_file_prev_frame,
            text='File Name Preview',
            padding=self.parent_flabel_pad
        )
        self.file_preview.grid(row=1, column=0, sticky=N+S+W)
        self.file_preview_var = StringVar()
        self.file_preview_var.set('D2-4-XXXXX-XXXXX-XXXXX - Purchase Order.xlsx')
        preview_label = Label(self.file_preview, textvariable=self.file_preview_var)
        preview_label.grid()

        self.vendor_choice = LabelFrame(
            self.vendor_frame,
            text='Purchasing From Who?',
            padding=self.parent_flabel_pad
        )
        self.vendor_choice.grid(row=1, column=0)
        self.vendor_dropdow = Combobox(self.vendor_choice, textvariable=self.vendor_name_var, values=self.vendor_list)
        self.vendor_dropdow.grid()
        self.vendor_dropdow.bind('<<ComboboxSelected>>', self.UpdateVendorShtuff)


        self.create_widgets()

    def create_widgets(self):
        """Create the widgets for the GUI"""
        self.QuoteSpecificWid()
        self.VendorWid()
        self.InputWid()


    def QuoteSpecificWid(self):
        # also check if the location of the dynamic project shipping frame
        date_frame = LabelFrame(
            self.quote_spec_frame,
            text='Date',
            padding=self.parent_flabel_pad
        )
        date_frame.grid(row=0, column=0, sticky=W)
        self.date_var.set(self.date_now)
        date_entry = Entry(
            date_frame,
            textvariable=self.date_var,
            width=self.entry_width
        )
        date_entry.grid()

        delivery_frame = LabelFrame(
            self.quote_spec_frame,
            text='Expected Delivery',
            padding=self.parent_flabel_pad
        )
        delivery_frame.grid(row=0, column=1, sticky=W)
        delivery_entry = Entry(
            delivery_frame,
            textvariable=self.expected_del_var,
            width=self.entry_width
        )
        delivery_entry.grid()

        quite_id_frame = LabelFrame(
            self.quote_spec_frame,
            text='Vendor Quote ID/Number',
            padding=self.parent_flabel_pad
        )
        quite_id_frame.grid(row=1, column=0, sticky=W)
        delivery_entry = Entry(
            quite_id_frame,
            textvariable=self.quote_id_var,
            width=self.entry_width
        )
        delivery_entry.grid()

        short_descript_frame = LabelFrame(
            self.quote_spec_frame,
            text='Enter Short Description',
            padding=self.parent_flabel_pad
        )
        short_descript_frame.grid(row=1, column=1, sticky=W)
        short_descript_entry = Entry(
            short_descript_frame,
            textvariable=self.short_descript_var,
            width=self.entry_width
        )
        short_descript_entry.grid()
        short_descript_entry.bind("<Key>", lambda key: self.UpdateFND(key))

        charged_to_frame = LabelFrame(
            self.quote_spec_frame,
            text='Payment Method',
            padding=self.parent_flabel_pad
        )
        charged_to_frame.grid(row=2, column=0, sticky=W)
        charged_to_option = Combobox(
            charged_to_frame,
            textvariable=self.charged_to_var,
            values=self.payment_options
        )
        charged_to_option.current(0)
        charged_to_option.grid()


    def VendorWid(self):
        vendor_reset_butt = Button(self.vendor_frame, text='⟳', command=self.ClearVendor)
        vendor_reset_butt.grid(row=0, sticky=W)
        vendor_reset_butt.config(width=3)

        vendor_loc_frame = LabelFrame(
            self.vendor_frame,
            text='Vendor Location',
            padding=self.parent_flabel_pad
        )
        vendor_loc_frame.grid(row=1, column=1)
        vendor_contact_e = Entry(vendor_loc_frame, textvariable=self.vendor_loc_var, width=self.entry_width)
        vendor_contact_e.grid()

        vendor_contact_frame = LabelFrame(
            self.vendor_frame,
            text='Contact',
            padding=self.parent_flabel_pad
        )
        vendor_contact_frame.grid(row=2, column=0)
        vendor_contact_e = Entry(vendor_contact_frame, textvariable=self.vendor_contact_var, width=self.entry_width)
        vendor_contact_e.grid()

        vendor_email_frame = LabelFrame(
            self.vendor_frame,
            text='Vendor Contact Email',
            padding=self.parent_flabel_pad
        )
        vendor_email_frame.grid(row=2, column=1)
        vendor_email_e = Entry(vendor_email_frame, textvariable=self.vendor_email_var, width=self.entry_width)
        vendor_email_e.grid()

        vendor_number_frame = LabelFrame(
            self.vendor_frame,
            text='Phone Number',
            padding=self.parent_flabel_pad
        )
        vendor_number_frame.grid(row=3, column=0)
        vendor_num_e = Entry(vendor_number_frame, textvariable=self.vendor_number_var, width=self.entry_width)
        vendor_num_e.grid()

        submit_butt = Button(self.vendor_frame, text='Submit/Generate', command=self.SubmitGenerate)
        submit_butt.grid(row=4, column=0, columnspan=2)


    def InputWid(self):
        add_butt = Button(self.add_sub_line_frame, text='+', command=self.CreateLine)
        sub_butt = Button(self.add_sub_line_frame, text='-', command=self.DeleteLastLine)

        add_butt.grid(row=0, column=0)
        sub_butt.grid(row=0, column=1)

        self.CreateLine()

    def CreateLine(self):
        self.line_count += 1

        print(f'<{__name__}> Creating Line at row {self.line_count + 1}')

        new_line = ALine(self.input_frame, self.line_count)
        self.line_array.append(new_line)


    def DeleteLastLine(self):
        if self.line_count <= 0:
            print(f'<{__name__}> Min number of lines reached')
            messagebox.showwarning("No Can Do", "You can't do that homie. You only have one line left")
            return

        self.line_count -= 1
        self.line_array[-1].Delete()
        self.line_array.pop()


    def UpdateVendorShtuff(self, event=None):
        descript = self.short_descript_var.get()
        project = self.proj_var.get()

        self.short_name_entry.config(state='disabled')


        vendor_title = self.vendor_name_var.get()

        indexed = self.vendor_list.index(vendor_title)

        self.vendor_loc_var.set(self.vendor_location[indexed])
        self.vendor_email_var.set(self.vendor_mail[indexed])
        self.vendor_number_var.set(self.vendor_num[indexed])
        self.vendor_contact_var.set(self.vendor_contact[indexed])


        self.shrt_vendor_var.set(self.short_vendor[indexed])
        shrt_vendor = self.shrt_vendor_var.get()

        if len(project) == 0:
            project = 'XXXXX'
        if len(descript) == 0:
            descript = 'XXXXX'
        if len(shrt_vendor) == 0:
            shrt_vendor = 'XXXXX'

        shin_dig = f"D2-4-{shrt_vendor}-{project}-{descript} - Purchase Order.xlsx"
        # print(shin_dig)
        self.file_preview_var.set(shin_dig)


    def ClearVendor(self):
        self.short_name_entry.config(state='enabled')

        self.vendor_list, self.short_vendor, self.vendor_contact, self.vendor_mail, self.vendor_num, self.vendor_location = \
            self.GetVendorInfor()

        self.vendor_dropdow.destroy()

        self.vendor_dropdow = Combobox(self.vendor_choice, textvariable=self.vendor_name_var, values=self.vendor_list)
        self.vendor_dropdow.grid()
        self.vendor_dropdow.bind('<<ComboboxSelected>>', self.UpdateVendorShtuff)



        descript = self.short_descript_var.get()
        project = self.proj_var.get()

        if len(project) == 0:
            project = 'XXXXX'
        if len(descript) == 0:
            descript = 'XXXXX'

        shrt_vendor = 'XXXXX'

        shin_dig = f"D2-4-{shrt_vendor}-{project}-{descript} - Purchase Order.xlsx"
        # print(shin_dig)
        self.file_preview_var.set(shin_dig)

        self.shrt_vendor_var.set('')
        self.vendor_name_var.set('')
        self.vendor_loc_var.set('')
        self.vendor_email_var.set('')
        self.vendor_number_var.set('')
        self.vendor_contact_var.set('')

    def GetCurrentDate(self, seconds=False, slash=True):
        now = datetime.now()
        if slash:
            return now.strftime('%m/%d/%Y')
        if not slash:
            return now.strftime('%m%y')

    def UpdateFND(self, key):
        descript = self.short_descript_var.get()
        project = self.proj_var.get()
        shrt_vendor = self.shrt_vendor_var.get()

        code = key.keycode
        if 65 <= code <= 90 or 48 <= code <= 57 or 96 <= code <= 105:
            char = key.char
        elif code == 8:
            descript = descript[:-1]
            char = ''
        else:
            char = ''
        if len(descript) == 0 and code == 8:
            descript = 'XXXXX'
        if len(project) == 0:
            project = 'XXXXX'
        if len(shrt_vendor) == 0:
            shrt_vendor = 'XXXXX'

        descript = f'{descript}{char}'

        shin_dig = f"D2-4-{shrt_vendor}-{project}-{descript} - Purchase Order.xlsx"
        # print(shin_dig)
        self.file_preview_var.set(shin_dig)

    def UpdateFNP(self, key=None):
        descript = self.short_descript_var.get()
        project = self.proj_var.get()
        shrt_vendor = self.shrt_vendor_var.get()
        # print(key)
        if key.x != 0:
            code = key.keycode

            if 65 <= code <= 90 or 48 <= code <= 57 or 96 <= code <= 105:
                char = key.char
            elif code == 8:
                project = project[:-1]
                char = ''
            else:
                char = ''

            if len(project) == 0 and code == 8:
                project = 'XXXXX'
        else:
            char = ''
        if len(descript) == 0:
            descript = 'XXXXX'
        if len(shrt_vendor) == 0:
            shrt_vendor = 'XXXXX'
        project = f'{project}{char}'

        shin_dig = f"D2-4-{shrt_vendor}-{project}-{descript} - Purchase Order.xlsx"

        self.file_preview_var.set(shin_dig)

    def UpdateFNsd(self, key):
        descript = self.short_descript_var.get()
        project = self.proj_var.get()
        shrt_vendor = self.shrt_vendor_var.get()

        code = key.keycode

        if 65 <= code <= 90 or 48 <= code <= 57 or 96 <= code <= 105:
            char = key.char
        elif code == 8:
            shrt_vendor = shrt_vendor[:-1]
            char = ''
        else:
            char = ''

        if len(project) == 0:
            project = 'XXXXX'
        if len(descript) == 0:
            descript = 'XXXXX'
        if len(shrt_vendor) == 0 and code == 8:
            shrt_vendor = 'XXXXX'
        shrt_vendor = f'{shrt_vendor}{char}'

        shin_dig = f"D2-4-{shrt_vendor}-{project}-{descript} - Purchase Order.xlsx"

        self.file_preview_var.set(shin_dig)


    def GetVendorInfor(self):
        # ill code this later
        vendor_lists = LoadVendors()



        vendor_list = vendor_lists[0]
        short_vendor = vendor_lists[1]

        vendor_contact = vendor_lists[3]
        vendor_loc = vendor_lists[4]
        vendor_num = vendor_lists[5]
        vendor_mail = vendor_lists[6]

        # print(f'vendor\n{vendor_loc}')

        return vendor_list, short_vendor, vendor_contact, vendor_mail, vendor_num, vendor_loc


    def SubmitGenerate(self):
        item_purch_lst = []
        quantitty_purchased_lst = []
        amount_per_lst = []

        for line in self.line_array:
            item_purchased, quantitty, amount_per = line.GetLine()

            item_purch_lst.append(item_purchased)
            quantitty_purchased_lst.append(quantitty)
            amount_per_lst.append(amount_per)

        item_quant_amnt_lst = [item_purch_lst, quantitty_purchased_lst, amount_per_lst]
        # 0-Date, 1-short_D, 2-payment, 3-proj#, 4-vendor, 5-contact, 6-email, 7-phone#
        other_shtuff_lst = [
            self.date_var.get(),
            self.short_descript_var.get(),
            self.charged_to_var.get(),
            self.proj_var.get(),
            self.vendor_name_var.get(),
            self.vendor_contact_var.get(),
            self.vendor_email_var.get(),
            self.vendor_number_var.get(),
            self.quote_id_var.get(),
            self.expected_del_var.get(),
            self.vendor_loc_var.get(),
        ]

        if self.IsEmpty(item_quant_amnt_lst, other_shtuff_lst):
            return

        continue_q = messagebox.askyesnocancel('Continue?', 'Submit and Generate?')

        if continue_q != True:
            return

        now = datetime.now()
        year = now.year

        general_year_ps_loc = f"Finance\\Yearly_Purchase_Orders\\{year}"

        if not path.isdir(general_year_ps_loc):
            mkdir(general_year_ps_loc)

        shop_q = False
        shop_year_folder = None
        if other_shtuff_lst[3] == "Shop":

            month = now.strftime('%B')


            shop_year_folder = f'Shop\\{year}'
            shop_month_folder = f'{shop_year_folder}\\{month}'
            # special_shop_month = f'{shop_year_folder}'
            purchase_order_folder = f'{shop_month_folder}\\Purchase_Orders'


            shop_q = True

            if not path.isdir(purchase_order_folder):
                mkdir(purchase_order_folder)




        else:

            purchase_order_folder = f'Projects\\{other_shtuff_lst[3]}\\Purchase_Orders'

            if not path.isdir(purchase_order_folder):
                mkdir(purchase_order_folder)



        dws_tot_count = self.IncreasePurchaseCount(shop_q)

        final_file_name = f'PO{dws_tot_count} {self.file_preview_var.get()}'

        general_po_loc = f"{general_year_ps_loc}\\{final_file_name}"

        purchase_order_dest_loc = f'{purchase_order_folder}\\{final_file_name}'



        copyfile(self.purchase_order_loc, purchase_order_dest_loc)

        AddDataToExcel(
            excel_loc=purchase_order_dest_loc,
            sheet_name='INPUT',
            col_loc=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
            row_list_data=[
                0,
                other_shtuff_lst[3],
                other_shtuff_lst[8],
                other_shtuff_lst[9],
                other_shtuff_lst[4],
                other_shtuff_lst[10],
                other_shtuff_lst[5],
                other_shtuff_lst[7],
                other_shtuff_lst[6],
                other_shtuff_lst[2],
                other_shtuff_lst[0],
                item_quant_amnt_lst[0],
                item_quant_amnt_lst[1],
                item_quant_amnt_lst[2],
                dws_tot_count
            ],
            place_loc=(0, 0),
            scan_min=(0, 0),
            scan_max=(15, 15)
        )


        self.AddToMasterExcel(item_quant_amnt_lst, other_shtuff_lst, dws_tot_count, shop_loc=shop_year_folder)

        copyfile(purchase_order_dest_loc, general_po_loc)

        for line in self.line_array:
            line.Delete()

        self.line_count = -1
        self.line_array = []

        self.CreateLine()

        self.date_var.set(self.date_now)
        self.short_descript_var.set('')
        self.charged_to_var.set('NET 30')
        self.proj_var.set('')
        self.vendor_name_var.set('')
        self.vendor_contact_var.set('')
        self.vendor_email_var.set('')
        self.vendor_number_var.set('')
        self.quote_id_var.set('')
        self.expected_del_var.set('')
        self.vendor_loc_var.set('')
        self.shrt_vendor_var.set('')
        self.short_name_entry.config(state='enable')
        self.file_preview_var.set('D2-4-XXXXX-XXXXX-XXXXX - Purchase Order.xlsx')

        if self.top_level != None:
            self.destroy()
            self.top_level.destroy()



    def IsEmpty(self, item_quant_amnt_lst, other_shtuff_lst):
        now_now = datetime.now()
        year = now_now.year
        month = now_now.strftime('%B')

        year_folder_path = f'Shop\\{year}'
        folder_path = f"{year_folder_path}\\{month}"

        # checking if that year of shop purchases exists
        if not path.isdir(year_folder_path) or not path.isdir(folder_path):
            CreateNewProject(shop_q=True)

        project = other_shtuff_lst[3]
        shop_q__in_empty = False
        if project != "Shop":
            not_shop_folder_path = f"Projects\\{project}"
            project_master_excel = f'{not_shop_folder_path}\\{project}-master.xlsx'
            src_folder = f'{not_shop_folder_path}\\!src'
            project_purchase_csv = f'{src_folder}\\{project}p.csv'
            project_log_csv = f'{src_folder}\\{project}p_log.csv'

            message_file_open = f"{project_master_excel} is open. Make sure you close it before you begin."
            master_open_q = XLCheckIfOpen(file=project_master_excel, title="Close File", message=message_file_open)

            message_file_open1 = f"{project_purchase_csv} is open. Make sure you close it before you begin."
            p_open = CSVCheckIfOpen(file=project_purchase_csv, title="Close File", message=message_file_open1)

            message_file_open2 = f"{project_log_csv} is open. Make sure you close it before you begin."
            p_log_open = CSVCheckIfOpen(file=project_log_csv, title="Close File", message=message_file_open2)

        else:

            project_pathxlsx = f'{folder_path}\\{month}-master.xlsx'
            src_folder = f'{folder_path}\\!src'
            project_purchase_csv = f'{src_folder}\\{month}p.csv'
            project_log_csv = f'{src_folder}\\{month}p_log.csv'






            message_file_open = f"{project_pathxlsx} is open. Make sure you close it before you begin."
            master_open_q = XLCheckIfOpen(file=project_pathxlsx, title="Close File", message=message_file_open)

            message_file_open1 = f"{project_purchase_csv} is open. Make sure you close it before you begin."
            p_open = CSVCheckIfOpen(file=project_purchase_csv, title="Close File", message=message_file_open1)

            message_file_open2 = f"{project_log_csv} is open. Make sure you close it before you begin."
            p_log_open = CSVCheckIfOpen(file=project_log_csv, title="Close File", message=message_file_open2)

        #
        if master_open_q or p_open or p_log_open:
            return True


        list_1_str_stuffs = ['Item', 'Quantitty', 'Amount']
        list_2_str_stuffs = [
            'Date',
            'Short Description',
            'Payment Method',
            'Project Number',
            'Vendor Name',
            'Vendor Contact',
            'Vendor Email',
            'Contact Number',
            'Quote ID',
            'Expected Delivery',
            'Vendor Location'
        ]

        for i, item_quant_amnt in enumerate(item_quant_amnt_lst):
            for j, element in enumerate(item_quant_amnt):

                if element == '':
                    messagebox.showwarning(title=f'Nuh uh, my dude: Empty {list_1_str_stuffs[i]}',
                                           message=f'Missing {list_1_str_stuffs[i]} in line {j + 1}, my man\n\ntsk tsk')
                    return True

                blah = element.replace('.', '', 1)
                # print(f'_________________________{blah}')
                if not blah.isdigit() and i == 2:
                    messagebox.showwarning(title='My hommie... Incorrect Amount',
                                           message=f'Must be a number on line {j + 1} Amount\n'
                                                   f'Do you know what a number is???')
                    return True

                if not element.isdigit() and i == 1:
                    messagebox.showwarning(title='My hommie... Incorrect Quantitty',
                                           message=f'Must be a number on line {j + 1} Quantitty\n'
                                                   f'Do you know what a number is???')
                    return True

        for i, input_info in enumerate(other_shtuff_lst):
            if input_info == '' and i < 7:
                messagebox.showwarning(title=f'My dude...tsk tsk tsk:Empty {list_2_str_stuffs[i]}',
                                       message=f'Missing {list_2_str_stuffs[i]}\n'
                                               f'Come on bruh\n'
                                               f'Get it together')
                return True

            elif input_info == '':
                skip_q = messagebox.askokcancel(title=f'Possibly Okay:Empty {list_2_str_stuffs[i]}',
                                       message=f'Missing {list_2_str_stuffs[i]}\n'
                                               f'Just letting you know that it is empty')
                if skip_q != True:
                    return True

        preview = self.file_preview_var.get()

        if path.isfile(preview):
            messagebox.showwarning(title=f'Could be good, could be bad',
                                   message=f'A purchase order already exists with that name.\n'
                                           f'hmmmmmmm hope that is not bad news...')
            return True
        if project != "Shop":
            if not path.isdir(f'Projects\\{project}'):
                messagebox.showwarning(title=f'BRUH............',
                                       message=f'{other_shtuff_lst[3]} does not exist dude\n'
                                               f'So either check your project number or make a new one\n'
                                               f'also, you suck')

                return True

        return False


    def IncreasePurchaseCount(self, shop_q):
        purchase_order_var = 'Purchase_Order_Count'
        if not shop_q:

            proj_stats_loc = f'Projects\\{self.proj_var.get()}\\!src\\stats.txt'
            if not path.isdir(f'Projects\\{self.proj_var.get()}\\!src'):
                print(f'<{__name__}> Sorry bruv, could not find: Projects\\{self.proj_var.get()}\\!src')
                proj_stats_loc = f'Projects\\{self.proj_var.get()}\\src\\stats.txt'

            proj_stats = GetVar(proj_stats_loc, True)


            IncrementGivenStat(
                stat_file=proj_stats_loc,
                stat_str=purchase_order_var,
                increment=1,
                comment_lines=proj_stats[0],
                working_vars=proj_stats[1],
                var_vars=proj_stats[2]
            )

        date = self.GetCurrentDate(slash=False)
        year = datetime.now().year
        month = datetime.now().strftime("%B")

        dws_stats_loc = f'Shop\\{year}'
        shop_stat_loc = f'\\{month}\\!src\\stats.txt'

        # if not path.isdir(dws_stats_loc):
        #     CreateNewProject(shop_q=True)

        shop_stats_loc = f'{dws_stats_loc}{shop_stat_loc}'
        shop_stats = GetVar(shop_stats_loc, True)

        dws_total_purchase = IncrementGivenStat(
            stat_file=shop_stats_loc,
            stat_str=purchase_order_var,
            increment=1,
            comment_lines=shop_stats[0],
            working_vars=shop_stats[1],
            var_vars=shop_stats[2]
        )


        return f'{date}{dws_total_purchase}'


    def AddToMasterExcel(self, item_quant_amnt_lst: list, other_shtuff_lst, dws_tot_count, shop_loc=None):
        project = other_shtuff_lst[3]

        projects_folder = "Projects"

        if shop_loc != None:
            projects_folder = shop_loc

            now_now = datetime.now()
            # equals month
            project = now_now.strftime('%B')


        project_purchase_csv = f'{projects_folder}\\{project}\\!src\\{project}p.csv'

        project_log_csv = f'{projects_folder}\\{project}\\!src\\{project}p_log.csv'


        project_master_excel = f'{projects_folder}\\{project}\\{project}-master.xlsx'

        now_now = datetime.now()
        year = now_now.year
        month = now_now.strftime('%B')
        full_date = now_now.strftime('%m/%d/%Y')
        cc_purch_log_year_folder = f'Finance\\Monthly_Credit_Card_Purchases\\{year}'
        cc_purchase_log = f'{cc_purch_log_year_folder}\\{month}.csv'

        p_csv_lines = []
        l_csv_lines = [
            [
                other_shtuff_lst[3],
                dws_tot_count,
                other_shtuff_lst[2],
                other_shtuff_lst[4],
                other_shtuff_lst[5],
                other_shtuff_lst[8],
                other_shtuff_lst[9],
            ]
        ]
        for i in range(len(item_quant_amnt_lst[0])):
            p_csv_lines.append(
                [
                    full_date, 
                    item_quant_amnt_lst[0][i],
                    other_shtuff_lst[4],
                    other_shtuff_lst[2],
                    item_quant_amnt_lst[1][i], 
                    item_quant_amnt_lst[2][i],
                    str(float(item_quant_amnt_lst[1][i]) * float(item_quant_amnt_lst[2][i]))
                ]
            )

            l_csv_lines.append(
                [
                    full_date,
                    item_quant_amnt_lst[0][i],
                    item_quant_amnt_lst[1][i],
                    item_quant_amnt_lst[2][i]
                ]
            )
        print(f"<{__name__}> Line to {project}: {p_csv_lines}")
        print(f"<{__name__}> Line to {project} log: {l_csv_lines}")
        p_csv_q = False



        if not path.isfile(project_purchase_csv):
            p_csv_q = True

        # csv for input into project master file
        with open(project_purchase_csv, 'a+', newline='') as write_obj:
            csv_writer = writer(write_obj)

            if p_csv_q:
                pcsv_first_line = ['Date', 'Description', 'Vendor', 'Charged To', 'Price each/per weight', 'Qty', 'Total Each']
                csv_writer.writerow(pcsv_first_line)


            csv_writer.writerows(p_csv_lines)

        # for logging csv
        with open(project_log_csv, 'a+', newline='') as write_obj:
            csv_writer = writer(write_obj)

            csv_writer.writerows(l_csv_lines)

        # for keeping track of credit card purchases
        if other_shtuff_lst[2] != 'NET 30':

            if not path.isdir(cc_purch_log_year_folder):
                mkdir(cc_purch_log_year_folder)

            cc_csv_q = False
            if not path.isfile(cc_purchase_log):
                cc_csv_q = True
            with open(cc_purchase_log, 'a+', newline='') as write_obj:
                csv_writer = writer(write_obj)

                if cc_csv_q:
                    cc_csv_first_line = ['Date', 'Description', 'Vendor', 'Charged To', 'Price each/per weight', 'Qty', 'Total Each']
                    csv_writer.writerow(cc_csv_first_line)

                print(f"Writing lines: {p_csv_lines} to file: {cc_purchase_log}")

                csv_writer.writerows(p_csv_lines)

        # appending csv to master excel
        # code for handling legacy master files
        df = read_csv(project_purchase_csv)
        append_df_to_excel(
            project_master_excel,
            df=df,
            sheet_name=f'{project}_purchases',
            startrow=2,
            startcol=1,
            index=False,
            no_pic=True
        )


class ALine:

    def __init__(self, parent, l_num,):
        super().__init__()
        self.inside_of = parent
        self.line_num = l_num


        self.line_frame = Frame(self.inside_of)
        self.line_frame.grid(row=1 + self.line_num, column=1, sticky=N)

        self.item_var = StringVar()
        self.quantitty_var = StringVar()
        self.amount_var = StringVar()

        self.MakeLine()


    def MakeLine(self):
        # condition to only put the column names go into the first line
        if self.line_num == 0:
            line_label = Label(self.line_frame, text='Ln.')
            item_label = Label(self.line_frame, text='Item')
            amount_label = Label(self.line_frame, text='Amount')
            quatiddy_label = Label(self.line_frame, text='Quantity')
            line_label.grid(row=0, column=0, sticky=N+W)
            item_label.grid(row=0, column=1, sticky=N)
            amount_label.grid(row=0, column=2, sticky=N)
            quatiddy_label.grid(row=0, column=3, sticky=N)

        label_ln_num = Label(self.line_frame, text=f'{self.line_num + 1}   -   ')

        item_entry = Entry(self.line_frame, textvariable=self.item_var, width=40)
        amount_entry = Entry(self.line_frame, textvariable=self.amount_var, width=10)
        quantitty_entry = Entry(self.line_frame, textvariable=self.quantitty_var, width=8)


        label_ln_num.grid(row=1, column=0)

        item_entry.grid(row=1, column=1)
        amount_entry.grid(row=1, column=2)
        quantitty_entry.grid(row=1, column=3)


    def Delete(self):
        for widget in self.line_frame.winfo_children():
            widget.destroy()

        self.line_frame.destroy()

    def GetLine(self):
        item = self.item_var.get()
        qtty = self.quantitty_var.get()
        amnt = self.amount_var.get()

        return item, qtty, amnt

    def GiveFrameData(self):
        return self.line_frame

