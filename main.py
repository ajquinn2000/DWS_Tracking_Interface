from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from os import path


from new_project import CreateNewProject

from nb_packing_slip import PackingSlipPage
from nb_purchase_input import PurchaseInputPage
from nb_project_browser import ProjectBrowser, OpenProject, GetDocList, CreateDocCommand
from nb_vendor_browser import DisplayVendors


# add "add Worker" menu button w/ open worker folder menu button
# add global file variables, so you do not have to keep opening the file
# add tab for worker hours input
# make igs log change xlsx from year to year
# add packing slip stat
# add in code to handle the new year Shop file creation, New all year IGS projects






def main():



    # Setup Tk()
    dws_tracking_win = Tk()
    dws_tracking_win.geometry('850x600')
    dws_tracking_win.title('main_boi')


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
    app3.grid(sticky=NSEW)
    app4 = DisplayVendors(master=nb_vendor_browser)
    app4.grid()


    menubar = Menu(dws_tracking_win)
    project_menu = Menu(menubar, tearoff=0)
    doc_menu = Menu(menubar, tearoff=0)
    vendor_menu = Menu(menubar, tearoff=0)

    project_menu.add_command(label="New Project", command=CreateNewProject)
    project_menu.add_command(label="Open Project", command=OpenProject)
    menubar.add_cascade(label="Projects", menu=project_menu)

    doc_menu.add_command(label='New Document', command=CreateDocCommand)
    menubar.add_cascade(label='Documents', menu=doc_menu)

    vendor_menu.add_command(label='Add Vendor', command=app4.NewVendor)
    vendor_menu.add_command(label='Delete Vendor', command=app4.DeleteVendor)
    menubar.add_cascade(label='Vendors', menu=vendor_menu)

    dws_tracking_win.config(menu=menubar)

    #Main loop
    dws_tracking_win.mainloop()


if __name__ == '__main__':
    main()

