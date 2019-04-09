from widgets import CartesianGrid, PolarGrid, QuitButton
from tkinter import Tk, Frame

class App:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        
        # Variable for tracking the mouse pointer
        self.pointer_y = 0

        # Setting up the plots
        self.cartesian = CartesianGrid(frame, master)
        self.polar = PolarGrid(frame, master)
        self.quit_button = QuitButton(frame, master, self.cartesian.canv_w, self.polar.canv_w)

        # Initializing mouse pointer tracking
        self.cartesian.canvas.bind("<B1-Motion>", self.track_pointer)
    
    def track_pointer(self, event):
        self.pointer_y = event.y

root = Tk()

root.attributes("-fullscreen", True)

app = App(root)

root.mainloop()
