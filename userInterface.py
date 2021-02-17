from tkinter import *

class BMP2GBGui(Frame):
    def __init__ (self, master=None):
        Frame.__init__(self, master, height = 640, width=480)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        #setting top level window to a variable
        TLW = self.winfo_toplevel()

        #Creating menu along top of window
        self.menuBar = Menu(TLW)
        TLW['menu'] = self.menuBar
        self.fileMenu = Menu(self.menuBar)
        self.menuBar.add_cascade(label = 'File', menu=self.fileMenu)
        self.fileMenu.add_command(label = 'Import image...')
        #create general program frame
        self.programFrame = Frame(self, height = 640, width = 480)
        self.programFrame.grid(column = 0, row = 0)

        #This will be the area where the image is displayed
        self.imageArea = Canvas(self.programFrame, height=320, width=320, borderwidth = 5, relief = SUNKEN, bg='#FFFFFF')
        self.imageArea.grid()

        #This label 
        self.imageAreaLabel = Label(self.programFrame, text = "Image Area", borderwidth = 2, relief=GROOVE)
        self.imageAreaLabel.grid()

#Testin
BMP2GB = BMP2GBGui()
BMP2GB.master.title('Bitmap 2 Gameboy')
BMP2GB.mainloop()