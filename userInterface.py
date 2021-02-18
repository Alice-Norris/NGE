from NGEfunc import *
from tkinter import *
####                   FUNCTION SECTION                 ####
#                                                          #
#   This section contains functions that help the          #
#   GUI work. Any function that does not place a           #
#   widget but provides GUI functionality should           #
#   be placed in here.                                     #
############################################################

#this function fills the view canvases with rectangles.
#x defines the number of rectangles across to be drawn across
#y defines the number of rectangles to be drawn down
def viewGridGenerator(canvas, x, y):
    row = 0
    column = 0
    rectangles = 0
    while(row < x):
        canvas.create_rectangle(row*33, column*33, row*33+33, column*33+33)
        column += 1
        if (column == y):
            column = 0
            row += 1
            
############################################################
####                END FUNCTION SECTION                ####
############################################################

####                    MENU SECTION                    ####
#                                                          #
#   This section will define menus and link their          #
#   options to the methods that make them work.            #
#                                                          #
############################################################

#creates file menu, menu items, and defines their commands
def fileMenu(self):
    self.fileMenu = Menu(self.menuBar, tearoff = 0)
    self.menuBar.add_cascade(label = 'File', menu=self.fileMenu)
    self.fileMenu.add_command(label = 'Save')
    self.fileMenu.add_command(label = 'Save As...')
    self.fileMenu.add_command(label = 'Import image...')
    self.fileMenu.add_command(label = 'Open Sheet ...')
    self.fileMenu.add_command(label = "Quit", command=self.quit)

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
############################################################
####                    END MENU SECTION                ####
############################################################

def sheetArea(self):
    self.sheetFrame = LabelFrame(self, labelanchor = 's', borderwidth = 2, text = "Sheet View", padx=5, pady=5)
    self.sheetFrame.grid(column = 0, row=0, padx=5, pady=5)
    self.sheetDisplay = Canvas(self.sheetFrame, height=266, width=530, bg='#FFFFFF', border=0, borderwidth = 0, highlightthickness=0)
    self.sheetDisplay.grid(sticky = 's')
    self.sheetDisplay.grid_propagate(0)
    viewGridGenerator(self.sheetDisplay, 16, 8)
        
def tileArea(self):
    self.tileFrame = LabelFrame(self, labelanchor = 's', borderwidth = 2, text = 'Tile View', padx=5, pady=5)
    self.tileFrame.grid(column = 1, row = 0, padx = 5, pady = 5)
    self.tileDisplay = Canvas(self.tileFrame, height = 266, width = 266, bg = '#FFFFFF', borderwidth = 0, highlightthickness=0)
    self.tileDisplay.grid()
    row = 0
    column = 0
    characters=[]
    viewGridGenerator(self.tileDisplay, 8, 8)

            
class BMP2GBGui(Frame):
    def __init__ (self, master=None):
        Frame.__init__(self, master, width=1024, height = 512, bg='#F0F0F0')
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