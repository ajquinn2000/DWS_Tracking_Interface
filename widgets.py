from tkinter import StringVar
from tkinter.ttk import Label, Combobox, Entry
from tkinter import PhotoImage, Button


class DropDown:
    def __init__(self, master, font, values, x_loc, y_loc, g_or_p='p', **kw):
        super().__init__(**kw)
        self.info = None
        self.master = master
        self.font = font
        self.values = values
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.g_or_p = g_or_p

        self.string_var = StringVar()

        self.create()

    def create(self):

        self.info = Combobox(master=self.master, values=self.values, font=self.font)
        if self.g_or_p == 'g':
            self.info.grid(
                column=self.x_loc,
                row=self.y_loc
            )
        elif self.g_or_p == 'p':
            self.info.place(relx=self.x_loc, rely=self.y_loc, anchor='n')


    def update_(self):
        self.info.destroy()

        self.info = Label(master=self.master, values=self.values)
        if self.g_or_p == 'g':
            self.info.grid(
                column=self.x_loc,
                row=self.y_loc
            )
        elif self.g_or_p == 'p':
            self.info.place(relx=self.x_loc, rely=self.y_loc, anchor='n')


class InputBoxes:
    def __init__(self, master, text, font, x_loc, y_loc, **kw):
        super().__init__(**kw)
        self.info = None
        self.master = master
        self.text = text
        self.font = font
        self.x_loc = x_loc
        self.y_loc = y_loc

        self.create()

    def create(self):
        self.info = Entry(master=self.master, font=self.font)
        self.info.grid(
            column=self.x_loc,
            row=self.y_loc
        )


    def update_(self):
        self.info.destroy()

        self.info = Label(master=self.master, text=self.text, font=self.font)
        self.info.grid(
            column=self.x_loc,
            row=self.y_loc
        )



class Label_:
    def __init__(self, master, text, font, x_loc, y_loc, background='white', g_or_p='p', **kw):
        super().__init__(**kw)
        self.info = None
        self.master = master
        self.text = text
        self.font = font
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.background = background
        self.g_or_p = g_or_p

        self.create()

    def create(self):
        self.info = Label(master=self.master, text=self.text, font=self.font, background=self.background)
        if self.g_or_p == 'g':
            self.info.grid(
                column=self.x_loc,
                row=self.y_loc,
            )
        elif self.g_or_p == 'p':
            self.info.place(
                relx=self.x_loc,
                rely=self.y_loc,
                anchor='n'
            )


    def update_(self):
        self.info.destroy()

        self.info = Label(master=self.master, text=self.text, font=self.font)
        if self.g_or_p == 'g':
            self.info.grid(
                column=self.x_loc,
                row=self.y_loc
            )
        elif self.g_or_p == 'p':
            self.info.place(
                relx=self.x_loc,
                rely=self.y_loc,
                anchor='n'
            )


class Button_:
    def __init__(self, master, text, font, width, x_loc, y_loc, func, g_or_p='p', **kw):
        super().__init__(**kw)
        self.info = None
        self.master = master
        self.text = text
        self.font = font
        self.width = width
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.func = func
        self.g_or_p = g_or_p

        self.pixel_virtual = PhotoImage(width=1, height=1)
        pixel_label = Label(image=self.pixel_virtual)
        pixel_label.image = self.pixel_virtual

        self.create()
        # print(func)

    def create(self):
        self.info = Button(master=self.master, image=self.pixel_virtual, text=self.text, width=round(self.width), command=self.func, compound='c')
        if self.g_or_p == 'g':
            self.info.grid(
                column=self.x_loc,
                row=self.y_loc
            )
        elif self.g_or_p == 'p':
            self.info.place(
                relx=self.x_loc,
                rely=self.y_loc,
                anchor='n'
            )


    def update_(self):
        self.info.destroy()

        self.info = Button(master=self.master, text=self.text)
        if self.g_or_p == 'g':
            self.info.grid(
                column=self.x_loc,
                row=self.y_loc
            )
        elif self.g_or_p == 'p':
            self.info.place(
                relx=self.x_loc,
                rely=self.y_loc,
                anchor='n'
            )
