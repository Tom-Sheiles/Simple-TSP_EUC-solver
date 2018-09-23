import matplotlib

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

import wx

class TSPGUIClass(wx.Frame): 
    
    
    def __init__(self,parent,title):
        super(TSPGUIClass, self).__init__(parent, title=title, size=(1024,576))
        self.initElements()
        
    def initElements(self):        
        panel = wx.Panel(self,size=(5000,5000))
        
        # Menu bar items
        menubar = wx.MenuBar()
        file = wx.Menu()
        exit = file.Append(wx.ID_EXIT, 'Exit', "status msg..")
        menubar.Append(file, '&File')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.Quit, exit)
        
        # Elements
        nameText = wx.StaticText(panel, label="Name:")
        sizeText = wx.StaticText(panel, -1, label='Size:')
        commentText = wx.StaticText(panel, 1, label='Comment:')
        lengthText = wx.StaticText(panel, label='Length:')
        dateText = wx.StaticText(panel, label='Date:')
        authorText = wx.StaticText(panel, label='Author:')
        timeText = wx.StaticText(panel, label="Time:")

        plotParent = wx.Panel(panel, pos = (180,10), size=(580,1000))
        separateBox = wx.StaticBox(panel, size=(126,225), pos=(10,2), label="TSP Problem Details") 
        randomInput = wx.TextCtrl(plotParent, pos=(0,400))
        randomInputText = wx.StaticText(plotParent, label='Number of Random\ncities', pos=(5,430))
        randomButton = wx.Button(plotParent, label="Generate Random TSP", pos=(120,398))
        
        inputButtonBox = wx.StaticBox(panel, id=-1, size=(200,300), pos=(780,2), label="File Options")
        loadButton = wx.Button(inputButtonBox,id=1, label=("Load File"), pos=(5,30), style=wx.STAY_ON_TOP)
        saveButton = wx.Button(inputButtonBox,id=1, label=("Save Loaded File"), pos=(5,65))
        LoadPrevious = wx.Button(inputButtonBox,id=1, label=("Load From Databse"), pos=(5,100))
        SolveLoaded = wx.Button(inputButtonBox,id=1, label=("Solve Problem!"), pos=(5,170))
        solveTimeBox = wx.TextCtrl(inputButtonBox, value="Enter Solve Time", pos=(5,205))
        greedyCheck = wx.CheckBox(inputButtonBox, label="Greedy\nSolver", pos=(120,170))

        # self.matPlotInit(plotParent, [],[])
        self.matPlotInit(plotParent, [24,16,104,104,104,104,124],[25,25,33,48,65,81,101])

        # Sizer Init
        bs = wx.GridBagSizer(10,300)
        bs.Add(nameText, pos=(1,0), flag=wx.LEFT | wx.TOP, border=14)
        bs.Add(sizeText, pos=(2,0), flag=wx.LEFT, border=14)
        bs.Add(commentText, pos=(3,0), flag=wx.LEFT, border=14)
        bs.Add(lengthText, pos=(4,0), flag=wx.LEFT, border=14)
        bs.Add(dateText, pos=(5,0), flag=wx.LEFT, border=14)
        bs.Add(authorText, pos=(6,0), flag=wx.LEFT, border=14)
        bs.Add(timeText, pos=(7,0), flag=wx.LEFT, border=14)

        panel.SetSizerAndFit(bs)
        #panel.SetSizer(bs)
        
        # Window Attributes
        self.Show(True)
        self.Center()
        
    def matPlotInit(self, plotParent, x = [],y = []):  
        
        f = Figure()
        a = f.add_subplot(111)
        f.set_size_inches(8,5)
        if x:
            x.append(x[0])
            y.append(y[0])
            a.scatter(x, y, color="r")       
            a.plot(x, y, "--", linewidth=1)
        else:
            a.plot()
        canvas = FigureCanvas(plotParent, -1, f)
        a.grid(ls='--')
        canvas.draw()
        
    def Quit(self, e):
        dialoge = wx.MessageDialog(None, 'Are your sure you want to quit', 
                                   'Quit',wx.YES_NO)
        if dialoge.ShowModal() == wx.ID_YES:
            self.Close()
        else:
            return
        

          

def initGui():
    import TSP as tsp
    app = wx.App()
    TSPGUIClass(None, title='TSP Solver')
    app.MainLoop()    
