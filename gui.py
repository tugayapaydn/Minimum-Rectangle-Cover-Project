from tkinter import *
from Graph import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

class GUI:
    def __init__(self):
        self._root = Tk()
        self._root.title("Rectilinear Polygon Covering")
        self._root.geometry("1366x768")

        frame1 = Frame(self._root)
        frame1.pack(side=TOP)
        frame2 = Frame(self._root)
        frame2.pack(side=TOP)

        self._label_file_name = Label(frame1, text="Filename")
        self._file_entry = Entry(frame1, textvariable=StringVar())
        self._label_error = Label(frame2, text="")
        self._calc_button = Button(master=frame1, command=self.calc, height=2, width=8, text="Calculate")
    
        self._label_file_name.pack(side=TOP, anchor="center")
        self._file_entry.pack(side=TOP, anchor="center")
        self._calc_button.pack(side=TOP, anchor="center")
        self._label_error.pack(side=TOP, anchor="nw")

        self._fig_before = Figure(figsize = (5, 5), dpi = 144)
        self._fig_after = Figure(figsize = (5, 5), dpi = 144)
        self._canvas1 = FigureCanvasTkAgg(self._fig_before, master=self._root)
        self._canvas2 = FigureCanvasTkAgg(self._fig_after, master=self._root)

    def _draw_polygon(self, graph, p):
        for key, value in graph.items():
            for v in value:
                x = [key.getCoord()[0], v.getCoord()[0]]
                y = [key.getCoord()[1], v.getCoord()[1]]
                p.plot(x, y, color = "black")

    def calc(self):
        self._label_error.configure(text="")
        file = self._file_entry.get()
        self._canvas1.get_tk_widget().pack_forget()
        self._canvas2.get_tk_widget().pack_forget()
        self._fig_before.clear()
        self._fig_after.clear()

        if file != None and len(file) != 0:
            try:
                p = RectilinearPolygon(file)
                pass
            except ValueError as identifier:
                self._label_error.configure(text="Number of vertices in a polygon must be greater than 3")
                return None
            except FileNotFoundError:
                self._label_error.configure(text="There is no such existing file.")
                return None

            graph = p.minimum_cover()
            
            plot1 = self._fig_before.add_subplot(111)
            plot2 = self._fig_after.add_subplot(111)

            self._draw_polygon(graph[0], plot1)
            self._draw_polygon(graph[1], plot2)

            self._canvas1.draw()
            self._canvas2.draw()
            
            self._canvas1.get_tk_widget().pack(side=LEFT)
            self._canvas2.get_tk_widget().pack(side=RIGHT)

    def main(self):
        self._root.mainloop()

if __name__ == "__main__":
    g = GUI()
    g.main()

