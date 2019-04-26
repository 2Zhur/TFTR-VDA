from plots import Plot
from widgets import CartesianGrid, QuitButton
from tkinter import Tk, Frame
from math import sin, cos, radians
from numpy import array

class App:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        
        # Variable for tracking the mouse pointer
        self.pointer_y = 0

        # Setting up the plots
        self.cartesian = CartesianGrid(frame, master) # canvas is placed in the default position
                                                      # in the upper left corner
        self.cartesian_zoom = CartesianGrid(frame, master, v_pos="bottom")
        self.polar = Plot(master, "polar", relx=0.5, relwidth=0.4)
        
        self.data_tplt = [cos(radians(2*i)) for i in range(360)]

        data = array(self.data_tplt)

        self.polar.plot_data(data)

        self.quit_button = QuitButton(frame, master, self.cartesian.canv_w, self.polar.canv_w)

        # Initializing mouse pointer tracking
        self.polar.canvas.bind("<B1-Motion>", self.track_pointer)
    
    def track_pointer(self, event):
        canv_w = self.polar.canvas.winfo_vrootwidth()
        self.polar.plot_data(
            array([cos(radians(100*i*event.x/canv_w)) + 0.7 * sin(radians(13*i*event.x/canv_w)) for i in range(360)])
        )

root = Tk()

root.attributes("-fullscreen", True)

app = App(root)

root.mainloop()
