import tkinter.ttk as ttk
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib
import os
import numpy as np
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.style = ttk.Style()
        # self.style.theme_use("clam")
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        # self.parent.grid_columnconfigure(0, weight=1)
        self.grid(row=0,column=0)
        self.tool_bar = ttk.Frame(parent, width=200)
        self.tool_bar.grid(row=0, column=1)
        self.tool_bar.grid_columnconfigure(0, weight=1)
        
        self.setupPlot()
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.getFiles()
        self.getAllData()
        self.setToolbar()
        # print(self.data)
        self.plotAll()
        
        
    def setToolbar(self):
        self.toolbaritems = {}
        keyset = set()
        for k in self.data.keys():
            for var in self.data[k].keys():
                keyset.add(var)
        keyset.remove("time")
        for k in keyset:
            self.toolbaritems[k] = tk.BooleanVar()
        for i,k in enumerate(keyset):
            tk.Checkbutton(self.tool_bar, text=k, variable=self.toolbaritems[k], command=self.plotAll).grid(row=i, sticky="nsew")
        
    def setupPlot(self):
        self.figure = plt.figure(figsize=(6,4), dpi=100)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)
        self.toolbar_frame = tk.Frame(self.parent)
        self.toolbar_frame.grid(row=1,column=0)
        NavigationToolbar2Tk(self.figure_canvas, self.toolbar_frame)
        self.ax = self.figure.add_subplot()
        self.ax.plot([1,2,3,4],[500,3,2,1],label="test")
        self.figure_canvas.get_tk_widget().grid(row=0, column=0)
        
    def getFiles(self):
        self.files = tk.filedialog.askopenfilenames(parent=root, title='Choose CSV logfiles', initialdir=os.getcwd(), filetypes=[("CSV files", "*.csv")])
        
    def getAllData(self):
        self.data = {}
        for f in self.files:
            res = self.readData(f)
            self.data[f.split("/")[-1]] = res
        
    def readData(self, path):
        res = {}
        with open(path) as f:
            header = f.readline().strip('\n').split(",")
        data = np.genfromtxt(path,skip_header=1,delimiter=",")
        for i,e in enumerate(header):
            res[e] = data[:,i]
        return res
            
    def plotAll(self):
        self.ax.clear()
        for key in self.data.keys():
            data = self.data[key]
            for var in data.keys():
                if var != "time":
                    if self.toolbaritems[var].get():
                        self.ax.plot(data["time"],data[var],label=key.split(".")[0]+"-"+var)
                        self.figure.legend()
        self.figure.canvas.draw()

    def on_closing(self):
        plt.close()
        self.parent.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).grid(row=0,column=0)
    root.mainloop()