from tkinter import Tk, Frame, Button, filedialog as fd
from plots import Plot
from numpy import array, ndarray, sin, cos, radians, concatenate
from numpy import polynomial as Pol
from parsing import TFTR_dataframe
from lup import *

class QuitButton:

    def __init__(self, frame, master, cart_width, polar_width):
        self.quit_button = Button(master, text="Quit", fg="red", command=frame.quit)
        self.quit_button.place_configure(
            in_=master, x=cart_width+polar_width+3, rely=0.0,\
            relwidth=0.05, relheight=0.05
        )
        self.quit_button.place()


class ChooseSource:

    def __init__(self, frame, master, cart_width, polar_width, command):
        self.cs = Button(
            master,\
            text="Choose Data Source",\
            fg="black",\
            command=command
        )

        self.cs.place_configure(
            in_=master, x=cart_width+3, rely=0.95,\
            relwidth=0.15, relheight=0.05
            )
        self.cs.place()

class App:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        
        # Data slice start time (on the zoomed graph)
        self.dsst = 0

        # Poloidal data time
        self.pdt = 0

        # Setting up the plots
        self.cartesian = Plot(master, "cartesian")  # canvas is placed in the default position
                                                    # in the upper left corner

        self.cartesian_zoom = Plot(master, "cartesian", zoom=True, rely=0.5)
        self.polar = Plot(master, "polar", relx=0.5, relwidth=0.4)

        self.file_name = fd.askopenfilename(filetypes={("Data Files", "*.C1")})

        self.df = TFTR_dataframe(self.file_name, "P93A.MM", "I76778.C1")
        self.cartesian.plot_data(self.df.timed_data().transpose()[1])

        self.quit_button = QuitButton(frame, master, self.cartesian.canv_w, self.polar.canv_w)
        self.cs = ChooseSource(frame, master, self.cartesian.canv_w, self.polar.canv_w, self.choose_source)

        # Initializing mouse pointer tracking        
        self.cartesian.canvas.bind("<Button-1>", self.move_zoomed)
        self.cartesian.canvas.bind("<B1-Motion>", self.move_zoomed)
        self.cartesian_zoom.canvas.bind("<Button-1>", self.display_poloidal)
        self.cartesian_zoom.canvas.bind("<B1-Motion>", self.display_poloidal)

    def choose_source(self):
        self.file_name = fd.askopenfilename(filetypes={("Data Files", "*.C1")})
        self.cartesian.cursor = -1
        self.df = TFTR_dataframe(self.file_name, "P93A.MM", "I76778.C1")
        self.cartesian.plot_data(self.df.timed_data().transpose()[1])

    def move_zoomed(self, event):
        canv_w = self.cartesian.canv_w
        self.cartesian_zoom.cursor = -1

        if self.cartesian.cursor == -1:
            self.cartesian.put_cursor(event.x)
        else:
            self.cartesian.move_cursor(event.x)

        data = self.df.timed_data().transpose()[1]
        
        data_len = len(data)

        if data_len <= (canv_w - 40):
            data_step = 1
            canv_step = (canv_w - 40) / data_len
        else:
            data_step = data_len / (canv_w - 40)
            canv_step = 1

        move = lambda i : self.cartesian_zoom.plot_data(
                data[i:100+i]
            )
        
        dti = lambda t1, t2 : self.cartesian_zoom.dti(t1, t2)

        i = 0

        if 20 < event.x < canv_w - 20:
            i = int((event.x - 20 / canv_step) * data_step)
            if i < data_len - 100:
                move(i)
                dti((i - 1) * 2, (99 + i) * 2)
                self.dsst = (i - 1) * 2
            else:
                move(data_len - 100)
                dti((data_len - 100) * 2, (data_len - 1) * 2)
                self.dsst = (data_len - 100) * 2

    def display_poloidal(self, event):


        canv_w = self.cartesian.canv_w

        if 20 < event.x < canv_w - 20:

            canv_step = (canv_w - 40) / 100

            if self.cartesian_zoom.cursor == -1:
                self.cartesian_zoom.put_cursor(event.x)
            else:
                self.cartesian_zoom.move_cursor(event.x)

            offset = int((event.x - 20) / canv_step)

            time = self.dsst + offset

            pd = self.df.poloidal_data(time)

            num_of_sens = len(pd[0])

            pd_ext = concatenate((pd, pd, pd), axis=1)

            i = 0

            for angle in pd_ext[0][0:num_of_sens]:
                pd_ext[0][i] = radians(angle - 360.0)
                i += 1

            i = 0

            for angle in pd_ext[0][num_of_sens:(2 * num_of_sens)]:
                pd_ext[0][i + num_of_sens] = radians(angle)
                i += 1

            i = 0

            for angle in pd_ext[0][(2 * num_of_sens):(3 * num_of_sens)]:
                pd_ext[0][i + (2 * num_of_sens)] = radians(angle + 360.0)
                i += 1
           
            print(pd_ext)

            polinomial = Pol.Polynomial.fit(pd_ext[0], pd_ext[1], deg=33).convert().coef
            
            print(polinomial)

            # X = ndarray((num_of_sens + 2, num_of_sens + 2))
            # i = 0
            # j = 0

            # angle = 0.0

            # for row in X:
            #     i = 0
            #     angle = pd_ext[0][j]
                
            #     for elem in row:
            #         X[j][i]= angle ** i
            #         i += 1
                
            #     j += 1
            
            # b = pd_ext[1]

            # L, U, P = lu(X)


            poloidal = get_all_points(polinomial)

            print(poloidal)

            self.polar.plot_data(poloidal)
            self.polar.disp_time(time)



root = Tk()

root.attributes("-fullscreen", True)

app = App(root)

root.mainloop()
