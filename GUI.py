import TSP as tsp
import datetime
import time
import mysql.connector
import random
import numpy as np

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import style

style.use('fivethirtyeight')

import wx

class TSPGUIClass(wx.Frame): 
    xs = []
    ys = []
    fileName = ""
    initialNodes = []
    tourDistance = float()
    tourString = ""
    
    def __init__(self,parent,title):
        super(TSPGUIClass, self).__init__(parent, title=title, size=(1024,576))
        try: 
            self.connection = mysql.connector.connect(host = 'mysql.ict.griffith.edu.au',
                                             database = '1810ICTdb',
                                             user = 's5132012',
                                             password = 'XwxXSo4j')
        except:
            print("Cannot Connect to Database")
            self.close()
    
        if self.connection.is_connected():
            print('Connected to the database')       
            self.cursor = self.connection.cursor(buffered=True)
            
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
        self.nameText = wx.StaticText(panel, label="Name:")
        self.sizeText = wx.StaticText(panel, -1, label='Size:')
        self.commentText = wx.StaticText(panel, 1, label='Comment:')
        self.typeText = wx.StaticText(panel, label='Type:')
        self.lengthText = wx.StaticText(panel, label='Length:')
        self.dateText = wx.StaticText(panel, label='Date:')
        self.authorText = wx.StaticText(panel, label='Author:')
        self.timeText = wx.StaticText(panel, label="Time:")

        self.plotParent = wx.Panel(panel, pos = (180,10), size=(580,1000))
        separateBox = wx.StaticBox(panel, size=(126,245), pos=(10,2), label="TSP Problem Details") 
        self.randomInput = wx.TextCtrl(self.plotParent, pos=(0,400))
        randomInputText = wx.StaticText(self.plotParent, label='Number of Random\ncities', pos=(5,430))
        randomButton = wx.Button(self.plotParent, label="Generate Random TSP", pos=(120,398))
        
        inputButtonBox = wx.StaticBox(panel, id=-1, size=(200,300), pos=(780,2), label="File Options")
        loadButton = wx.Button(inputButtonBox,id=1, label=("Load File"), pos=(5,30), style=wx.STAY_ON_TOP)
        saveButton = wx.Button(inputButtonBox,id=1, label=("Save Loaded File"), pos=(5,65))
        LoadPrevious = wx.Button(inputButtonBox,id=1, label=("Load From Databse"), pos=(5,100))
        SolveLoaded = wx.Button(inputButtonBox,id=1, label=("Solve Problem!"), pos=(5,170))
        self.solveTimeBox = wx.TextCtrl(inputButtonBox, value="Enter Solve Time", pos=(5,205))
        greedyCheck = wx.CheckBox(inputButtonBox, label="Greedy\nSolver", pos=(120,170))

        self.matPlotInit(self.plotParent, [],[])

        # Sizer Init
        bs = wx.GridBagSizer(10,300)
        bs.Add(self.nameText, pos=(1,0), flag=wx.LEFT | wx.TOP, border=14)
        bs.Add(self.sizeText, pos=(2,0), flag=wx.LEFT, border=14)
        bs.Add(self.commentText, pos=(3,0), flag=wx.LEFT, border=14)
        bs.Add(self.typeText, pos=(4,0), flag=wx.LEFT, border=14)
        bs.Add(self.lengthText, pos=(5,0), flag=wx.LEFT, border=14)
        bs.Add(self.dateText, pos=(6,0), flag=wx.LEFT, border=14)
        bs.Add(self.authorText, pos=(7,0), flag=wx.LEFT, border=14)
        bs.Add(self.timeText, pos=(8,0), flag=wx.LEFT, border=14)

        panel.SetSizerAndFit(bs)

        loadButton.Bind(wx.EVT_BUTTON, self.LoadFile, loadButton)
        SolveLoaded.Bind(wx.EVT_BUTTON, self.Solve, SolveLoaded)
        randomButton.Bind(wx.EVT_BUTTON, self.RandomTour, randomButton)
        saveButton.Bind(wx.EVT_BUTTON, self.SaveDB, saveButton)
        LoadPrevious.Bind(wx.EVT_BUTTON, self.LoadDatabase, LoadPrevious)
        
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
            a.scatter(x, y, color="r", s=21)       
            a.plot(x, y, "--", linewidth=1)
        else:
            a.plot()
        canvas = FigureCanvas(plotParent, -1, f)
        a.grid(ls='--')
        canvas.draw()
        
    def onClose(self, e):
        self.Destroy()
        
    def Quit(self, e):
        dialoge = wx.MessageDialog(None, 'Are your sure you want to quit', 
                                   'Quit',wx.YES_NO)
        if dialoge.ShowModal() == wx.ID_YES:
            self.Destroy()
        else:
            return

    def LoadFile(self, e):
        dialoge = wx.TextEntryDialog(None, '"File Name".tsp', 'Load File')
        if dialoge.ShowModal() == wx.ID_OK:
            self.fileName = dialoge.GetValue()
            fileRead = tsp.consoleFileHandle(self.fileName)
            
            problemName = fileRead[0][6:-1]
            comment = fileRead[1][9:-1]
            problemType = fileRead[4][18:-1]
            dimension = fileRead[3][10:-1]
            self.nameText.SetLabel("Name: " + problemName)
            self.commentText.SetLabel("Comment: " + comment)
            self.typeText.SetLabel("Type: " + problemType)
            self.sizeText.SetLabel("Size: " + dimension + " Nodes")
            self.timeText.SetLabel("Time: " + datetime.datetime.now().strftime("%H:%M:%S"))
            self.dateText.SetLabel("Date: " + datetime.datetime.now().strftime("%Y-%m-%d"))
            
            TSPtour = tsp.generateCities(fileRead)
            self.initialNodes = np.trim_zeros(TSPtour)
            TSPtour = tsp.greedySearch(TSPtour)
            self.coordGenerate(TSPtour)
            self.matPlotInit(self.plotParent, self.xs, self.ys)
            
        dialoge.Destroy()
    
    def Solve(self, e):
        self.matPlotInit(self.plotParent, [],[])
        startTime = time.time()
        try:
            fileRead = tsp.consoleFileHandle(self.fileName)
            TSPtour = tsp.generateCities(fileRead)
            TSPtour = tsp.greedySearch(TSPtour)
        except:
            TSPtour = self.initialNodes 
            
        solveTime = int(self.solveTimeBox.GetValue())
  
        while time.time() < (startTime + int(solveTime)):
            TSPtour = tsp.greedyTwoOptSolver(TSPtour)
  
        ''' threading to handle unresponsive window  
        t = threading.Thread(target = self.solverThread, args=(TSPtour, startTime, solveTime))
        self.threads.append(t)
        t.start()
        t.join()
        '''
      
        self.coordGenerate(TSPtour)
        self.matPlotInit(self.plotParent, self.xs, self.ys)
        self.tourDistance = tsp.totalDistance(TSPtour)
        self.lengthText.SetLabel("Length: " + str(self.tourDistance))
        self.tourString = tsp.TourToString(TSPtour)
    
    ''' 
    def solverThread(self, TSPtour, startTime, solveTime):
        while time.time() < (startTime + int(solveTime)):
            tsp.greedyTwoOptSolver(TSPtour) 
    '''
        
        
    def RandomTour(self, e):
        nTowns = int(self.randomInput.GetValue())
        x = random.sample(range(0,1000), nTowns)
        y = random.sample(range(0,1000), nTowns)
        
        self.matPlotInit(self.plotParent, x,y)
        
    def coordGenerate(self, totalList):
        self.xs.clear()
        self.ys.clear()
        for i in range(0, len(totalList)):
            self.xs.append(totalList[i][1])
            self.ys.append(totalList[i][2])
            
    def LoadDatabase(self, e):
        sqlCommand = "SELECT Name FROM Problem;"
        self.cursor.execute(sqlCommand)
        dbProblems = self.cursor.fetchall()
        
        self.LoadDialog = wx.Dialog(None, title="Problems", size =(200,120))
        button = wx.Button(self.LoadDialog, pos=(4, 40), label="Ok")
        self.listBox = wx.ComboBox(self.LoadDialog)
        
        button.Bind(wx.EVT_BUTTON, self.okButton, button)
        
        for i in range(0, len(dbProblems)):
            self.listBox.Append(dbProblems[i])
        
        self.LoadDialog.ShowModal()
        self.LoadDialog.Center()
        self.LoadDialog.Destroy()
        
    def okButton(self, e):
        name = self.listBox.GetString(self.listBox.GetSelection())
        self.fileName = name
        
        self.nameText.SetLabel("Name: " + name)
        self.cursor.execute("SELECT Size FROM Problem WHERE(Name='" + name + "');")
        size = self.cursor.fetchone()[0]
        self.sizeText.SetLabel("Size: " + str(size))
        
        self.cursor.execute("SELECT Comment FROM Problem WHERE(Name='" + name + "');")
        self.commentText.SetLabel("Comment: " + str(self.cursor.fetchone()[0]))
        
        self.cursor.execute("SELECT TourLength FROM Solution WHERE(ProblemName='" + name + "');")
        
        try:
            self.lengthText.SetLabel("Length: " + str(self.cursor.fetchone()[0]))
        except:
            print('Exception: No Problem Length found')    
    
        
        self.cursor.execute("SELECT Author FROM Solution WHERE(ProblemName='" + name + "');")
        
        try:
            self.authorText.SetLabel("Author: " + str(self.cursor.fetchone()[0]))
        except:
            print('Exception: Author not found')
        
        self.cursor.execute("SELECT ID, x, y FROM Cities WHERE(Name='" + name + "');") 
        self.initialNodes = self.cursor.fetchall()
        
        self.coordGenerate(self.initialNodes)
        self.matPlotInit(self.plotParent, self.xs, self.ys)
        
                                                                   
        
    def SaveDB(self, e):       
        name = None
        problem = None
        
        try:
            name = self.nameText.Label.split()[1].strip()
            size = self.sizeText.Label.split()[1].strip()
            comment = self.commentText.Label.split(":")[1].strip()
        except:
            print("Exception: Could not Save problem due to issues with naming")
        
        try:
            date = self.dateText.Label.split()[1].strip()
        except:
            print("Could not save date")
            date = ""
               
        author = wx.TextEntryDialog(None, "Enter Author Name", "Author Text")
        if author.ShowModal() == wx.ID_OK:
            author = author.GetValue()
        runTime = self.solveTimeBox.GetValue()
        tour = self.tourString
        
        try:
            Length = self.lengthText.Label.split()[1].strip()
        except:
            Length = ""
        
        if name is not None:
            sqlCommand = "SELECT Name FROM Problem WHERE(Name = '" + name + "');"
            self.cursor.execute(sqlCommand)
            problem = self.cursor.fetchall()
        
        if problem == []:
            sqlCommand = "INSERT INTO Problem(Name,Size,Comment) VALUES('" + name + "','" + size + "','" + comment + "');"
            self.cursor.execute(sqlCommand)
            self.connection.commit()
            dialog = wx.MessageDialog(None, "Problem Saved to the database", "Saved")
            dialog.ShowModal()
            self.saveCities(name)

        if Length != "":
            sqlCommand = "INSERT INTO Solution(ProblemName,TourLength,Date,Author,RunningTime,Tour,Algorithm)" + "VALUES('" + name + "','" + Length + "','" + date + "','" + author + "','" + runTime + "','" + tour +"','2Opt');"
            self.cursor.execute(sqlCommand)
            self.connection.commit()
            dialog = wx.MessageDialog(None, "New Solution Saved to Database", "Saved")
            dialog.ShowModal()
            
    def saveCities(self, name):
        tour = self.initialNodes
         
        for i in range(0, len(tour)):
            sqlCommand = "INSERT INTO Cities(Name,ID,x,y) VALUES('" + name + "','" + str(tour[i][0]) + "','" + str(tour[i][1]) + "','" + str(tour[i][2]) + "');"
            self.cursor.execute(sqlCommand)
            self.connection.commit()
             
        

app = wx.App()

fileRead = None
TSPtour = None

problemName = ""
comment = ""
problemType = ""
dimension = ""

TSPGUIClass(None, title='TSP Solver')
app.MainLoop()    
