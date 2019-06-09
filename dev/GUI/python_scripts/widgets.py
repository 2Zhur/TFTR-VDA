from tkinter import Canvas, Frame, Button
from tkinter import filedialog as fd


class ChooseConfig1:
    def __init__(self, frame, master, cart_width, polar_width):
        self.cc1 = Button(
            master,\
            text="Choose Data Source",\
            fg="black",\
            command=fd.askopenfilename
        )

        self.cc1.place_configure(
            in_=master, x=cart_width+3, rely=0.95,\
            relwidth=0.15, relheight=0.05
            )
        self.cc1.place()
