from tkinter import StringVar, BooleanVar, IntVar, messagebox, N, W, E, S, NW, Text, END, Checkbutton
from tkinter.ttk import Frame, Radiobutton, Label, Entry, Button, Combobox, LabelFrame

from general_funcs import AddDataToExcel, GetVar
from igs_funcs import LoadData, GoToTracking, IGS_Generate_Update_Logs


class PackingSlipPage(Frame):
    GoToTracking()

    def __init__(self, master=None, from_project=False, top_level=None):
        super().__init__(master)
        self.grid()

        self.destrou_top_level = top_level

        igs_shtuff = GetVar('Python_Source\!variables\igs_tracking_var.txt', False)
        list_thang = LoadData(igs_shtuff[2])
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

            project_label.grid(row=5, column=0, sticky=W)
            project_entry.grid(row=6, column=0, ipadx=30)

            self.window_q = False


        self.ship_to_var = StringVar()

        self.ship_to_text = Text(self.ship_proj_frame, height=3, width=23)
        self.ship_to_text.grid(row=4, column=0)

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

        # ship_to_label = Label(self.ship_proj_frame, text='|Ship To|')
        # ship_to_label.grid(row=3, column=0)




        submit_butt = Button(self.ship_proj_frame, text='Submit/Generate', command=self.GetLinesAndSubmit)
        submit_butt.grid(row=8, column=0)

        self.CreateNewLine()


    def CreateNewLine(self):
        self.line_count += 1
        print(f'Creating Line at row {self.line_count + 1}')

        new_line = ALine(self.input_frame, self.line_count, self.igs_items, self.igs_var.get())
        self.line_list.append(new_line)


    def DeleteLastLine(self):
        if self.line_count == 0:
            print('Min number of lines reached')
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
        print(f'IGS Toggle{checked_q}')

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
            print(output)

            item_lst.append(output[0])
            qty_list.append(output[1])

        igs_q = self.igs_var.get()

        print(ship_to)

        if self.CheckIfEmpty(item_lst, qty_list, ship_to, project_got):
            return

        for line_class in self.line_list:
            line_class.Delete()
            # input_frame = line_class.GiveFrameData()
            # for widget in input_frame.winfo_children():
            #     widget.destroy()
            #
            # input_frame.destroy()


        if igs_q:
            submit_igs_junk = IGS_Generate_Update_Logs(
                shipping_loc=ship_to,
                proj=project_got,
                itms=item_lst,
                qtys=qty_list
            )

            submit_igs_junk.CheckandUpdate()
        if not igs_q:
            packing_slip_loc = f'Projects\\{project_got}\\D2-7.0-{project_got} - Packing Slip.xlsx'

            AddDataToExcel(
                excel_loc=packing_slip_loc,
                sheet_name='INPUT',
                col_loc=[2, 3, 4],
                row_list_data=[ship_to, item_lst, qty_list],
                place_loc=(0, 0),
                scan_min=(0, 0),
                scan_max=(20, 5)
            )

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