from tkinter import Canvas, Frame, Button


class CartesianGrid:
    
    def __init__(self, frame, master, **kwargs):

        # Getting frame dimensions
        self.canv_w, self.canv_h = frame.winfo_vrootwidth()/2, frame.winfo_vrootheight()/2

        # Configuring canvas dimensions and position
        self.canvas = Canvas(master, bg="black", borderwidth=3, relief="sunken")

        ### Configuring vertical position
        if "v_pos" in kwargs:
            if kwargs["v_pos"] == "top":
                self.canvas.place_configure(in_=master, rely=0.0, relx=0.0, relwidth=0.5, relheight=0.5)
            elif kwargs["v_pos"] == "middle":
                self.canvas.place_configure(in_=master, rely=0.25, relx=0.0, relwidth=0.5, relheight=0.5)
            elif kwargs["v_pos"] == "bottom":
                self.canvas.place_configure(in_=master, rely=0.5, relx=0.0, relwidth=0.5, relheight=0.5)
            elif type(kwargs["v_pos"]) == float:
                self.canvas.place_configure(in_=master, rely=kwargs["v_pos"], relx=0.0, relwidth=0.5, relheight=0.5)
        else:
            # Valid parameter for vertical position not provided!
            # Setting to default: "top"
            self.canvas.place_configure(in_=master, rely=0.0, relx=0.0, relwidth=0.5, relheight=0.5)
        
        ### Configuring horisontal position
        if "h_pos" in kwargs:
            if kwargs["h_pos"] == "left":
                self.canvas.place_configure(relx=0.0)
            elif kwargs["h_pos"] == "middle":
                self.canvas.place_configure(relx=0.25)
            elif kwargs["h_pos"] == "right":
                self.canvas.place_configure(relx=0.5)
            elif type(kwargs["h_pos"]) == float:
                self.canvas.place_configure(relx=kwargs["h_pos"])
        else:
            # Valid parameter for horizontal position not provided!
            # Setting to default: "left"
            self.canvas.place_configure(relx=0.0)

        self.canvas.place()

        # Drawing axes
        self.canvas.create_line(10, self.canv_h/2, self.canv_w-10, self.canv_h/2, fill="yellow", width=1.0)
        self.canvas.create_line(10, self.canv_h, 10, 0, fill="yellow", width=1.0)
        
        # Drawing the grid

        ### Drawing the virtical lines
        grid_line_no = 1
        while grid_line_no*50 < self.canv_w:
            self.canvas.create_line(10+grid_line_no*50, self.canv_h, 10+grid_line_no*50,\
                0, fill="yellow", width=1.0, dash=[1, 8]
                )
            grid_line_no += 1
        
        ### Drawing the horisontal lines
        grid_line_no = 1
        while grid_line_no*50 < self.canv_h:
            self.canvas.create_line(self.canv_w, 10+grid_line_no*50, 0, 10+grid_line_no*50,\
                fill="yellow", width=1.0, dash=[1, 8]
                )
            grid_line_no += 1
    
    def plot_data(self, data):
        pass


class PolarGrid:

    def __init__(self, frame, master):

        self.canv_w, self.canv_h = frame.winfo_vrootheight()/2, frame.winfo_vrootheight()/2

        # Configuring canvas dimensions
        self.canvas = Canvas(master, bg="black", borderwidth=3, relief="sunken")
        self.canvas.place_configure(
            in_=master, relx=0.5, rely=0.0, relheight=0.5,\
            width=frame.winfo_vrootheight()/2
            )
        self.canvas.place()
        self.canvas.create_line(10, self.canv_h/2, self.canv_w-10, self.canv_h/2, fill="yellow", width=1.0)
        self.canvas.create_line(self.canv_w/2, self.canv_h-10, self.canv_w/2, 10, fill="yellow", width=1.0)
        self.canvas.create_oval(20, 20, self.canv_w-20, self.canv_h-20, outline="yellow", dash=[16, 16])
        self.canvas.create_oval(100, 100, self.canv_w-100, self.canv_h-100, outline="yellow", dash=[1, 16])


class QuitButton:

    def __init__(self, frame, master, cart_width, polar_width):
        self.quit_button = Button(master, text="Quit", fg="red", command=frame.quit)
        self.quit_button.place_configure(in_=master, x=cart_width+polar_width+3, y=0)
        self.quit_button.place()
