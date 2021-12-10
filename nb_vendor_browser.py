from tkinter import StringVar, BooleanVar, IntVar, messagebox, N, W, E, S, NW, Text, END, GROOVE, Canvas, Toplevel
from tkinter.ttk import Frame, Radiobutton, Label, Entry, Button, Combobox, LabelFrame, Scrollbar, Style

from operator import itemgetter
from csv import writer, reader
from os import startfile

from general_funcs import AddDataToExcel, GetVar, LoadVendors
from nb_project_browser import GetDocList
from globalz import general_file_loc


vendor_csv_loc = general_file_loc[6]



def SortVendorList(csv_list):
    first_line = csv_list[0]
    w_o_first_line = csv_list[1:]
    w_o_first_line.sort()
    w_o_first_line.insert(0, first_line)
    return w_o_first_line


def UpdateVendorCSV(i_row, vendor_list):
    i_row += 1



    with open(vendor_csv_loc, 'r', newline='') as reader_csvfile:
        # print(f'getting info from {vendor_csv_loc}')
        data = [line for line in reader(reader_csvfile)]
        # print(data)

    try:
        # print('Tried opening it first')
        # vendor_list [vendor, contact, loc, num, mail]
        with open(vendor_csv_loc, 'w', newline='') as try_reader_csvfile:
            writer(try_reader_csvfile).writerows(data)
    except PermissionError:
        messagebox.showwarning('CSV File Open', f'Make sure the CSV is closed before you proceed\n'
                                                f'CSV File: {vendor_csv_loc}')
        return True

    for enumed, row in enumerate(data):

        if enumed == i_row:
            # print(row)
            row[0] = vendor_list[0]
            # skipping row[1 and 2] technically columns 1 and 2
            row[3] = vendor_list[1]
            row[4] = vendor_list[2]
            row[5] = vendor_list[3]
            row[6] = vendor_list[4]
            data[i_row] = row

    data = SortVendorList(data)

    with open(vendor_csv_loc, 'w', newline='') as writer_csvfile:
        writer(writer_csvfile).writerows(data)

    return None


def AppendCSV(line):
    with open(vendor_csv_loc, 'r', newline='') as reader_csvfile:
        # print(f'getting info from {vendor_csv_loc}')
        data = [line for line in reader(reader_csvfile)]
        # print(data)

    try:
        # print('Tried opening it first')
        # vendor_list [vendor, contact, loc, num, mail]
        with open(vendor_csv_loc, 'w', newline='') as try_reader_csvfile:
            writer(try_reader_csvfile).writerows(data)
    except PermissionError:
        messagebox.showwarning('CSV File Open', f'Make sure the CSV is closed before you proceed\n'
                                                f'CSV File: {vendor_csv_loc}')
        return True

    data.append(line)

    data = SortVendorList(data)

    with open(vendor_csv_loc, 'w', newline='') as writer_csvfile:
        writer(writer_csvfile).writerows(data)

    return None


class ScrollableFrame(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.config(height=500, width=550)
        canvas = Canvas(self, height=500, width=550)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        self.scrollable_frame['padding'] = (5, 5, 5, 5)

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.grid(row=0, column=0, sticky=W+E)
        scrollbar.grid(row=0, column=1, sticky=N+S+E)


class DisplayVendors(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.parent_flabel_pad = (5, 5)

        self.scrolls = ScrollableFrame(self)
        self.scrolls.grid(row=0, column=0, sticky=N+S+E+W)

        self.search_var = StringVar(self)
        self.vendor_list = []

        self.CreateWidgets()

    def CreateWidgets(self):
        butt_frame = Frame(self)
        butt_frame.grid(row=0, column=1, sticky=N+S+E+W)

        set_lframe = LabelFrame(butt_frame, text='Reset and Source File', padding=self.parent_flabel_pad)
        set_lframe.grid(row=0, column=0, sticky=W+E)
        add_delete_lframe = LabelFrame(butt_frame, text='Add or Delete Vendors', padding=self.parent_flabel_pad)
        add_delete_lframe.grid(row=1, column=0, sticky=W+E)
        search_lframe = LabelFrame(butt_frame, text='Search', padding=self.parent_flabel_pad)
        search_lframe.grid(row=2, column=0, sticky=W + E)

        refresh_butt = Button(set_lframe, text='⟳', command=lambda: self.RefreshScroll(clear_search=True), width=3)
        refresh_butt.grid(row=0, column=0, sticky=W + E)

        open_csv_butt = Button(set_lframe, text='Open CSV', command=self.OpenVendorCsv)
        open_csv_butt.grid(row=0, column=1, sticky=N + E)

        new_vendor_butt = Button(add_delete_lframe, text='New Vendor', command=self.NewVendor)
        new_vendor_butt.grid(row=0, column=0, sticky=N + E)

        delete_vendor_butt = Button(add_delete_lframe, text='Delete Vendor', command=self.DeleteVendor)
        delete_vendor_butt.grid(row=0, column=1, sticky=N + E)

        self.RefreshScroll()

        search_combo = Combobox(search_lframe, textvariable=self.search_var, values=self.vendor_list)
        search_combo.grid(row=0, column=0)
        search_combo.bind("<Key>", lambda key: self.SearchFunc(key))
        search_combo.bind("<<ComboboxSelected>>", self.SearchFunc)


    def RefreshScroll(self, sort=None, clear_search=False):
        if clear_search:
            self.search_var.set('')

        vendor_lists = LoadVendors()

        self.vendor_list = vendor_lists[0]
        refresh_vendor_lst = self.vendor_list
        shrt_vendor = vendor_lists[1]
        descript = vendor_lists[2]
        vendor_contact = vendor_lists[3]
        vendor_loc = vendor_lists[4]
        vendor_num = vendor_lists[5]
        vendor_mail = vendor_lists[6]



        if sort is not None:
            iter_list = []
            for ji, vendor in enumerate(self.vendor_list):
                if sort.lower() not in vendor.lower():
                    # print(f"'{sort.lower()}' not in {vendor.lower()}")
                    iter_list.append(ji)
                else:
                    # print(f"{ji}:'{sort.lower()}' is in {vendor.lower()}")
                    pass
            iter_list = sorted(iter_list, reverse=True)

            for iterz in iter_list:
                refresh_vendor_lst.pop(iterz)
                shrt_vendor.pop(iterz)
                descript.pop(iterz)
                vendor_contact.pop(iterz)
                vendor_loc.pop(iterz)
                vendor_num.pop(iterz)
                vendor_mail.pop(iterz)



        for given_proj_frame in self.scrolls.scrollable_frame.winfo_children():
            given_proj_frame.destroy()
        vendor_frame_list = []



        for i, vendor in enumerate(refresh_vendor_lst):
            vendor_data = [vendor_contact[i], vendor_loc[i], vendor_num[i], vendor_mail[i]]
            vendor_frame_list.append(
                VendorLineClass(
                    self.scrolls.scrollable_frame,
                    vendor,
                    shrt_vendor[i],
                    descript[i],
                    vendor_data,
                    i
                )
            )
        # print(len(refresh_vendor_lst))


    def OpenVendorCsv(self):
        startfile(vendor_csv_loc)


    def NewVendor(self):
        temp_vendor_win = Toplevel()
        temp_vendor_win.title('Add Vendor')
        temp_frame = Frame(temp_vendor_win)
        temp_frame.grid()
        temp_slip = AddVendor(vendor_class=self, master=temp_frame, top_level=temp_vendor_win)
        temp_slip.grid()

    def DeleteVendor(self):
        vendor_lists = LoadVendors()

        vendor_list = vendor_lists[0]

        temp_delete_win = Toplevel()
        temp_delete_win.title('Delete Vendor')
        temp_d_frame = Frame(temp_delete_win)
        temp_d_frame.grid()
        temp_delete = DeleteVendor(
            vendor_class=self,
            master=temp_d_frame,
            top_level=temp_delete_win,
            vendor_list=vendor_list
        )
        temp_delete.grid()


    def SearchFunc(self, key=None):
        search_var = self.search_var.get()

        # print(key.x)

        if key.x != 0:
            code = key.keycode
            if 65 <= code <= 90 or 48 <= code <= 57 or 96 <= code <= 105 or code == 32:
                # print(f'{code}: added to search var')
                typed_so_far = search_var + key.char
            elif code == 8:
                # print('did backspace')
                typed_so_far = search_var[:-1]
            else:
                return

        else:
            typed_so_far = search_var

        # print(key)
        # print(f"'{typed_so_far}'")
        self.RefreshScroll(sort=typed_so_far)






class VendorLineClass(Frame):
    # label frame name self.selectionFrame.configure(text="hello")
    def __init__(self, scrolls, vendor, shrt_vendor, descript, v_d, i):
        super().__init__(scrolls)
        style_frame = Frame(scrolls, relief=GROOVE)
        style_frame['padding'] = (5, 10, 5, 10)
        style_frame.grid(row=i, column=0, sticky=W+E)

        self.parent_flabel_pad = (5, 5)
        self.l_w = 35
        font_var = ('lucida', 10, 'underline')

        self.config(padding=self.parent_flabel_pad)


        self.label_frame__frame = Frame(scrolls)
        self.vendor_var = StringVar(master=self, value=vendor)

        self.shrt_vendor_var = StringVar(master=self, value=shrt_vendor)

        self.vendor_frame = LabelFrame(style_frame, labelwidget=self.label_frame__frame, borderwidth=1, labelanchor='nw', padding=self.parent_flabel_pad)
        self.vendor_frame.grid()

        self.line_in_csv = i

        descript_loc_frame = Frame(self.vendor_frame)

        contact_label = Label(scrolls, text='Contact', font=font_var)
        self.contact_lframe = LabelFrame(self.vendor_frame, labelwidget=contact_label, padding=self.parent_flabel_pad)
        self.vendor_contact_var = StringVar(master=self.vendor_frame, value=v_d[0])

        loc_label = Label(scrolls, text='Address', font=font_var)
        self.loc_lframe = LabelFrame(descript_loc_frame, labelwidget=loc_label, padding=self.parent_flabel_pad)
        self.vendor_loc_var = StringVar(master=self.vendor_frame, value=v_d[1])

        num_label = Label(scrolls, text='Phone Number', font=font_var)
        self.num_lframe = LabelFrame(self.vendor_frame, labelwidget=num_label, padding=self.parent_flabel_pad)
        self.vendor_num_var = StringVar(master=self.vendor_frame, value=v_d[2])

        mail_label = Label(scrolls, text='Email', font=font_var)
        self.mail_lframe = LabelFrame(self.vendor_frame, labelwidget=mail_label, padding=self.parent_flabel_pad)
        self.vendor_mail_var = StringVar(master=self.vendor_frame, value=v_d[3])

        descript_label = Label(scrolls, text='Description', font=font_var)
        self.descp_lframe = LabelFrame(descript_loc_frame, labelwidget=descript_label, padding=self.parent_flabel_pad)
        self.vendor_descp_var = StringVar(master=self.vendor_frame, value=descript)

        self.contact_lframe.grid(row=0, column=0, sticky=N + S)
        self.mail_lframe.grid(row=1, column=0, sticky=N + S)
        self.num_lframe.grid(row=2, column=0, sticky=N + S)
        descript_loc_frame.grid(row=0, column=1, rowspan=3, sticky=N + S)

        self.loc_lframe.grid(row=0, column=0, sticky=N + S)
        self.descp_lframe.grid(row=1, column=0, sticky=N + S)

        self.label_frame_list = [
            self.contact_lframe,
            self.loc_lframe,
            self.num_lframe,
            self.mail_lframe,
            self.descp_lframe
        ]



        self.CreateLabels()



    def CreateLabels(self):
        edit_butt = Button(master=self.label_frame__frame, text='Edit', command=self.EditVendor)
        edit_butt.grid(row=0, column=0)
        edit_butt.config(width=4)

        ven_label = Label(self.label_frame__frame, textvariable=self.vendor_var, font=('lucida', 15))
        ven_label.grid(row=0, column=1)

        shrt_ven_label = Label(self.label_frame__frame, textvariable=self.shrt_vendor_var, font=('lucida', 10))
        shrt_ven_label.grid(row=0, column=2)

        contact_label = Label(
            self.contact_lframe,
            textvariable=self.vendor_contact_var,
            width=self.l_w,
        )
        contact_label.grid()

        mail_label = Label(
            self.mail_lframe,
            textvariable=self.vendor_mail_var,
            width=self.l_w,
        )
        mail_label.grid()


        num_label = Label(
            self.num_lframe,
            textvariable=self.vendor_num_var,
            width=self.l_w,
        )
        num_label.grid()

        loc_label = Label(
            self.loc_lframe,
            textvariable=self.vendor_loc_var,
            width=self.l_w,
            wraplength=self.l_w*5,
        )
        loc_label.grid()

        descp_label = Label(
            self.descp_lframe,
            textvariable=self.vendor_descp_var,
            width=self.l_w,
            wraplength=self.l_w * 6,
        )
        descp_label.grid()

    def EditVendor(self):
        for widget in self.label_frame__frame.winfo_children():
            widget.destroy()
        for label_frame in self.label_frame_list:
            for widget in label_frame.winfo_children():
                widget.destroy()

        confirm_butt = Button(self.label_frame__frame, text='✓',
                              command=lambda: self.UpdateVenFromVars(loc_entry, descrp_entry))
        confirm_butt.config(width=3)
        vendor_entry = Entry(self.label_frame__frame, width=self.l_w, textvariable=self.vendor_var)
        shrt_vendor_entry = Entry(self.label_frame__frame, width=self.l_w, textvariable=self.shrt_vendor_var)

        confirm_butt.grid(row=0, column=0)
        vendor_entry.grid(row=0, column=1)
        shrt_vendor_entry.grid(row=0, column=2)

        contact_entry = Entry(self.contact_lframe, width=self.l_w, textvariable=self.vendor_contact_var)
        mail_entry = Entry(self.mail_lframe, width=self.l_w, textvariable=self.vendor_mail_var)
        num_entry = Entry(self.num_lframe, width=self.l_w, textvariable=self.vendor_num_var)
        loc_entry = Text(self.loc_lframe, height=3, width=26)
        loc_entry.insert('end', self.vendor_loc_var.get())

        descrp_entry = Text(self.descp_lframe, height=3, width=26)
        descrp_entry.insert('end', self.vendor_descp_var.get())

        contact_entry.grid()
        mail_entry.grid()
        num_entry.grid()
        loc_entry.grid()
        descrp_entry.grid()


    def UpdateVenFromVars(self, loc_text_bx=None, decrp_text_bx=None):
        loc_edited_text = loc_text_bx.get("1.0", "end")
        loc_edited_text = loc_edited_text.rstrip("\n")
        self.vendor_loc_var.set(loc_edited_text)

        decrp_edited_text = decrp_text_bx.get("1.0", "end")
        decrp_edited_text = decrp_edited_text.rstrip("\n")
        self.vendor_descp_var.set(decrp_edited_text)

        # list [vendor, contact, loc, num, mail]
        work_q = UpdateVendorCSV(self.line_in_csv, [
            self.vendor_var.get(),
            self.vendor_contact_var.get(),
            self.vendor_loc_var.get(),
            self.vendor_num_var.get(),
            self.vendor_mail_var.get()
        ])

        if work_q:
            return

        for widget in self.label_frame__frame.winfo_children():
            widget.destroy()
        for label_frame in self.label_frame_list:
            for widget in label_frame.winfo_children():
                widget.destroy()

        self.CreateLabels()


class AddVendor(Frame):
    def __init__(self, vendor_class, master=None, top_level=None):
        super().__init__(master)
        self.grid()
        self.parent_flabel_pad = (5, 5)
        self.entry_width = 23

        self.vendor_class = vendor_class
        self.top_level = top_level

        self.vendor_name_var = StringVar(master=master)
        self.shrt_vendor_name_var = StringVar(master=master)
        # DONT FORGET TEXT FOR THIS self.vendor_descrp_var = StringVar(master=master)
        self.vendor_contact_var = StringVar(master=master)
        # DONT FORGET TEXT FOR THIS self.vendor_loc_var = StringVar(master=master)
        self.vendor_num_var = StringVar(master=master)
        self.vendor_email_var = StringVar(master=master)

        self.text_list = []

        self.CreateWidgets()

    def CreateWidgets(self):
        vendor_name_lframe = LabelFrame(
            self,
            text='Vendor/Company Name',
            padding=self.parent_flabel_pad
        )
        vendor_name_lframe.grid(row=0, column=0)
        vendor_name_entry = Entry(
            vendor_name_lframe,
            textvariable=self.vendor_name_var,
            width=self.entry_width
        )
        vendor_name_entry.grid()
        # ------------------------------
        shrt_vendor_name_lframe = LabelFrame(
            self,
            text='Short Name',
            padding=self.parent_flabel_pad
        )
        shrt_vendor_name_lframe.grid(row=1, column=0)
        shrt_vendor_name_entry = Entry(
            shrt_vendor_name_lframe,
            textvariable=self.shrt_vendor_name_var,
            width=self.entry_width
        )
        shrt_vendor_name_entry.grid()
        # ------------------------------
        text_frame = Frame(self)
        text_frame.grid(row=0, column=1, rowspan=3)
        vendor_descrp_lframe = LabelFrame(
            text_frame,
            text='What Do They Sell?',
            padding=self.parent_flabel_pad
        )
        vendor_descrp_lframe.grid(row=0, column=0)
        vendor_descrp_entry = Text(vendor_descrp_lframe, height=3, width=26)

        vendor_descrp_entry.grid()
        # ------------------------------
        vendor_loc_lframe = LabelFrame(
            text_frame,
            text='Location\Address',
            padding=self.parent_flabel_pad
        )
        vendor_loc_lframe.grid(row=1, column=0)
        vendor_loc_entry = Text(vendor_loc_lframe, height=3, width=26)

        vendor_loc_entry.grid()
        # ------------------------------
        vendor_contact_lframe = LabelFrame(
            self,
            text='Contact',
            padding=self.parent_flabel_pad
        )
        vendor_contact_lframe.grid(row=0, column=2)
        vendor_contact_entry = Entry(
            vendor_contact_lframe,
            textvariable=self.vendor_contact_var,
            width=self.entry_width
        )
        vendor_contact_entry.grid()
        # ------------------------------
        vendor_mail_lframe = LabelFrame(
            self,
            text='Email',
            padding=self.parent_flabel_pad
        )
        vendor_mail_lframe.grid(row=1, column=2)
        vendor_mail_entry = Entry(
            vendor_mail_lframe,
            textvariable=self.vendor_email_var,
            width=self.entry_width
        )
        vendor_mail_entry.grid()
        # ------------------------------
        vendor_num_lframe = LabelFrame(
            self,
            text='Phone Number',
            padding=self.parent_flabel_pad
        )
        vendor_num_lframe.grid(row=2, column=2)
        vendor_num_entry = Entry(
            vendor_num_lframe,
            textvariable=self.vendor_num_var,
            width=self.entry_width
        )
        vendor_num_entry.grid()


        confirm_butt = Button(self, text='Confirm', command=self.CSVAddAndUpdate)
        confirm_butt.grid(row=2, column=0)

        self.text_list = [vendor_descrp_entry, vendor_loc_entry]

    def CSVAddAndUpdate(self):
        given_line = [
            self.vendor_name_var.get(),
            self.shrt_vendor_name_var.get(),
            self.text_list[0].get("1.0", "end"),
            self.vendor_contact_var.get(),
            self.text_list[1].get("1.0", "end"),
            self.vendor_num_var.get(),
            self.vendor_email_var.get()
        ]

        execute_q = AppendCSV(line=given_line)

        if execute_q:
            return

        self.vendor_class.RefreshScroll()

        self.top_level.destroy()


class DeleteVendor(Frame):
    def __init__(self, vendor_class, master=None, top_level=None, vendor_list=None):
        super().__init__(master)
        self.grid()
        self.parent_flabel_pad = (5, 5)
        self.entry_width = 23

        self.vendor_class = vendor_class
        self.top_level = top_level

        self.choice_var = StringVar(master=master)

        decision = Combobox(
            self,
            textvariable=self.choice_var,
            state="readonly",
            values=vendor_list
        )
        decision.grid(row=0, column=0)

        confirm_buttz = Button(self, text='Delete Vendor', command=self.DeleteVenCSV)
        confirm_buttz.grid(row=1, column=0)

    def DeleteVenCSV(self):
        with open(vendor_csv_loc, 'r', newline='') as reader_csvfile:
            # print(f'getting info from {vendor_csv_loc}')
            data = [line for line in reader(reader_csvfile)]
            # print(data)

        try:

            # print('Tried opening it first')
            with open(vendor_csv_loc, 'w', newline='') as try_reader_csvfile:
                writer(try_reader_csvfile).writerows(data)

        except PermissionError:
            messagebox.showwarning('CSV File Open', f'Make sure the CSV is closed before you proceed\n'
                                                    f'CSV File: {vendor_csv_loc}')
            return

        choice = self.choice_var.get()

        no_col_labels = data[1:]

        for ij, line in enumerate(no_col_labels):
            if line[0] == choice:
                data.pop(ij+1)

        with open(vendor_csv_loc, 'w', newline='') as try_reader_csvfile:
            writer(try_reader_csvfile).writerows(data)

        self.vendor_class.RefreshScroll()

        self.top_level.destroy()


