from tkinter import Canvas

class Plot:
    def __init__(self, frame, master, grid_type, **kwargs):

        #Denis was here
        # Acquiring window dimensions
        self.window_w = frame.winfo_vrootwidth()
        self.window_h = frame.winfo_vrootheight()

        # Initializing the canvas
        self.canvas = Canvas(master, bg="black", borderwidth=3, relief="sunken")

        # Configuring the canvas position
        self.canvas.place_configure(
            in_=master,\
            relx=kwargs["relx"],\
            rely=kwargs["rely"],\
            relwidth=kwargs["relwidth"],\
            relheight=kwargs["relheight"]
        )


    def plot_data(self, data):
        pass
