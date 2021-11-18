from tkinter import StringVar, Canvas, messagebox, N, W, E, S, NSEW, Tk, Scrollbar, Toplevel
from tkinter.ttk import Frame, Label, Entry, Button, LabelFrame, Combobox, Style

from os import startfile, listdir, path
from shutil import copyfile
from time import sleep

from nb_purchase_input import PurchaseInputPage
from nb_packing_slip import PackingSlipPage
from general_funcs import AddDataToExcel
from new_project import CreateNewProject


def OpenProject(project=None):
    # if the project number is not supplied when the function is called
    if project is None:
        # create a mini-window
        open_proj = Tk()
        #
        entry = Entry(open_proj)

    # inner function
    def openOpenProject(event=None, skip_destroy=None):
        proj = entry.get()
        proj_path = f'Projects\\{proj}'
        startfile(proj_path)
        # if the window was made, destroying it
        if skip_destroy is None:
            open_proj.destroy()
        return
    # if the project number is supplied when the outter function is called
    if project is not None:
        # making the given project number a string var so that the same inner function can be used
        entry = StringVar(value=str(project))
        # calling inner function and skipping the destroying part since the window wasn't made
        openOpenProject(skip_destroy=True)
        # skipping junk below since the innter funtion wasn't called
        return

    question_label = Label(open_proj, text="Enter Project number below\n"
                                           "Press Open to open Projects folder")

    confirm_butt = Button(open_proj, text='Open', command=openOpenProject)
    open_proj.bind('<Return>', openOpenProject)

    question_label.grid(row=0, column=0)
    entry.grid(row=1, column=0)
    confirm_butt.grid(row=2, column=0)


def CreateProjectDocument(project, doc):
    print(f'Creating document {doc} for project {project}')
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

        if doc == 'D2-7.0 - Packing Slip':
            temp_ps_tk = Toplevel()
            temp_ps_tk.title('ps_pop_up')
            test_frame = Frame(temp_ps_tk)
            test_frame.grid()
            temp_slip = PackingSlipPage(master=test_frame, from_project=project, top_level=temp_ps_tk)
            temp_slip.grid()


        if doc == 'D2-4.0 - Purchase Order':
            temp_po_tk = Toplevel()
            temp_po_tk.title('po_pop_up')
            test_frame = Frame(temp_po_tk)
            test_frame.grid()
            temp_slip = PurchaseInputPage(master=test_frame, from_project=project, top_level=temp_po_tk)
            temp_slip.grid()





    else:
        create_new_proj = messagebox.askquestion(
            f'{project} Does Not Exist, bruv',
            f'{project} does not exist. Would you like to create that project, homie?'
        )
        if create_new_proj:
            project = CreateNewProject()
            CreateProjectDocument(project, doc)
        else:
            return


def GetDocList():
    file_list = []
    loc_list = ['D2 - Documentation', 'D3 - Manufacturing']
    for file_option in loc_list:
        given_dir = f'Quality_Control\\!D - Documents\\{file_option}'

        file_list.extend(listdir(given_dir))

    # print(file_list)

    for i, item in enumerate(file_list):
        if item[-5] == '.' and item[:2] != '~$':
            file_list[i] = item[:-5]
        else:
            file_list.pop(i)

    # print(file_list)

    return file_list


class ScrollableFrame(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.config(height=500, width=600)
        canvas = Canvas(self, height=500, width=500)
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
        canvas.grid(row=0, column=0, sticky=W)
        scrollbar.grid(row=0, column=1, sticky=N+S+E)


class ProjectBrowser(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.create_widgets()

        self.scrolls_frame_lst = []

    def create_widgets(self):
        """Create the widgets for the GUI"""
        scrolls = ScrollableFrame(self)
        scrolls.grid(row=0, column=0, sticky=NSEW)

        refresh_butt = Button(self, text='⟳', command=lambda: self.RefreshScroll(scrolls), width=3)
        refresh_butt.grid(row=0, column=1, sticky=N)

        self.RefreshScroll(scrolls)


    def RefreshScroll(self, scrolls):
        proj_list = listdir('Projects')
        doc_list = GetDocList()

        for given_proj_frame in scrolls.scrollable_frame.winfo_children():
            given_proj_frame.destroy()

        for i, proj in enumerate(proj_list):
            ProjLineClass(scrolls, doc_list, proj, i)


            # doc_create_selector = Frame()

def CreateDocCommand():
    parent_flabel_pad = (5, 5)

    creat_doc_win = Toplevel()
    doc_list = GetDocList()
    proj_list = listdir('Projects')
    print(f'Here {proj_list}')

    doc_label = LabelFrame(creat_doc_win, text='|Choose Doc|', padding=parent_flabel_pad)
    doc_label.grid(row=0, column=0)
    doc_var = StringVar()
    doc_choice = Combobox(doc_label, state="readonly", textvariable=doc_var, values=doc_list)
    doc_choice.config(width=30)
    doc_choice.grid(row=1, column=0)

    proj_label = LabelFrame(creat_doc_win, text='|Choose Project|', padding=parent_flabel_pad)
    proj_label.grid(row=2, column=0)
    proj_var = StringVar()
    proj_choice = Combobox(proj_label, state="readonly", textvariable=proj_var, values=proj_list)
    proj_choice.config(width=30)
    proj_choice.grid(row=3, column=0)

    def Submit():
        project = proj_var.get()
        doc = doc_var.get()
        if project == 'Select Project':
            messagebox.showwarning("SMH...Error", 'Come on man... Choose a project')
        if doc == 'Choose Project':
            messagebox.showwarning('Bruv...Error', "You couldn't pic a document? It is soooo ez pz")
        CreateProjectDocument(project, doc)

    sub_butt = Button(creat_doc_win, text='Submit', command=Submit)
    sub_butt.grid(row=4, column=0)





class ProjLineClass(LabelFrame):
    def __init__(self, scrolls, doc_list, proj, i):
        super().__init__(scrolls)
        self.parent_flabel_pad = (5, 5)

        self.config(padding=self.parent_flabel_pad)

        proj_frame = LabelFrame(scrolls.scrollable_frame, text=proj, padding=self.parent_flabel_pad)

        proj_var = StringVar(master=proj_frame, value=proj)
        proj_frame.grid(row=i, column=0)
        # proj_label = Label(proj_frame, text=proj)
        # proj_label.grid(row=0, column=0)
        proj_open = Button(proj_frame, text=f'Open', command=lambda: OpenProject(proj_var.get()))
        proj_open.grid(row=0, column=1)

        create_doc_frame = LabelFrame(proj_frame, text='Create New Document', padding=self.parent_flabel_pad)
        create_doc_frame.grid(row=0, column=2)
        line_string_var = StringVar(master=proj_frame)

        doc_choice = Combobox(create_doc_frame, state='readonly', textvariable=line_string_var, values=doc_list)
        doc_choice.config(width=30)
        doc_choice.grid(row=0, column=0)
        create_doc = Button(
            create_doc_frame,
            text='Create Doc',
            command=lambda: CreateProjectDocument(proj_var.get(), line_string_var.get())
        )
        create_doc.grid(row=0, column=1)
