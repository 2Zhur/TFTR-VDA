from plots import Plot
from widgets import CartesianGrid, QuitButton
from tkinter import Tk, Frame
from math import sin, cos, radians
from numpy import array
from parsing import TFTR_dataframe

class App:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        
        # Variable for tracking the mouse pointer
        self.pointer_y = 0

        # Setting up the plots
        self.cartesian = Plot(master, "cartesian") # canvas is placed in the default position
                                                      # in the upper left corner

        df = TFTR_dataframe("BP76778.C1", "P93A.MM", "I76778.C1")
        self.cartesian.plot_data(df.timed_data().transpose()[1])

        self.cartesian_zoom = CartesianGrid(frame, master, v_pos="bottom")
        self.polar = Plot(master, "polar", relx=0.5, relwidth=0.4)
        
        self.data_tplt = [cos(radians(2*i)) for i in range(360)]

        data = array(self.data_tplt)

        self.polar.plot_data(data)

        self.quit_button = QuitButton(frame, master, self.cartesian.canv_w, self.polar.canv_w)

        # Initializing mouse pointer tracking
        self.cartesian.canvas.bind("<B1-Motion>", self.track_pointer)
    
    def track_pointer(self, event):
        canv_w = self.cartesian.canvas.winfo_width()
        self.polar.plot_data(
            array([sin(radians(6 * i*event.x/canv_w)) for i in range(360)])
        )

root = Tk()

root.attributes("-fullscreen", True)

app = App(root)

root.mainloop()
