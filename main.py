from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from dans_solvers import cosLaw
# import os
# os.chdir(os.path.dirname(os.getcwd()))


class App1(ttk.Frame):

    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def chosened(self):
        l_a_q = self.selected.get()
        if l_a_q == 'a':
            self.c_name.set('c Angle')
        elif l_a_q == 'l':
            self.c_name.set('C Length')

    def createWidgets(self):
        #text variables
        self.a = StringVar()
        self.b = StringVar()
        self.c = StringVar()
        self.c_name = StringVar()

        self.selected = StringVar()
        self.selected.set('a')
        self.chosened()
        r1 = ttk.Radiobutton(self, text='Angle', value='a', variable=self.selected, command=self.chosened).grid(row=0, column=0, sticky=W)
        r2 = ttk.Radiobutton(self, text='Length', value='l', variable=self.selected, command=self.chosened).grid(row=0, column=1, sticky=W)


        #labels
        self.label1 = ttk.Label(self, text="Side A:").grid(row=1, column=0, sticky=W)
        self.label2 = ttk.Label(self, text="Side B:").grid(row=2, column=0, sticky=W)
        self.label3 = ttk.Label(self, textvariable=self.c_name).grid(row=3, column=0, sticky=W)

        #text boxes
        self.textboxa = ttk.Entry(self, textvariable=self.a).grid(row=1, column=1, sticky=E)
        self.textboxb = ttk.Entry(self, textvariable=self.b).grid(row=2, column=1, sticky=E)
        self.textboxc = ttk.Entry(self, textvariable=self.c).grid(row=3, column=1, sticky=E)

        #buttons
        self.button1 = ttk.Button(self, text="Ok", command=self.calculateCosLaw).grid(row=4, column=2, sticky=E)

#exitApplication = tk.Button(root, text='Exit Application', command=root.destroy)
#canvas1.create_window(85, 300, window=exitApplication)


    def calculateCosLaw(self):
        a = float(self.a.get())
        b = float(self.b.get())
        c = float(self.c.get())

        print(self.selected.get())

        ans = cosLaw(self.selected.get(), a, b, c)

        messagebox.showinfo(title="THIS IS THE ANSWER I CAME UP WITH!!! <3", message=str(ans))


class App2(ttk.Frame):
    """ Application to convert feet to meters or vice versa. """
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """Create the widgets for the GUI"""
        # 1 textbox (stringvar) titties
        self.entry= StringVar()
        self.textBox1= ttk.Entry(self, textvariable=self.entry).grid(row=0, column=1)

        # 5 labels (3 static, 1 stringvar)
        self.displayLabel1 = ttk.Label(self, text="feet").grid(row=0, column=2, sticky=W)
        self.displayLabel2 = ttk.Label(self, text="is equivalent to:").grid(row=1, column=0)
        self.result= StringVar()
        self.displayLabel3 = ttk.Label(self, textvariable=self.result).grid(row=1, column=1)
        self.displayLabel4 = ttk.Label(self, text="meters").grid(row=1, column=2, sticky=W)

        # 2 buttons
        self.calculateButton = ttk.Button(self, text="Calculate", command=self.convert_feet_to_meters).grid(row=2, column=2, sticky=(S,E))
        self.quitButton = ttk.Button(self, text="Quit", command=self.destroy).grid(row=2, column=1, sticky=(S,E))

#exitApplication = tk.Button(root, text='Exit Application', command=root.destroy)
#canvas1.create_window(85, 300, window=exitApplication)


    def convert_feet_to_meters(self):
        """Converts feet to meters, uses string vars and converts them to floats"""
        self.measurement = float(self.entry.get())
        self.meters = self.measurement * 0.3048
        self.result.set(self.meters)



def main():
    #Setup Tk()
    window = Tk()

    #Setup the notebook (tabs)
    notebook = ttk.Notebook(window)
    frame1 = ttk.Frame(notebook)
    frame2 = ttk.Frame(notebook)

    notebook.add(frame1, text="Cosine Law Calculator")
    notebook.add(frame2, text="Feet to Meters")

    notebook.grid()

    #Create tab frames
    app1 = App1(master=frame1)
    app1.grid()
    app2 = App2(master=frame2)
    app2.grid()

    #Main loop
    window.mainloop()


if __name__ == '__main__':
    main()

