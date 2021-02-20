from nge import Character, Sheet, Book, create_2d_array
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
def view_grid_generator(canvas, x, y):
    row = 0
    column = 0
    rectangles = create_2d_array(x, y)
    while(row < x):
        canvas.create_rectangle(row*33, column*33, row*33+33, column*33+33, )
        column += 1
        if (column == y):
            column = 0
            row += 1
        
def create_color_canvas(self, frame, color):
    #self.tile_display = Canvas(self.tile_frame, height = 266, width = 266, bg = '#FFFFFF', borderwidth = 0, highlightthickness=0)
    self.tile_display = Canvas(frame, height = 32, width = 32, bg = color, borderwidth = 3, relief = 'sunken')
    return self.tile_display

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
def file_menu(self):
    self.file_menu = Menu(self.menu_bar, tearoff = 0)
    self.sheets_menu = Menu(self.file_menu, tearoff=0)
    self.file_menu.add_cascade(label = 'Sheets', menu=self.sheets_menu)
    self.menu_bar.add_cascade(label = 'File', menu=self.file_menu)
    self.file_menu.add_command(label = 'Save')
    self.file_menu.add_command(label = 'Save As...')
    self.file_menu.add_command(label = 'Import image...')
    self.file_menu.add_command(label = "Quit", command=self.quit)

    #creates sheet cascade, adds to file menu
    self.sheets_menu.add_command(label = 'New Sheet')
    self.sheets_menu.add_command(label = 'Open Sheet...')
    self.sheets_menu.add_command(label = 'Delete Sheet...')

#creates edit menu, menu items, and defines their commands
def edit_menu(self):
    self.edit_menu = Menu(self.menu_bar, tearoff = 0)
    self.menu_bar.add_cascade(label = 'Edit', menu=self.edit_menu)
    self.edit_menu.add_command(label = 'Preferences...')

#creates help menu, menu items, and defines their commands
def help_menu(self):
    self.help_menu = Menu(self.menu_bar, tearoff = 0)
    self.menu_bar.add_cascade(label = 'Help', menu=self.help_menu)
    self.help_menu.add_command(label = 'About')
############################################################
####                  END MENU SECTION                  ####
############################################################

####                   FRAME SECTION                    ####
#                                                          #
#   This section will define menus and link their          #
#   options to the methods that make them work.            #
#                                                          #
############################################################
def create_frames(self):
    self.sheet_frame = LabelFrame(self, labelanchor = 's', borderwidth = 2, text = "Sheet View", padx=5, pady=5)
    self.sheet_frame.grid(column = 0, row=0, padx=5, pady=5, sticky = 'n')

    self.tile_frame = LabelFrame(self, labelanchor = 's', borderwidth = 2, text = 'Character View', padx=5, pady=5)
    self.tile_frame.grid(column = 1, row = 0, padx = 5, pady = 5, sticky = 'n')

    self.tool_frame = LabelFrame(self, labelanchor = 's', borderwidth = 2, text = 'Tools', padx = 5, pady = 5)
    self.tool_frame.grid(column = 2, row = 0, padx=5, pady=5, sticky = 'n')

    self.color_frame = LabelFrame(self, labelanchor = 's', borderwidth = 2, text = 'Colors', padx=5, pady=5)
    self.color_frame.grid(column = 3, row = 0, padx=5, pady=5, sticky = 'n')
    self.current_color_frame = LabelFrame(self.color_frame, labelanchor='n', borderwidth = 0, text='Current', padx = 5, pady = 5)
    self.current_color_frame.grid()
    self.palette_frame = LabelFrame(self.color_frame, labelanchor = 'n', borderwidth = 0, text= 'Palette', padx=5, pady=5)
    self.palette_frame.grid()
############################################################
####                  END FRAME SECTION                 ####
############################################################

####                   WIDGET SECTION                   ####
#                                                          #
#   This section will define menus and link their          #
#   options to the methods that make them work.            #
#                                                          #
############################################################
def sheet_area(self):
    self.sheet_display = Canvas(self.sheet_frame, height=266, width=530, bg='#FFFFFF', border=0, borderwidth = 0, highlightthickness=0)
    self.sheet_display.grid(sticky = 's')
    view_grid_generator(self.sheet_display, 16, 8)
        
def tile_area(self):
    self.tile_display = Canvas(self.tile_frame, height = 266, width = 266, bg = '#FFFFFF', borderwidth = 0, highlightthickness=0)
    self.tile_display.grid()
    row = 0
    column = 0
    characters=[]
    view_grid_generator(self.tile_display, 8, 8)

def tool_area(self):
    self.pencil_image = BitmapImage(file='pencil.xbm', foreground ='black', background='white')
    self.eraser_image = BitmapImage(file='eraser.xbm', foreground = 'black', background = 'white')
    self.bucket_image = BitmapImage(file = 'bucket.xbm', foreground = 'black', background = 'white')
    self.pencil_button = Button(self.tool_frame, image=self.pencil_image, width=64, height=64)
    self.pencil_button.grid()
    self.eraser_button = Button(self.tool_frame, image=self.eraser_image, width=64, height = 64)
    self.eraser_button.grid()
    self.bucket_button = Button(self.tool_frame, image = self.bucket_image, width = 64, height = 64)
    self.bucket_button.grid()
    
def color_area(self):
    self.black_swatch = create_color_canvas(self, self.palette_frame, '#000000')
    self.black_swatch.grid(pady=5)
    self.dk_gray_swatch = create_color_canvas(self, self.palette_frame, '#575757')
    self.dk_gray_swatch.grid(pady=5)
    self.lt_gray_swatch = create_color_canvas(self, self.palette_frame, '#ababab')
    self.lt_gray_swatch.grid(pady=5)
    self.white = create_color_canvas(self, self.palette_frame, '#ffffff')
    self.white.grid(pady=5)
    self.current_color = create_color_canvas(self, self.current_color_frame, '#ffffff')
    self.current_color.grid()
############################################################
####                 END WIDGET SECTION                 ####
############################################################
            
class BMP2GBGui(Frame):
    def __init__ (self, master=None):
        Frame.__init__(self, master, width=1024, height = 512, bg='#F0F0F0')
        self.grid_propagate(0)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        #setting top level window to a variable
        TLW = self.winfo_toplevel()

        #Creating menu along top of window
        self.menu_bar = Menu(TLW)
        TLW['menu'] = self.menu_bar

        #call functions to create menus
        file_menu(self)
        edit_menu(self)
        help_menu(self)

        #call function to create frams
        create_frames(self)

        #create canvases for sheet and tile views
        sheet_area(self)
        tile_area(self)
        tool_area(self)

        color_area(self)
#Testin
BMP2GB = BMP2GBGui()
BMP2GB.master.title('Bitmap 2 Gameboy')
BMP2GB.mainloop()