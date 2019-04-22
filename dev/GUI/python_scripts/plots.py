from tkinter import Canvas

class Plot:
    def __init__(self, master, grid_type, **kwargs):

        # Setting relative canvas dimensions, if not set

        ### Setting relative horisontal position...
        if not "relx" in kwargs:
            kwargs["relx"] = 0.0

        ### ...and relative vertical position...
        if not "rely" in kwargs:
            kwargs["rely"] = 0.0

        ### ...and relative width...
        if not "relwidth" in kwargs:
            kwargs["relwidth"] = 0.5

        ### ...and relative height...
        if not "relheight" in kwargs:
            kwargs["relheight"] = 0.5


        # Initializing the canvas
        self.canvas = Canvas(
            master,\
            bg="black",\
            borderwidth=3
        )

        # Configuring the canvas position
        self.canvas.place_configure(
            in_=master,\
            relx=kwargs["relx"],\
            rely=kwargs["rely"],\
            relwidth=kwargs["relwidth"],\
            relheight=kwargs["relheight"]
        )
        self.canvas.place()
        
        # Acquiring resulting canvas dimensions
        self.canv_w = self.canvas.winfo_vrootwidth() * kwargs["relwidth"]
        self.canv_h = self.canvas.winfo_vrootheight() * kwargs["relheight"]

        self.plot_lines = []

        if grid_type == "polar":
            self._make_polar_grid()
        
        self.grid_type = grid_type


    def plot_data(self, data):
        
        if self.grid_type == "polar":
            if len(data) != 360:
                raise Exception
            # values -> radius + angle -> x, y -> relx, rely

        if self.grid_type == "cartesian":
            pass


    def _make_polar_grid(self):
        
        ### Drawing the vertical axis
        self.canvas.create_line(
            self.canv_w/2,\
            10,\
            self.canv_w/2,\
            self.canv_h - 10,\
            fill="yellow",\
            width=1.0
        )
        
        ### Drawing the horisontal axis
        self.canvas.create_line(
            10,\
            self.canv_h/2,\
            self.canv_w - 10,\
            self.canv_h/2,\
            fill="yellow",\
            width=1.0
        )

        ### Calculating the dimensions of the circles
        ### of the polar grid
        min_rad = (self.canv_h - 40) / 4
        max_rad = (self.canv_h - 40) / 2

        ### Drawing the circles themselves

        ### The outer one
        self.canvas.create_oval(
            self.canv_w/2 - max_rad,\
            self.canv_h/2 - max_rad,\
            self.canv_w/2 + max_rad,\
            self.canv_h/2 + max_rad,\
            outline="yellow",\
            dash=[1, 16]
        )
        
        ### The inner one
        self.canvas.create_oval(
            self.canv_w/2 - min_rad,\
            self.canv_h/2 - min_rad,\
            self.canv_w/2 + min_rad,\
            self.canv_h/2 + min_rad,\
            outline="yellow",\
            dash=[1, 16]
        )

        ### The middle one
        self.canvas.create_oval(
            self.canv_w/2 - (max_rad + min_rad) / 2,\
            self.canv_h/2 - (max_rad + min_rad) / 2,\
            self.canv_w/2 + (max_rad + min_rad) / 2,\
            self.canv_h/2 + (max_rad + min_rad) / 2,\
            outline="yellow",\
            dash=[16, 16]
        )
        
        i = 0
        while i < 360:
            self.plot_lines.append(
                self.canvas.create_line(0, 0, 0, 0)
            )
            i += 1
        

    def _make_cartesian_grid(self):
        pass
