import tkinter.ttk as ttk
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib, os
import numpy as np

try:
    from config import path, lambdadict,lineno_header_data, no_headerlines_ignore, x_axis_field, delimiter, unwanted_keys, lineskipper
except ImportError:
    path = ""
    lambdadict = {}
    lineno_header_data = 0
    no_headerlines_ignore = 1
    x_axis_field="time"
    delimiter=","
    unwanted_keys=[]
    lineskipper = lambda file: (line for line in file)


matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.style = ttk.Style()
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_rowconfigure(0, weight=1)

        self.grid(row=0,column=0,sticky="nsew")
        self.tool_bar = ttk.Frame(parent, width=120)
        self.tool_bar.grid(row=0, column=1)
        self.parent.grid_columnconfigure(1, minsize=120, weight=0)
        
        self.files = []
        self.path = path
        self.lambdadict = lambdadict
        self.lineno_header_data = lineno_header_data
        self.no_headerlines_ignore = no_headerlines_ignore
        self.x_axis_field=x_axis_field
        self.delimiter = delimiter
        self.unwanted_keys = unwanted_keys
        
        self.setupPlot()
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.getFiles()
        
    def setToolbar(self):
        # reset toolbar
        for w in self.tool_bar.winfo_children():
            w.destroy()
            
        self.toolbaritems = {}
        keyset = set()
        for k in self.data.keys():
            for var in self.data[k].keys():
                keyset.add(var)
        if self.x_axis_field in keyset:
            keyset.remove(self.x_axis_field)
        for e in self.unwanted_keys:
            if e in keyset:
                keyset.remove(e)
        keyset=sorted(keyset)
        for k in keyset:
            self.toolbaritems[k] = tk.BooleanVar()
        i = 0
        for i,k in enumerate(keyset):
            tk.Checkbutton(self.tool_bar, text=k, variable=self.toolbaritems[k], command=self.plotAll).grid(row=i, sticky="nsew")#,pady=3
        # print("setting buttons", i)
        tk.Button(self.tool_bar, text="Open New", command=self.getFiles).grid(row=i+1, sticky="nsew",pady=3)
        tk.Button(self.tool_bar, text="Delete All", command=self.removeFiles).grid(row=i+2, sticky="nsew",pady=3)

    def writeConfig(self):
        try:
            with open('config.py', 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            lines = [
                'path = ''\n',
                'lineno_header_data = 0\n',
                'no_headerlines_ignore = 1\n',
                'x_axis_field = "time"\n',
                'delimiter = ","\n',
                'unwanted_keys = []\n',
                'lineskipper = lambda file: (line for line in file)\n',
                'lambdadict = {}\n',
            ]
        lines[0] = "path='"+self.path+"'\n"
        with open('config.py', 'w') as file:
            file.writelines(lines)

    def removeFiles(self):
        self.files = []
        self.getAllData()
        self.plotAll()
                
    def setupPlot(self):
        self.figure = plt.figure(figsize=(6,4), dpi=100)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)
        self.toolbar_frame = tk.Frame(self.parent)
        self.toolbar_frame.grid(row=1,column=0)
        NavigationToolbar2Tk(self.figure_canvas, self.toolbar_frame)
        self.ax = self.figure.add_subplot()
        self.ax.plot([1,2,3,4],[7,3,2,1],label="test")
        self.figure_canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        
    def getFiles(self):
        if self.path:
            p = self.path
        else:
            p = os.getcwd()
        files = tk.filedialog.askopenfilenames(parent=root, title='Choose CSV logfiles', initialdir=p, filetypes=[("CSV files", "*.csv"), ("CSV files", "*.CSV")])
        for f in files:
            self.files.append(f)
        s = f.split("/")
        self.path = "/".join(s[:-1])
        self.writeConfig()
        self.getAllData()

    def getAllData(self):
        self.data = {}
        for f in self.files:
            res = self.readData(f)
            self.data[f.split("/")[-1]] = res
        self.setToolbar()
        
    def readData(self, path):
        res = {}
        with open(path) as f:
            lines=f.readlines()
            header = lines[self.lineno_header_data].strip('\n').split(",")
        fi = open(path, "r")
        try:
            data = np.genfromtxt(lineskipper(fi),skip_header=self.no_headerlines_ignore,delimiter=self.delimiter,autostrip=True)
        except ValueError as e:
            print("Something went wrong reading the file\nplease check config for lineno_header_data and no_headerlines_ignore")
            print(e)
            
        for i,e in enumerate(header):                
            res[e] = data[:,i]
            if e in lambdadict:
                res[e] = [lambdadict[e](x) for x in res[e]]
        return res
            
    def plotAll(self):
        self.ax.clear()
        ylabels = []
        for key in self.data.keys():
            data = self.data[key]
            for var in data.keys():
                if var != self.x_axis_field:
                    if var in self.toolbaritems.keys():
                        if self.toolbaritems[var].get():
                            self.ax.plot(data[self.x_axis_field],data[var],label=key.split(".")[0]+"-"+var)
                            ylabels.append(var)
                            self.ax.legend()
        self.ax.set_xlabel(self.x_axis_field)
        self.ax.set_ylabel(" / ".join(ylabels))
        self.figure.canvas.draw()

    def on_closing(self):
        plt.close()
        self.parent.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).grid(row=0,column=0)
    root.mainloop()