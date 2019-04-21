from tkinter import Canvas, Frame, Button
from math import sin, cos, radians
from numpy import ndarray


class Plot:
    # Polina was here
    # Class constructor
    def __init__(self, master, plot_type, **kwargs):
        
        # Initializing the canvas
        
        ### Background color configuration
        ### if not "bg" in kwargs:
        ###    kwargs["bg"] = "black"
        
        ### Borderwidth configuration
        ### if not "borderwidth" in kwargs:
        ###    kwargs["borderwidth"] = 3

        ### Relief configuration
        ### if not "relief" in kwargs:
        ###    kwargs["relief"] = "sunken"

        self.canvas = Canvas(master, bg="black", borderwidth=3, relief="sunken")
        self.canvas.pack_configure(
            in_=master, relx=kwargs["relx"], rely=kwargs["rely"], relwidth=kwargs["relwidth"],\
            relheight=kwargs["relheight"]
            )
        self.canvas.place()
        
        self.canv_w = self.canvas.winfo_width()
        self.canv_h = self.canvas.winfo_height()

        if plot_type == "cartesian":
            self._make_cartesian_grid()
        elif plot_type == "polar":
            self._make_polar_grid()
        else:
            raise ValueError
        
        self.plot_type = plot_type


    # Public method for plotting data (grid independent)
    def plot_data(self, data):
        if self.plot_type == "cartesian":
            self._plot_cartesian(data)
        elif self.plot_type == "polar":
            self._plot_polar(data)
        else:
            raise ValueError
    
    #
    ### Private methods
    #
    
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


    def _make_cartesian_grid(self):
        pass

    
    def _plot_polar(self, data):

        dmin = self._data_min(data)
        dmax = self._data_max(data)
        drange = dmax - dmin

        rel_coords = ndarray(data.shape(), float)
        for pol_c, rel_c in data, rel_coords:
            rel_c[0] = pol_c[1]


    def _plot_cartesian(self, data, **kwargs):
        pass


    def _data_mean(self, data):
        if type(data) == ndarray:
            return data.mean()


    def _data_max(self, data):
        if type(data) == ndarray:
            return data.max()


    def _data_min(self, data):
        if type(data) == ndarray:
            return data.min()


    # def _polar_connect(self, prev_point, point):
        
    #     ### Calculating the dimensions of the circles
    #     ### of the polar grid
    #     min_rad = (self.canv_h - 40) / 4
    #     max_rad = (self.canv_h - 40) / 2

