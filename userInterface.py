from tkinter import *
#creates file menu, menu items, and defines their commands
def fileMenu(self):
    self.fileMenu = Menu(self.menuBar, tearoff = 0)
    self.menuBar.add_cascade(label = 'File', menu=self.fileMenu)
    self.fileMenu.add_command(label = 'Import image...')

#creates edit menu, menu items, and defines their commands
def editMenu(self):
    self.editMenu = Menu(self.menuBar, tearoff = 0)
    self.menuBar.add_cascade(label = 'Edit', menu=self.editMenu)
    self.editMenu.add_command(label = 'Preferences...')

#creates help menu, menu items, and defines their commands
def helpMenu(self):
    self.helpMenu = Menu(self.menuBar, tearoff = 0)
    self.menuBar.add_cascade(label = 'Help', menu=self.helpMenu)
    self.helpMenu.add_command(label = 'About')

def sheetArea(self):
    self.sheetFrame = Frame(self, borderwidth = 2, relief = GROOVE)
    self.sheetFrame.grid(column = 0, row = 0)
    self.sheetDisplay = Canvas(self.sheetFrame, height=320, width=320, borderwidth = 5, relief = SUNKEN, bg='#FFFFFF')
    self.sheetDisplay.grid()
    self.sheetLabel = Label(self.sheetFrame, text = "Sheet View")
    self.sheetLabel.grid()

def tileArea(self):
    self.tileFrame = Frame(self, borderwidth = 2, relief = GROOVE)
    self.tileFrame.grid(column =1, row = 0)
    self.tileDisplay = Canvas(self.tileFrame, height = 320, width = 320, borderwidth = 5, relief = SUNKEN, bg = '#FFFFFF')
    self.tileDisplay.grid()
    self.tileLabel = Label(self.tileFrame, text = "Tile View")
    self.tileLabel.grid()
    tileDisplay.

class BMP2GBGui(Frame):
    def __init__ (self, master=None):
        Frame.__init__(self, master, width=800, height = 600, bg='#F0F0F0')
        self.grid_propagate(0)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        #setting top level window to a variable
        TLW = self.winfo_toplevel()

        #Creating menu along top of window
        self.menuBar = Menu(TLW)
        TLW['menu'] = self.menuBar

        #call functions to create menus
        fileMenu(self)
        editMenu(self)
        helpMenu(self)

        #create canvases for sheet and tile views
        sheetArea(self)
        tileArea(self)
#Testin
BMP2GB = BMP2GBGui()
BMP2GB.master.title('Bitmap 2 Gameboy')
BMP2GB.mainloop()