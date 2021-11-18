from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from os import path

from new_project import CreateNewProject

from nb_packing_slip import PackingSlipPage
from nb_purchase_input import PurchaseInputPage
from nb_project_browser import ProjectBrowser, OpenProject, GetDocList, CreateDocCommand

# allow amount to be a float not just digit
# make the purchase input pull for vendor list
# add user defined project numbers that increase the project could as well.
# add "Add Vendor" menu button w/ open vendor list menu button
# add "add Worker" menu button w/ open worker folder menu button
# add tab for worker hours input
# make igs log change xlsx from year to year
# add packing slip stat
# add in code to handle the new year Shop file creation, New all year IGS projects



def main():
    #Setup Tk()
    dws_tracking_win = Tk()
    dws_tracking_win.geometry('850x600')
    dws_tracking_win.title('main_boi')

    #Setup the notebook (tabs)
    notebook = ttk.Notebook(dws_tracking_win)

    nb_project_browser = ttk.Frame(notebook)
    nb_gen_packslip = ttk.Frame(notebook)
    nb_purchase_input = ttk.Frame(notebook)


    notebook.add(nb_project_browser, text='Project Browser')
    notebook.add(nb_gen_packslip, text="Packing Slip")
    notebook.add(nb_purchase_input, text="Purchase Input")


    Grid.rowconfigure(dws_tracking_win, 0, weight=1)
    Grid.columnconfigure(dws_tracking_win, 0, weight=1)

    # Grid.rowconfigure(dws_tracking_win, 1, weight=1)

    # fitting the notebook to the edges of the parent window
    notebook.grid(row=0, column=0, sticky=NSEW)

    #Create tab frames
    app1 = ProjectBrowser(master=nb_project_browser)
    app1.grid()
    app2 = PackingSlipPage(master=nb_gen_packslip)
    app2.grid()
    app3 = PurchaseInputPage(master=nb_purchase_input)
    app3.grid(sticky=NSEW)


    menubar = Menu(dws_tracking_win)
    project_menu = Menu(menubar, tearoff=0)
    doc_menu = Menu(menubar, tearoff=0)

    project_menu.add_command(label="New Project", command=CreateNewProject)
    project_menu.add_command(label="Open Project", command=OpenProject)
    menubar.add_cascade(label="Projects", menu=project_menu)

    doc_menu.add_command(label='New Document', command=CreateDocCommand)
    menubar.add_cascade(label='Documents', menu=doc_menu)

    dws_tracking_win.config(menu=menubar)

    #Main loop
    dws_tracking_win.mainloop()


if __name__ == '__main__':
    main()

