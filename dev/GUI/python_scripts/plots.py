from tkinter import Canvas
from math import sin, cos, radians

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
        
        ### Also configure zoom in case of a cartesian grid
        if grid_type == "cartesian" and not "zoom" in kwargs:
            kwargs["zoom"] = 1.0

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

        if grid_type == "cartesian":
            self._make_cartesian_grid()
        
        self.grid_type = grid_type
        
########
        if self.grid_type == "cartesian":
            self.zoom = kwargs["zoom"]


    def plot_data(self, data):

        if self.grid_type == "polar":
            if len(data) != 360:
                raise Exception("Wrond data lenth!")

            dmax = data.max()
            dmin = data.min()

            max_div = max(abs(dmax), abs(dmin))

            min_rad = (self.canv_h - 40) / 4
            max_rad = (self.canv_h - 40) / 2
            mid_rad = (max_rad + min_rad) / 2
            gap_w = max_rad - mid_rad

            get_abs_rad = lambda val: mid_rad + (val * gap_w / max_div)

            get_abs_x = lambda val, abs_rad: (self.canv_w / 2) + cos(radians(val)) * abs_rad
            get_abs_y = lambda val, abs_rad: (self.canv_h / 2) + sin(radians(val)) * abs_rad

            i = 0

            abs_rad1 = 0
            abs_rad2 = 0

            x1 = 0.0
            y1 = 0.0

            x2 = 0.0
            y2 = 0.0

            while i < 360:

                if i == 0:
                    abs_rad1 = get_abs_rad(data[0])
                    x1 = get_abs_x(i, abs_rad1)
                    y1 = get_abs_y(i, abs_rad1)


                abs_rad2 = get_abs_rad(data[(i+1) % 360])

                x2 = get_abs_x(i, abs_rad2)
                y2 = get_abs_y(i, abs_rad2)

                self.canvas.coords(self.plot_lines[i], x1, y1, x2, y2)

                abs_rad1 = abs_rad2
                x1 = x2
                y1 = y2

                i += 1

            # values -> radius + angle -> x, y -> relx, rely

        if self.grid_type == "cartesian":
            pass

##############################################################
#                 Polar grid private methods                 #
##############################################################

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
            self.canv_w/2 - ((max_rad + min_rad) / 2),\
            self.canv_h/2 - ((max_rad + min_rad) / 2),\
            self.canv_w/2 + ((max_rad + min_rad) / 2),\
            self.canv_h/2 + ((max_rad + min_rad) / 2),\
            outline="yellow",\
            dash=[16, 16]
        )

        i = 0
        while i < 360:
            self.plot_lines.append(
                self.canvas.create_line(0, 0, 0, 0, fill="yellow")
            )
            i += 1

##############################################################
#                   For the cartesian grid                   # 
##############################################################        

#
# The class already has the folowing attributes:
# - self.canv_w - the width of the canvas
# - self.canv_h - the height of the canvas
# - self.zoom - the desired zoom
#   (see lines 26 and 61)
# - self.grid_type - "cartesian" or "polar"
#

    def _make_cartesian_grid(self):
        pass
