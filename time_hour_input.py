import widgets
from appending_funcs import append_df_to_excel
from globalz import general_file_loc

from os import listdir, path, getcwd, remove, mkdir
from datetime import datetime, timedelta
from tkinter import Frame, Radiobutton, StringVar, messagebox, Canvas, Toplevel, Entry, Label
from tkinter.messagebox import askyesno
from tkinter.ttk import Button
from csv import writer
from pandas import read_csv, DataFrame, ExcelWriter
from openpyxl import load_workbook
from calendar import month_name
from shutil import copyfile
from PIL import ImageTk, Image



def daterange(start_date, end_date):
    for n in range(int(1 + (end_date - start_date).days)):
        yield start_date + timedelta(n)



def forward():
    getDateStringandRange('f', True)


def backward():
    getDateStringandRange('b', True)


def getDateStringandRange(back_forwards_q=None, update_label_q=False):
    global date_list, pivot_weds, second_thurs, date_offset, week

    # if the forwards button is pressed
    if back_forwards_q == 'f':
        date_offset = timedelta(days=7) + date_offset
        pivot_weds = (date_offset.strftime("%m/%d/%Y"), date_offset)

    # default or backwards button
    if back_forwards_q == 'b':
        date_offset = timedelta(days=-7) + date_offset
        pivot_weds = (date_offset.strftime("%m/%d/%Y"), date_offset)

    # getting the date 7 days before or after depending on which button is pressed or 7 days after for default
    second_offset = timedelta(days=-6) + pivot_weds[1]
    second_thurs = (second_offset.strftime("%m/%d/%Y"), second_offset)

    print(f'<{__name__}> Current Pay Week: {second_thurs[0]} - {pivot_weds[0]}')

    date_list = []
    for single_date in daterange(second_thurs[1], pivot_weds[1]):
        date_list.append((single_date.strftime("%m/%d/%Y"), single_date))

    week = str(second_thurs[0]) + '-' + str(pivot_weds[0])

    if update_label_q:
        label_list['Action Frame'][0].info['text'] = week

        for w, line in enumerate(line_list):
            line.updateDateLabel(date_list[w][0])


    # print(date_list)

def getWorkerList():
    global worker_list
    worker_list = listdir('Workers')
    worker_list.pop(0)


large_font = ("Verdana", 20)
smol_font = ("Verdana", 12)
tiny_font = ("Verdana", 8)
job_lst = [
    'Deburring',
    'Burn Table',
    'Assembly',
    'Fitting',
    'Drafting',
    'Forming',
    'Saw',
    'Welding',
    'Paint Prep',
    'Paint',
    'Janitoral',
    'Maintenance',
    'Trucks',
    'HELPER',
    'Mockup, Test',
    'Shipping Prep',
    'Machining',
    'Management',
    'Inspection',
    'Drive'
]
hour_lst = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10"
]

width = 1100
height = 750

worker_list = []

label_list = {'Action Frame': []}
button_list = {'Action Frame': []}
date_list = []
line_list = []
week = None

today = datetime.today()
day_o_week = today.weekday()

# calculating day offset (Thursday is 3rd day of the week)
current_day_dif = 2 - day_o_week
# getting date at that offset
date_offset = timedelta(days=current_day_dif) + today
pivot_weds = (date_offset.strftime("%m/%d/%Y"), date_offset)
second_thurs = (0, 0)
getDateStringandRange()

# print(f'{today}, {day_o_week}, \n{pirvot_thurs}')

getWorkerList()

print(f"<{__name__}> Worker List:{worker_list}\n~~~~~~~~~~~~~~~~~~~~~~~\n")


# main window for the GUI
class Window(Toplevel):
    def __init__(self):
        super().__init__()
        self.major_frame = Frame(self)
        self.major_frame.grid()


        self.width = width
        self.height = height
        self.action_frame_w = self.width * .25
        self.input_frame_w = self.width * .75
        self.bg = 'black'

        self.button_margin = .9

        self.wsr = []

        self.working_file = general_file_loc[0] + '\\temp_time_hour_input.csv'
        self.worker_first_row = ['Date', 'Project', 'Job', 'Time Spent']
        self.first_row = ['Date', 'Job', 'Time', 'Name']

        self.title('Weekly Time Hour Input')
        self.geometry(str(self.width) + 'x' + str(self.height))

        self.logo_path = general_file_loc[0] + '\\' + general_file_loc[4]
        self.img = Image.open(self.logo_path)
        self.re_img = self.img.resize((int(round(self.action_frame_w)), int(round(self.height * .19))))
        self.logo_object = ImageTk.PhotoImage(self.re_img)

        self.draw()

    # the initial creation and storage of the beginning widgets
    def draw(self):
        # holds the week selector, worker selector, submit button, and release button
        action_frame = Frame_(
            master=self,
            frame_width=self.action_frame_w,
            frame_height=self.height,
            x_loc=0,
            y_loc=0,
            g_or_p='p',
            bg_color='black'
        )
        input_frame = Frame_(
            master=self,
            frame_width=self.input_frame_w,
            frame_height=self.height,
            x_loc=.25,
            y_loc=0,
            g_or_p='p',
            bg_color='black'
        )

        # for creating the week chooser frame
        self.dateSelector(action_frame.info)
        # print(action_frame.info)
        # for the worker selector, submit, and release button (Maybe add clear button)
        self.WSR(action_frame.info)
        # for the entrie lines
        self.inputWidgets(input_frame.info)


        # label_list['Action Frame'].append(widgets.Label_(master=self.master, text='text', font=large_font, x_loc=self.width/2, y_loc=self.height/2))

        # button = widgets.Button_(master=self.master, text='BOOP', font=large_font, x_loc=50, y_loc=50, func=move)
        # button.create()


    def dateSelector(self, action_frame):
        # getting proper formatting sizes
        date_frame_width = self.action_frame_w
        date_frame_height = self.height * .1

        # creating week selector frame
        date_sel_frame = Frame_(
            master=action_frame,
            frame_width=date_frame_width,
            frame_height=date_frame_height,
            x_loc=0,
            y_loc=.2,
            g_or_p='p',
            bg_color='white'
        )

        # creating current week label
        label_list['Action Frame'].append(
            widgets.Label_(
                master=date_sel_frame.info,
                text=week,
                font=smol_font,
                x_loc=.5,
                y_loc=0
            )
        )
        # creating buttons
        prev_week = widgets.Button_(
            master=date_sel_frame.info,
            text='<',
            font=smol_font,
            width=(self.action_frame_w/2) * self.button_margin,
            x_loc=.25,
            y_loc=.4,
            func=backward
        )

        next_week = widgets.Button_(
            master=date_sel_frame.info,
            text='>',
            font=smol_font,
            width=(self.action_frame_w/2) * self.button_margin,
            x_loc=.75,
            y_loc=.4,
            func=forward
        )

    def WSR(self, action_frame):
        # label_logo = widgets.Label(action_frame, image=self.logo_object)
        # label_logo.image = self.logo_object
        # label_logo.place(x=0, y=0)
        # action_frame.image = self.img

        canvas = Canvas(action_frame, width=self.action_frame_w, height=self.height * .18)
        canvas.place(x=0, y=0, anchor='nw')

        canvas.create_image(0, 0, anchor='nw', image=self.logo_object)

        worker_selector_dd = widgets.DropDown(
            master=action_frame,
            font=smol_font,
            values=worker_list,
            x_loc=.5,
            y_loc=.35,
        )

        self.wsr.append(worker_selector_dd)

        submit_button = widgets.Button_(
            master=action_frame,
            text='Submit',
            font=smol_font,
            width=self.action_frame_w * self.button_margin,
            x_loc=.5,
            y_loc=.4,
            func=lambda: self.Submit()
        )

        release_button = widgets.Button_(
            master=action_frame,
            text='Release',
            font=smol_font,
            width=self.action_frame_w * self.button_margin,
            x_loc=.5,
            y_loc=.45,
            func=lambda: self.Release()
        )


    def inputWidgets(self, input_frame):
        # project_num_frame = Frame_(input_frame, self.input_frame_w * .25, self.height, 0, 0, 'grey')
        # job_type_frame = Frame_(input_frame, self.input_frame_w * .25, self.height, .25, 0, 'white')
        # time_frame = Frame_(input_frame, self.input_frame_w * .25, self.height, .5, 0, 'grey')
        # time_q_frame = Frame_(input_frame, self.input_frame_w * .25, self.height, .75, 0, 'white')

        for i, day in enumerate(date_list):
            # if i != 0:
            #     break
            # print(day[0], i)

            line_list.append(DayofWeekLine(input_frame, day, i))

    def Submit(self):
        answer = askyesno(
            title="Submit?",
            message="Submit lines with project number to 'working.csv' \n(Click no to CANCEL)"
        )
        if not answer:
            return

        column_list = ['Date', 'Worker Name', 'Project Number', 'Job Type', 'Hours']
        # testing if the working file exists and adding the first line if it does not
        fileee = path.exists(self.working_file)
        # print(fileee)

        worker = self.wsr[0].info.get()
        # testing if worker is filled in
        if worker == '':
            wo = f'Missing Worker Info'
            # print(wo)
            messagebox.showerror(title='Error', message=wo)
            return
        # testing to see if there are any bits of missing info with project numbers filled in
        for line, day in zip(line_list, date_list):
            for j, entry in enumerate(line.entries_storage):
                project_num = entry[1].info.get()
                job_type = entry[2].info.get()
                time_hour = entry[3].info.get()
                time_q = entry[4][0].get()

                if project_num != '':
                    if job_type == '':
                        jt = f'Missing Job Type Info for {day[0]}'
                        print(f'<{__name__}> {jt}')
                        messagebox.showerror(title='Error', message=jt)
                        return
                    elif time_hour == '':
                        th = f'Missing Time Hour Info for {day[0]}'
                        print(f'<{__name__}> {th}')
                        messagebox.showerror(title='Error', message=th)
                        return
                    elif time_q == ' ' or time_q == '':
                        print(f'<{__name__}> {time_q}')
                        tq = f'Missing Time Hour Quarter Info for {day[0]}'
                        print(f'<{__name__}> {tq}')
                        messagebox.showerror(title='Error', message=tq)
                        return

        # if every entry has all of its info
        with open(self.working_file, 'a+', newline='') as write_obj:
            for line, day in zip(line_list, date_list):
                for j, entry in enumerate(line.entries_storage):
                    num_of_entries = len(line.entries_storage)

                    project_num = entry[1].info.get()
                    job_type = entry[2].info.get()
                    time_hour = entry[3].info.get()
                    time_q = entry[4][0].get()

                    # if the last line is empty, refreshing the entries other than the first
                    if project_num == '':
                        print(f'<{__name__}> Skipped Blank in {day[0]}')
                        if num_of_entries == j + 1 and num_of_entries != 1:
                            for l in range(0, num_of_entries):
                                line.DeleteEntryLine()
                        continue



                    print(f'<{__name__}> Submitting: Worker:{worker}, Date:{day[0]}, PN:{project_num}, JT:{job_type}, TH:{int(time_hour)}, TQ:{len(time_q), time_q}')

                    time_total = int(time_hour) + (.01 * int(time_q))

                    temp_row = [day[0], worker, project_num, job_type, time_total]

                    csv_writer = writer(write_obj)
                    if not fileee:
                        csv_writer.writerow(column_list)
                        fileee = True

                    csv_writer.writerow(temp_row)

                    # refreshing the first entry of the input space
                    # print(num_of_entries)
                    if num_of_entries == j + 1:
                        pass
                        for l in range(0, num_of_entries):
                            line.DeleteEntryLine()
                        # print(line.entries_storage)

                        # line.entries_storage[0][1].info.delete(0, 'end')
                        # line.entries_storage[0][2].info.set('')
                        # line.entries_storage[0][3].info.set('')
                        # line.entries_storage[0][4][0].set(value='')


    def Release(self):
        # ask to make sure it is okay to release
        answer = askyesno(
            title='Release and Delete',
            message='Are you sure that you want to release the submitted data and delete working cache? \n\n'
                    'THIS CANNOT BE UNDONE \n'
                    '(It is recommended to double check ' + self.working_file + ') \n\n'
                    'Click No to go back'
        )
        if not answer:
            return

        # reading it the entire contents to a .csv
        df = read_csv(self.working_file, index_col=False)
        print("<{__name__}> \nData Released:\n")

        projects_to_update = []

        for rando, row in df.iterrows():
            # generating the array
            release_temp = [row['Date'], row['Worker Name'], row['Project Number'], row['Job Type'], row['Hours']]



            # folder and file locations
            project = str(release_temp[2])
            folder_path = r'Projects\\' + project
            project_pathcsv = folder_path + r'\\!src\\' + project + '.csv'
            project_pathxlsx = folder_path + r'\\' + project + '-master.xlsx'

            add_q = True
            for proj in projects_to_update:
                if project == proj:
                    add_q = False
            if add_q:
                projects_to_update.append(project)

            # writing to the worker csv
            self.csvWorkerWrite(release_temp)
            # writing to the project csv
            self.csvProjectWrite(release_temp, folder_path, project_pathxlsx, project_pathcsv)
            # # ---putting the data in the project csv into the project xlsx for visualization---
            # # pulling the data from the csv
            # temp_data = read_csv(project_pathcsv)
            # # putting it into a dataframe for easy input into the excel
            # df_src_csv = DataFrame(temp_data)
            # # grabbing the last/most recent data point
            # last = df_src_csv.tail(1)
            #
            # append_df_to_excel(
            #     project_pathxlsx,
            #     df=last,
            #     sheet_name=str(release_temp[2]) + "_dataSheet",
            #     startcol=0,
            #     index=False
            # )
            #
            # # append_df_to_excel(project_pathxlsx, last, )

        for unloaded_proj in projects_to_update:
            folder_path_2 = r'Projects\\' + unloaded_proj
            master_excel = folder_path_2 + r'\\' + unloaded_proj + '-master.xlsx'
            sheet_name = f'{unloaded_proj}_dataSheet'
            src_csv = folder_path_2 + r'\\!src\\' + unloaded_proj + '.csv'

            book = load_workbook(master_excel)
            writer_boi = ExcelWriter(master_excel, engine='openpyxl')
            writer_boi.book = book

            std = book.get_sheet_by_name(sheet_name)
            book.remove_sheet(std)

            df = read_csv(src_csv)

            df.to_excel(writer_boi, sheet_name=sheet_name, index=False)

            # save and close
            writer_boi.save()

        remove(self.working_file)


    def csvWorkerWrite(self, release_temp):
        # put info in proper format
        worker_csv_input = [release_temp[0], release_temp[2], release_temp[3], release_temp[4]]

        # getting the month for proper yearly, month data storage
        month_input = str(worker_csv_input[0])
        month_num = month_input.partition('/')
        month = month_name[int(month_num[0])]

        worker_month_folder = 'Workers\\' + str(release_temp[1]) + '\\' + month + '.csv'
        print(f"<{__name__}> Writing to Worker: {worker_month_folder} \nInputting:")

        first_line_add = False
        if not path.isfile(worker_month_folder):
            first_line_add = True

        # writing the new data to the specific worker file
        with open(worker_month_folder, 'a+', newline='') as write_obj:
            csv_writer = writer(write_obj)

            if first_line_add:
                csv_writer.writerow(self.worker_first_row)
            print(f"<{__name__}> {worker_csv_input}")
            csv_writer.writerow(worker_csv_input)

        return

    def csvProjectWrite(self, release_temp, folder_path, project_pathxlsx, project_pathcsv):
        # put info in proper format
        project_csv_input = [release_temp[0], release_temp[3], release_temp[4], release_temp[1]]
        project = str(release_temp[2])

        src_folder = folder_path + '\\!src'

        first_line_test = False

        # creating src folder
        if not path.isdir(src_folder):
            # TRUE if the csv file is new and needs the first_row
            first_line_test = True

            print(f"<{__name__}> {project}: Made src Folder")
            mkdir(src_folder)

        # if the project source file does not exist
        if not path.isfile(project_pathcsv):
            first_line_test = True

        with open(project_pathcsv, 'a+', newline='') as write_obj:
            # create writer object
            csv_writer = writer(write_obj)

            if first_line_test:
                csv_writer.writerow(self.first_row)

            csv_writer.writerow(project_csv_input)


# class for creating different types of frames
class Frame_(Frame):
    def __init__(self, master, frame_width, frame_height, x_loc, y_loc, g_or_p, bg_color, rowspan=1, sticky='W', **kw):
        super().__init__(master, **kw)

        self.master = master
        self.info = None
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.g_or_p = g_or_p
        self.bg_color = bg_color
        self.rowspan = rowspan
        self.sticky = sticky

        self.create()

    def create(self):
        self.info = Frame(
            master=self.master,
            width=self.frame_width,
            height=self.frame_height,
            bg=self.bg_color
        )
        if self.g_or_p == 'g':
            self.info.grid(
                column=self.x_loc,
                row=self.y_loc,
                rowspan=self.rowspan,
                sticky='W'
            )
        elif self.g_or_p == 'p':
            self.info.place(
                relx=self.x_loc,
                rely=self.y_loc
            )

    def update_(self):
        self.info.destroy()
        self.info = Frame(
            master=self.master,
            width=self.frame_width,
            height=self.frame_height,
            bg='black'
        )
        if self.g_or_p == 'g':
            self.info.grid(
                column=self.x_loc,
                row=self.y_loc,
                rowspan=self.rowspan,
                sticky='W'
            )
        elif self.g_or_p == 'p':
            self.info.place(
                relx=self.x_loc,
                rely=self.y_loc
            )


# class for each day of the week
class DayofWeekLine:
    def __init__(self, input_frame, line_day, line_num, **kw):
        super().__init__(**kw)
        # self.project_num_f_info = project_num_f_info
        # self.job_type_f_info = job_type_f_info
        # self.time_f_info = time_f_info
        # self.time_q_f_info = time_q_f_info

        self.line_height = .2
        # index start at 0 (line 1 = 0)
        self.line_entries = 0
        self.entries_storage = []


        self.input_frame = input_frame
        self.line_day = line_day
        self.line_num = line_num
        self.text_var = widgets.StringVar()

        if line_num % 2 == 1:
            self.color = "black"
        else:
            self.color = "grey"

        self.line_frame = Frame_(
            master=self.input_frame,
            frame_height=height * self.line_height,
            frame_width=width * .75,
            x_loc=0,
            y_loc=line_num,
            g_or_p='g',
            bg_color=self.color,
            sticky='W'
        )

        self.info = self.line_frame.info
        self.info['padx'] = 10
        self.info['pady'] = 10

        self.dateline = self.dateLabel()
        self.updateDateLabel(self.line_day[0])

        # add entries to line buttons
        sub_entry_button = widgets.Button_(
            master=self.info,
            text='-',
            font=smol_font,
            width=40,
            x_loc=0,
            y_loc=1,
            g_or_p='g',
            func=lambda: self.DeleteEntryLine()
        )
        add_entry_button = widgets.Button_(
            master=self.info,
            text='+',
            font=smol_font,
            width=40,
            x_loc=1,
            y_loc=1,
            g_or_p='g',
            func=lambda: self.generateLine()
        )

        # generate the entries
        #self.generateLine()

    def dateLabel(self):

        date_line = widgets.Label(
            master=self.info,
            textvariable=self.text_var,
            font=smol_font,
        )

        date_line.grid(
            column=0,
            row=0,
            columnspan=2
        )

        return date_line

    def updateDateLabel(self, text_var):
        self.text_var.set(text_var)

    def timeQButts(self, entry_frame):
        choosen = StringVar(value=0)
        r0 = Radiobutton(
            entry_frame.info,
            text='.00',
            font=tiny_font,
            variable=choosen,
            value=0,
            indicatoron=0
        )
        r25 = Radiobutton(
            entry_frame.info,
            text='.25',
            font=tiny_font,
            variable=choosen,
            value=25,
            indicatoron=0
        )
        r50 = Radiobutton(
            entry_frame.info,
            text='.50',
            font=tiny_font,
            variable=choosen,
            value=50,
            indicatoron=0
        )
        r75 = Radiobutton(
            entry_frame.info,
            text='.75',
            font=tiny_font,
            variable=choosen,
            value=75,
            indicatoron=0
        )
        r0.grid(
            column=5,
            row=0
        )
        r25.grid(
            column=6,
            row=0
        )
        r50.grid(
            column=5,
            row=1,
            pady=(0, 5)
        )
        r75.grid(
            column=6,
            row=1,
            pady=(0, 5)
        )
        radios = (r0, r25, r50, r75)
        return choosen, radios

    def generateLine(self):
        entry_frame = Frame_(
            master=self.info,
            frame_height=50,
            frame_width=width * .75,
            x_loc=2,
            y_loc=self.line_entries * 2,
            g_or_p='g',
            bg_color=self.color,
            rowspan=2
        )

        entry_line = widgets.InputBoxes(
            master=entry_frame.info,
            text=self.line_day,
            font=smol_font,
            x_loc=2,
            y_loc=0,
        )

        job_type_dd = widgets.DropDown(
            master=entry_frame.info,
            font=smol_font,
            values=job_lst,
            x_loc=3,
            y_loc=0,
            g_or_p='g'
        )

        time_dd = widgets.DropDown(
            master=entry_frame.info,
            font=smol_font,
            values=hour_lst,
            x_loc=4,
            y_loc=0,
            g_or_p='g'
        )

        chosen, radios = self.timeQButts(entry_frame)

        self.entries_storage.append((entry_frame, entry_line, job_type_dd, time_dd, (chosen, radios)))
        self.line_entries += 1


    def DeleteEntryLine(self):
        if self.line_entries == 0:
            print(f'<{__name__}> Min Number of Entries {self.line_entries}')
            return False

        self.line_entries -= 1

        entry_frame_info = self.entries_storage[self.line_entries][0].info

        # print(f'le:{self.line_entries}, {self.entries_storage[self.line_entries]}')

        # the last entry in the line, getting rid of
        for widget in entry_frame_info.winfo_children():
            widget.destroy()

        entry_frame_info.destroy()
        self.entries_storage.pop()

        return True

    def getAllEntries(self):
        pass


def TimeHourInput():

    app = Window()
    app.config(bg='black')


def AddWorker():
    temp_po_tk = Toplevel()
    temp_po_tk.title('Add Worker')
    test_frame = Frame(temp_po_tk)
    test_frame.grid()

    label_direction = Label(test_frame, text='Enter Worker Name')
    label_direction.grid(row=0)

    vendor_var = StringVar(temp_po_tk)
    vendor_var.set('eg: Spng. Bob')

    vendor_entry = Entry(test_frame, textvariable=vendor_var)
    vendor_entry.grid(row=1)

    def make_dir():
        worker = vendor_var.get()
        mkdir(f"Workers\\{worker}")
        temp_po_tk.destroy()
        messagebox.showinfo("Worker Added", f"Worker, {worker}, Added. Woot!!!")

    sub_butt = Button(test_frame, text='Confirm', command=make_dir)
    sub_butt.grid(row=2)


