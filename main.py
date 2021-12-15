from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from os import path


from new_project import CreateNewProject
from general_funcs import GoToTracking
from nb_packing_slip import PackingSlipPage
from nb_purchase_input import PurchaseInputPage
from nb_project_browser import ProjectBrowser, OpenProject, CreateDocCommand
from nb_vendor_browser import DisplayVendors
from time_hour_input import TimeHourInput, AddWorker


# fix new project shop creation, so that it creates a new one every month and year
    # also so the user can select shop in purchase input
# add in yearly changing project folder
    # add in year search and set to current year
    # add in code to handle the new year Shop file creation, New all year IGS projects
    # make igs log change xlsx from year to year

# prevent making vendor w/blank name


# Minor bugs ___________
# vendor search not refreshing list






def main():



    # Setup Tk()
    dws_tracking_win = Tk()
    dws_tracking_win.geometry('750x600')
    dws_tracking_win.title('DWS Tracking Interface')


    # Setup the notebook (tabs)
    notebook = ttk.Notebook(dws_tracking_win)

    nb_project_browser = ttk.Frame(notebook)
    nb_gen_packslip = ttk.Frame(notebook)
    nb_purchase_input = ttk.Frame(notebook)
    nb_vendor_browser = ttk.Frame(notebook)


    notebook.add(nb_project_browser, text='Project Browser')
    notebook.add(nb_gen_packslip, text="Packing Slip")
    notebook.add(nb_purchase_input, text="Purchase Input")
    notebook.add(nb_vendor_browser, text='Vendor Browser')


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
    # app3.ClearVendor()

    app3.grid(sticky=NSEW)
    app4 = DisplayVendors(master=nb_vendor_browser, vendor_fo_purch=app3)
    app4.grid()


    menubar = Menu(dws_tracking_win)
    project_menu = Menu(menubar, tearoff=0)
    doc_menu = Menu(menubar, tearoff=0)
    vendor_menu = Menu(menubar, tearoff=0)
    worker_menu = Menu(menubar, tearoff=0)

    project_menu.add_command(label="New Project", command=CreateNewProject)
    project_menu.add_command(label="Open Project", command=OpenProject)
    menubar.add_cascade(label="Projects", menu=project_menu)

    doc_menu.add_command(label='New Document', command=CreateDocCommand)
    menubar.add_cascade(label='Documents', menu=doc_menu)

    vendor_menu.add_command(label='Add Vendor', command=app4.NewVendor)
    vendor_menu.add_command(label='Delete Vendor', command=app4.DeleteVendor)
    menubar.add_cascade(label='Vendors', menu=vendor_menu)

    worker_menu.add_command(label='Submit Worker Hours', command=TimeHourInput)
    worker_menu.add_command(label='Add Worker', command=AddWorker)
    menubar.add_cascade(label='Workers', menu=worker_menu)

    dws_tracking_win.config(menu=menubar)

    #Main loop
    dws_tracking_win.mainloop()


if __name__ == '__main__':
    GoToTracking()
    main()

