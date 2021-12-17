from tkinter import StringVar, BooleanVar, IntVar, messagebox, N, W, E, S, NW, Text, END, Checkbutton
from tkinter.ttk import Frame, Label, Entry, Button, Combobox, LabelFrame
from os import startfile, path, mkdir
from shutil import copyfile
from datetime import datetime

from general_funcs import AddDataToExcel, GetVar
from igs_funcs import LoadData, GoToTracking, IGS_Generate_Update_Logs



def CreateProjectDocument(project, doc):
    print(f'<{__name__}> Creating document {doc} for project {project}')
    if path.isdir(f'Projects\\{project}'):
        loc_list = ['D1 - Employee', 'D2 - Documentation', 'D3 - Manufacturing', 'D4 - Maintenance']
        file_loc_int = int(doc[1]) - 1
        copy_loc = f'Quality_Control\\!D - Documents\\{loc_list[file_loc_int]}\\{doc}.xlsx'


        split_doc = doc.split(' - ')
        destination = f'Projects\\{project}\\{split_doc[0]}-{project} - {split_doc[1]}.xlsx'

        if path.exists(destination):
            messagebox.showinfo('Brah, That Already Exists', 'That File Already Exists.\nEdit Document Instead...\nIDIOT')
            return


        copyfile(copy_loc, destination)
        AddDataToExcel(
            excel_loc=destination,
            sheet_name='INPUT',
            col_loc=[1],
            row_list_data=[str(project)],
            place_loc=(0, 0),
            scan_min=(0, 0),
            scan_max=(2, 2)
        )

        messagebox.showinfo(f"Doc: {doc} Created", f"Doc: {doc} created for Project: {project}")

    else:
        create_new_proj = messagebox.showwarning(
            f'{project} Does Not Exist, bruv',
            f'{project} does not exist. Check your Project Number, homie?'
        )
        return



class PackingSlipPage(Frame):
    GoToTracking()

    def __init__(self, master=None, from_project=False, top_level=None):
        super().__init__(master)
        self.grid()

        self.destrou_top_level = top_level

        igs_shtuff = GetVar('Python_Source\!variables\igs_tracking_var.txt', False)
        self.inv_file_loc = igs_shtuff[2]
        list_thang = LoadData(self.inv_file_loc)
        self.igs_items = list_thang[0]

        self.project_butt = from_project

        self.line_list = []
        self.line_count = -1

        self.parent_flabel_pad = (5, 5)

        self.input_frame = LabelFrame(self, text='Input', padding=self.parent_flabel_pad)
        self.input_frame.grid(row=0, column=1, rowspan=3, sticky=N)

        self.add_sub_frame = LabelFrame(self, text='Add/Sub Line', padding=self.parent_flabel_pad)
        self.add_sub_frame.grid(row=0, column=0, sticky=N+W+E)

        self.ship_proj_frame = LabelFrame(self, text='|Ship To|', padding=self.parent_flabel_pad)
        self.ship_proj_frame.grid(row=1, column=0, sticky=N)

        self.window_q = True

        if not self.project_butt:
            self.project_var = StringVar()
            project_label = Label(self.ship_proj_frame, text='|Project Number|')
            project_entry = Entry(self.ship_proj_frame, textvariable=self.project_var)

            project_label.grid(row=5, column=0, columnspan=2, sticky=W)
            project_entry.grid(row=6, column=0, columnspan=2, ipadx=30)

            self.window_q = False


        self.ship_to_var = StringVar()

        self.ship_to_text = Text(self.ship_proj_frame, height=3, width=23)
        self.ship_to_text.grid(row=4, column=0, columnspan=2)

        self.igs_var = BooleanVar(value=False)
        self.igs_checkbox = Checkbutton(
            self.ship_proj_frame,
            text='IGS Packing Slip?',
            variable=self.igs_var,
            command=self.IGSCombos
        )

        # for ^ checkbutton , onvalue = value, offvalue = value,

        self.igs_checkbox.grid(row=7, column=0)

        self.createWidgets()


    def createWidgets(self):
        # add_sub_label = Label(self.add_sub_frame, text='|Add or Sub Line|')
        # add_sub_label.grid(row=0, column=0)

        add_butt = Button(self.add_sub_frame, text='+', command=self.CreateNewLine)
        add_butt.grid(row=0, column=0, sticky=W)

        sub_butt = Button(self.add_sub_frame, text='-', command=self.DeleteLastLine)
        sub_butt.grid(row=0, column=1, sticky=E)

        open_inventory_butt = Button(self.ship_proj_frame, text='Open IGS File', command=self.OpenInv)
        open_inventory_butt.grid(row=7, column=1)

        # ship_to_label = Label(self.ship_proj_frame, text='|Ship To|')
        # ship_to_label.grid(row=3, column=0)




        submit_butt = Button(self.ship_proj_frame, text='Submit/Generate', command=self.GetLinesAndSubmit)
        submit_butt.grid(row=8, column=0, columnspan=2)

        self.CreateNewLine()


    def CreateNewLine(self):
        self.line_count += 1
        print(f'<{__name__}> Creating Line at row {self.line_count + 1}')

        new_line = ALine(self.input_frame, self.line_count, self.igs_items, self.igs_var.get())
        self.line_list.append(new_line)


    def DeleteLastLine(self):
        if self.line_count == 0:
            print(f'<{__name__}> Min number of lines reached')
            messagebox.showwarning("No Can Do", "You can't do that homie. You only have one line left")
            return
        self.line_count -= 1

        self.line_list[-1].Delete()
        self.line_list.pop()


    def IGSCombos(self):

        checked_q = self.igs_var.get()
        # if checked_q:
        #     self.igs_var.set(False)
        #     checked_q = False
        # else:
        #     self.igs_var.set(True)
        #     checked_q = True
        #
        print(f'<{__name__}> IGS Toggle: {checked_q}')

        for line in self.line_list:
            line.ComboEntrySwitch(checked_q)


    def GetLinesAndSubmit(self):
        item_lst = []
        qty_list = []

        if not self.project_butt:
            project_got = self.project_var.get()

        else:
            project_got = self.project_butt

        ship_to = self.ship_to_text.get("1.0", "end")

        for line_class in self.line_list:
            output = line_class.GetLine()
            print(f"<{__name__}> Line Added: {output}")

            item_lst.append(output[0])
            qty_list.append(output[1])

        igs_q = self.igs_var.get()

        print(f"<{__name__}> Shipping: {ship_to}")

        if self.CheckIfEmpty(item_lst, qty_list, ship_to, project_got):
            return

        first_exit_q = CreateProjectDocument(project_got, 'D2-7 - Packing Slip')

        if igs_q:
            submit_igs_junk = IGS_Generate_Update_Logs(
                shipping_loc=ship_to,
                proj=project_got,
                itms=item_lst,
                qtys=qty_list
            )

            exit_q = submit_igs_junk.CheckandUpdate()

            if exit_q:
                return

        if not igs_q:
            packing_slip_loc = f'Projects\\{project_got}\\D2-7-{project_got} - Packing Slip.xlsx'

            AddDataToExcel(
                excel_loc=packing_slip_loc,
                sheet_name='INPUT',
                col_loc=[2, 3, 4],
                row_list_data=[ship_to, item_lst, qty_list],
                place_loc=(0, 0),
                scan_min=(0, 0),
                scan_max=(20, 5)
            )

            now = datetime.now()
            year = now.year

            general_year_po_loc = f"Finance\\Yearly_Packing_Slips\\{year}"
            ps_year_loc = f"{general_year_po_loc}\\D2-7-{project_got} - Packing Slip.xlsx"

            if not path.isdir(general_year_po_loc):
                mkdir(general_year_po_loc)

                copyfile(packing_slip_loc, ps_year_loc)

        for line_class in self.line_list:
            line_class.Delete()
            # input_frame = line_class.GiveFrameData()
            # for widget in input_frame.winfo_children():
            #     widget.destroy()
            #
            # input_frame.destroy()

        self.ship_to_text.delete('1.0', END)

        self.line_list = []
        self.line_count = -1
        self.CreateNewLine()

        if self.window_q:
            self.destroy()
            self.destrou_top_level.destroy()
        else:
            self.project_var.set('')

    def CheckIfEmpty(self, item_lst, qty_list, ship_to, project_got):
        # print(f'Quantity {qty_list}, item_lst {item_lst}')
        for j, item, qty in zip(range(0, len(item_lst)), item_lst, qty_list):
            if item == '':
                messagebox.showwarning(title='Nuh uh, my dude:Empty Item', message=f'Missing item in line {j + 1}, my man')
                return True

            if str(qty) == '':
                messagebox.showwarning(title='Sorry Brosive: Empty Quantitty', message=f'Missing quantity in line {j + 1}, Slick')
                return True
            elif not qty.isdigit():
                messagebox.showwarning(title='My hommie... Incorrect Quantitty', message=f'Must be a number on line {j + 1}\n you know what a number is???')
                return True

        if ship_to == '\n':
            messagebox.showwarning(
                title='REALLY????? Empty Shipping Location',
                message=f"Missing shipping information... You don't know where this is going? SMH"
            )
            return True

        if project_got == '':
            messagebox.showwarning(
                title='Empty Quantitty... heh titty ;)',
                message=f'Missing project number, my man. Make sure you check closer next time'
            )
            return True


    def OpenInv(self):
        startfile(self.inv_file_loc)

class ALine:

    def __init__(self, parent, l_num, igs_data, igs_q):
        super().__init__()
        self.inside_of = parent
        self.line_num = l_num
        # print(self.line_num)
        self.igs_item_list = igs_data

        self.line_frame = Frame(self.inside_of)
        self.line_frame.grid(row=1 + self.line_num, column=1, sticky=N)

        self.item_var = StringVar(value=igs_data)
        self.quantitty_var = StringVar()

        if igs_q:
            self.item_text_bx = Combobox(self.line_frame, textvariable=self.item_var, values=self.igs_item_list)
            self.item_text_bx.set('')

        if not igs_q:
            self.item_text_bx = Entry(self.line_frame, textvariable=self.item_var)
            self.item_text_bx.delete(0, END)

        self.MakeLine()


    def MakeLine(self):
        # condition to only put the column names go into the first line
        if self.line_num == 0:
            line_label = Label(self.line_frame, text='|Ln.|')
            item_label = Label(self.line_frame, text='|Item|')
            quatiddy_label = Label(self.line_frame, text='|Quantity|')
            line_label.grid(row=0, column=0, sticky=NW)
            item_label.grid(row=0, column=1, sticky=N)
            quatiddy_label.grid(row=0, column=2, sticky=N)

        label_ln_num = Label(self.line_frame, text=f'{self.line_num + 1}   -   ')

        quantitty_text_bx = Entry(self.line_frame, textvariable=self.quantitty_var)


        label_ln_num.grid(row=1, column=0)
        self.item_text_bx.grid(row=1, column=1)
        quantitty_text_bx.grid(row=1, column=2)


    def Delete(self):
        for widget in self.line_frame.winfo_children():
            widget.destroy()

        self.line_frame.destroy()

    def GetLine(self):
        item = self.item_var.get()
        qtty = self.quantitty_var.get()

        return item, qtty

    def GiveFrameData(self):
        return self.line_frame

    def ComboEntrySwitch(self, igs_q):
        if igs_q:
            self.item_text_bx.destroy()
            self.item_text_bx = Combobox(self.line_frame, textvariable=self.item_var, values=self.igs_item_list)
            self.item_text_bx.set('')
            self.item_text_bx.grid(row=1, column=1)
        elif not igs_q:
            self.item_text_bx.destroy()
            self.item_text_bx = Entry(self.line_frame, textvariable=self.item_var)
            self.item_text_bx.grid(row=1, column=1)
