from tkinter import Canvas
from numpy import sin, cos, radians, gcd, log10, log
from decimal import Decimal

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
    
        # Also configure default zoom in case of a cartesian graph
        if grid_type == "cartesian" and not "zoom" in kwargs:
            kwargs["zoom"] = False
        
        if grid_type == "cartesian" and not "offset" in kwargs:
            kwargs["offset"] = 0

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

        # Creating a list to store indeces of the lines of the graph
        self.plot_lines = []

        # Polar grid
        if grid_type == "polar":
            self._make_polar_grid()
            self.time_label = -1

        # Cartesian grid
        if grid_type == "cartesian":
            self._make_cartesian_grid()
            
            # Cursor
            self.cursor = -1
        
        self.grid_type = grid_type

##############################################################
#                          Cursor                            # 
##############################################################

    def put_cursor(self, x):
        self.cursor = self.canvas.create_line(
            x,\
            10,\
            x,\
            self.canv_h - 10,\
            fill="red",\
            dash=[16, 16]
        )

    def move_cursor(self, x):
        self.canvas.coords(
            self.cursor,\
            x,\
            10,\
            x,\
            self.canv_h - 10
        )

    def hide_cursor(self):
        self.canvas.delete(self.cursor)
        self.cursor = -1

##############################################################
#                        Display time                        # 
##############################################################

    # Display time interval (for cartesian)
    def dti(self, t1, t2):

        self.canvas.create_text(
            self.canv_w - 300,\
            self.canv_h - 30,\
            font=("Courier", 10),\
            fill="yellow",\
            text=str(t1) + "us to " + str(t2) + "us",\
            anchor="nw"
        )

    # Display time (for polar)
    def disp_time(self, t):
        if self.time_label != -1:
            self.canvas.delete(self.time_label)
        self.time_label = self.canvas.create_text(
            self.canv_w - 300,\
            self.canv_h - 30,\
            font=("Courier", 10),\
            fill="yellow",\
            text="Time: " + str(t) + "us",\
            anchor="nw"
        )

##############################################################
#               Common method for plotting data              #
##############################################################

    def plot_data(self, data, **kwargs):

        ###########################################################
        #                       Polar grid                        #
        ###########################################################

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

            get_abs_x = lambda val, abs_rad: int((self.canv_w / 2) + cos(radians(val)) * abs_rad)
            get_abs_y = lambda val, abs_rad: int((self.canv_h / 2) + sin(radians(val)) * abs_rad)

            i = 0

            abs_rad1 = 0
            abs_rad2 = 0

            x1 = 0.0
            y1 = 0.0

            x2 = 0.0
            y2 = 0.0

            while i < 360: 

                if i == 0:
                    print(data[0])
                    abs_rad1 = get_abs_rad(data[0])
                    # print(abs_rad1)
                    x1 = get_abs_x(i, abs_rad1)
                    y1 = get_abs_y(i, abs_rad1)


                abs_rad2 = get_abs_rad(data[(i+1) % 360])

                x2 = get_abs_x(i, abs_rad2)
                y2 = get_abs_y(i, abs_rad2)

                self.canvas.coords(
                    self.plot_lines[i],\
                    x1,\
                    y1,\
                    x2,\
                    y2
                )

                abs_rad1 = abs_rad2
                x1, y1 = x2, y2

                i += 1

            # values -> radius + angle -> x, y -> relx, rely
        

        ###########################################################
        #                     Cartesian grid                      #
        ###########################################################

        if self.grid_type == "cartesian":

            self.canvas.delete("all")
            
            dmax = data.max()
            dmin = data.min()

            max_div = max(abs(dmax), abs(dmin))

            self._make_cartesian_grid()

            data_len = len(data)

            if data_len <= (self.canv_w - 40):
                data_step = 1
                canv_step = (self.canv_w - 40) / data_len
            else:
                data_step = data_len / (self.canv_w - 40)
                canv_step = 1

            get_abs_y = lambda y: int(((self.canv_h / 2 - 10) * (y / max_div)) + self.canv_h / 2)

            value_step = 10 ** (int(log10(max_div)))
            if max_div / value_step < 3:
                value_step /= 2

            y_p = 0
            y_n = 0
            level = value_step

            while y_p - y_n < self.canv_h:
                
                y_p = get_abs_y(level)
                y_n = get_abs_y(-1 * level)
                
                self.canvas.create_line(
                    20,\
                    y_p,\
                    self.canv_w - 20,\
                    y_p,\
                    fill="yellow",\
                    dash=[1, 6]
                )
                
                self.canvas.create_text(
                    10,\
                    y_p - 5,\
                    font=("Courier", 7),\
                    fill="yellow",\
                    text="{:.1E}".format(Decimal(str(level))),\
                    anchor="nw"
                )
                self.canvas.create_line(20, y_n, self.canv_w - 20, y_n, fill="yellow", dash=[1, 6])


                self.canvas.create_text(
                    10,\
                    y_n - 5,\
                    font=("Courier", 7),\
                    fill="yellow",\
                    text="{:.1E}".format(Decimal(str(-1 * level))),\
                    anchor="nw"
                )

                level += value_step

            x1 = 20
            y1 = get_abs_y(data[0])

            x2 = 20
            x2_fl = 20.0
            y2 = get_abs_y(data[0])

            i = 0
            i_fl = 0.0

            while i < data_len - 1:
                
                x2_fl += canv_step
                x2 = int(x2_fl)
                y2 = get_abs_y(data[i+1])

                self.canvas.create_line(x1, y1, x2, y2, fill="white")

                i_fl += data_step

                i = int(i_fl)

                x1, y1 = x2, y2

##############################################################
#                 Polar grid private method                  #
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
                self.canvas.create_line(
                    0,\
                    0,\
                    0,\
                    0,\
                    fill="white"
                )
            )
            i += 1

##############################################################
#               Cartesian grid private method                # 
##############################################################

    def _make_cartesian_grid(self):
        self.canvas.create_line(
            10,\
            self.canv_h/2,\
            self.canv_w - 10,\
            self.canv_h/2,\
            fill="yellow"
        )
        self.canvas.create_line(
            20,\
            10,\
            20,\
            self.canv_h - 10,\
            fill="yellow"
        )
