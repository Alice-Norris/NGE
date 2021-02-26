from nge import Character, Sheet, Workspace, Tool, Book #import classes from nge
from nge import create_2d_array #import functions from nge
from tkinter import *
          
class BMP2GBGui(Frame):
    #Constructor, calls scripts to create GUI
    def __init__ (self, master=None):
        #setting top level window to a variable
        Frame.__init__(self, master, width=1024, height = 768, bg='#F0F0F0')
        self.TLW = self.winfo_toplevel()
        self.grid_propagate(0)
        self.grid()
        
        #create Tool objects
        self.Pencil = Tool('pencil', '@pencil.xbm')
        self.Bucket = Tool('bucket', '@bucket.xbm')
        self.Eraser = Tool('eraser', '@eraser.xbm')
        self.Select = Tool('none', '@empty.xbm')

        #Create temporary objects for workspace
        self.tempBook = Book("testing")
        self.tempSheet = Sheet(0, self.tempBook)
        self.tempBook.add_sheet(self.tempSheet)
        self.tempChar = Character(0 , self.tempSheet)

        #Create Workspace object
        self.workspace = Workspace(self.Select)
        self.workspace.current_character = self.tempChar
        self.workspace.current_sheet=self.tempSheet
        self.workspace.current_book=self.tempBook

        #Creating menu along top of window
        self.create_menu(self.TLW)
        
        #Creates different areas of the GUI
        self.sheet_area()    #populates sheet frame
        self.tile_area()     #populates tile frame
        self.tool_area()     #populates tool frame 
        self.color_area()    #populate color frame with available colors and current color tools
        self.text_area()
    
    #######################
    ###HANDLER FUNCTIONS###
    #######################
    def mouse_over_tile_display(self, event):
        cursor_image = self.workspace.current_tool.tool_bitmap
        tile_display_x= self.tile_display.canvasx(event.x)
        tile_display_y = self.tile_display.canvasx(event.y)
        print(tile_display_x, " ", tile_display_y)
        print(self.workspace.current_tool.tool_bitmap)
        if(not self.tile_display.find_withtag(65)):
            self.tile_display.create_bitmap(tile_display_x - 36, tile_display_y - 36, bitmap = cursor_image)
        else:
            self.tile_display.itemconfigure(65, bitmap = cursor_image)
            pencil_coords = self.tile_display.coords(65)
            self.tile_display.move(65, event.x - pencil_coords[0] - 36, event.y - pencil_coords[1] - 36)

    def mouse_left_tile_display(self, event):
        self.tile_display.itemconfigure(65, bitmap = '@empty.xbm')

    def tile_display_clicked(self, event):
        click_x = self.tile_display.canvasx(event.x)
        click_y = self.tile_display.canvasy(event.y)
        print(click_x, " ", click_y)
        clicked_rectangle = self.tile_display.find_closest(click_x, click_y)[0]
        print(clicked_rectangle)
        self.tile_display.itemconfigure(clicked_rectangle, fill=self.workspace.current_color)
        character_pixel = int(click_x//33), int(click_y//33)
        self.workspace.current_character.data[character_pixel[0]][character_pixel[1]] = self.workspace.current_color
        for row in self.workspace.current_character.data:
            print(row)

    def sheet_display_clicked(self, event):
        click_x = self.tile_display.canvasx(event.x)
        click_y = self.tile_display.canvasy(event.y)
        print(click_x, " ", click_y)
        clicked_rectangle = self.sheet_display.find_closest(click_x, click_y)[0]
        print(clicked_rectangle)

    def select_tool(self, event):
        selected_tool = event.widget.winfo_name()
        if selected_tool == 'select':
            self.workspace.current_tool = self.Select
        elif selected_tool == 'pencil':
            self.workspace.current_tool = self.Pencil
        elif selected_tool == 'eraser':
            self.workspace.current_tool = self.Eraser
        elif selected_tool == 'bucket':
            self.workspace.current_tool = self.Bucket

    def set_current_color(self, event):
        color=event.widget.itemcget(1, "fill")
        self.current_color.itemconfigure(1, fill=color)
        self.workspace.current_color = color
    ###########################
    ###END HANDLER FUNCTIONS###
    ###########################
    
    ###################
    ###GUI FUNCTIONS###
    ###################
    def create_canvas_rectangles(self, canvas, x, y):
        row = 0
        column = 0
        while(column < y):
            canvas.create_rectangle(row*33, column*33, row*33+33, column*33+33, fill='#ffffff')
            row += 1
            if (row == x):
                row= 0
                column += 1

    def create_color_canvas(self, frame, color):
        #self.tile_display = Canvas(self.tile_frame, height = 266, width = 266, bg = '#FFFFFF', borderwidth = 0, highlightthickness=0)
        self.color_canvas = Canvas(frame, height = 32, width = 32, borderwidth = 3, relief = 'sunken')
        self.color_canvas.create_rectangle(37, 37, 0, 0, fill = color)
        return self.color_canvas

    def convert_character_to_hex(self):
        pixels = self.tile_display.find_all()
        hex_data = []
        firstbyte = ""
        secondbyte = ""
        row_hex = ""
        index = 0
        for pixel in pixels:
            color = self.tile_display.itemcget(pixel, "fill")
            if color == "#ffffff":
                firstbyte += "0"
                secondbyte += "0"
            elif color == "#ababab":
                firstbyte += "1"
                secondbyte += "0"
            elif color == "#575757":
                firstbyte += "0"
                secondbyte += "1"
            elif color == "#000000":
                firstbyte += "1"
                secondbyte += "1"

            if (pixel % 8 == 0):
                row_upper = hex(int(firstbyte, 2))
                row_lower = hex(int(secondbyte, 2))
                firstbyte=""
                secondbyte=""
            

    #######################
    ###END GUI FUNCTIONS###
    #######################

    ######################
    ###WIDGET FUNCTIONS###
    ######################
    def create_menu(self, TLW):
        #Creating menu along top of window
        self.menu_bar = Menu(TLW)
        TLW['menu'] = self.menu_bar

        #creates file menu
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
        self.edit_menu = Menu(self.menu_bar, tearoff = 0)
        self.menu_bar.add_cascade(label = 'Edit', menu=self.edit_menu)
        self.edit_menu.add_command(label = 'Preferences...')

        #creates help menu, menu items, and defines their commands
        self.help_menu = Menu(self.menu_bar, tearoff = 0)
        self.menu_bar.add_cascade(label = 'Help', menu=self.help_menu)
        self.help_menu.add_command(label = 'About')

    def sheet_area(self):
        self.sheet_frame = LabelFrame(self, labelanchor = 's', borderwidth = 2, text = "Sheet View", padx=5, pady=5)
        self.sheet_frame.grid(column = 0, row=0, padx=5, pady=5, sticky = 'n')
        self.sheet_display = Canvas(self.sheet_frame, height=266, width=530, bg='#FFFFFF', border=0, borderwidth = 0, highlightthickness=0, cursor='tcross')
        self.sheet_display.grid(sticky = 's')
        self.sheet_display.bind('<ButtonRelease>', self.sheet_display_clicked)
        self.create_canvas_rectangles(self.sheet_display, 16, 8)
        self.sheet_label = Label(self.sheet_frame, text="Book: " + self.workspace.current_book.book_name + "\nSheet: " + str(self.workspace.current_sheet.sheet_num))
        self.sheet_label.grid()
            
    def tile_area(self):
        self.tile_frame = LabelFrame(self, labelanchor = 's', borderwidth = 2, text = 'Character View', padx=5, pady=5)
        self.tile_frame.grid(column = 1, row = 0, padx = 5, pady = 5, sticky = 'n')

        self.tile_display = Canvas(self.tile_frame, height = 266, width = 266, bg = '#FFFFFF', borderwidth = 0, highlightthickness=0)
        self.tile_display.bind('<Motion>', self.mouse_over_tile_display)
        self.tile_display.bind('<Leave>', self.mouse_left_tile_display)
        self.tile_display.bind('<ButtonRelease>', self.tile_display_clicked)
        self.tile_display.grid()
        self.character_label = Label(self.tile_frame, text="Character: " + str(self.workspace.current_character.object_num))
        self.character_label.grid()  
        self.create_canvas_rectangles(self.tile_display, 8, 8)

    def tool_area(self):
        self.tool_frame = LabelFrame(self, labelanchor = 's', borderwidth = 2, text = 'Tools', padx = 5, pady = 5)
        self.tool_frame.grid(column = 2, row = 0, padx=5, pady=5, sticky = 'n')
        self.select_button = Button(self.tool_frame, name = 'select', bitmap='@select.xbm', width = 64, height = 64)
        self.select_button.bind('<ButtonRelease>', self.select_tool)
        self.select_button.grid()
        self.pencil_button = Button(self.tool_frame, name = 'pencil', bitmap='@pencil.xbm', width=64, height=64)
        self.pencil_button.bind('<ButtonRelease>', self.select_tool)
        self.pencil_button.grid()
        self.eraser_button = Button(self.tool_frame, name = 'eraser', bitmap='@eraser.xbm', width=64, height = 64)
        self.eraser_button.bind('<ButtonRelease>', self.select_tool)
        self.eraser_button.grid()
        self.bucket_button = Button(self.tool_frame, name = 'bucket', bitmap='@bucket.xbm', width = 64, height = 64)
        self.bucket_button.bind('<ButtonRelease>', self.select_tool)
        self.bucket_button.grid()

    def color_area(self):
        self.color_frame = LabelFrame(self, labelanchor = 's', borderwidth = 2, text = 'Colors', padx=5, pady=5)
        self.color_frame.grid(column = 3, row = 0, padx=5, pady=5, sticky = 'n')

        self.palette_frame = LabelFrame(self.color_frame, labelanchor = 'n', borderwidth = 0, text= 'Palette', padx=5, pady=5)
        self.palette_frame.grid()

        self.current_color_frame = LabelFrame(self.color_frame, labelanchor='n', borderwidth = 0, text='Current', padx = 5, pady = 5)
        self.current_color_frame.grid()

        self.black_swatch = self.create_color_canvas(self.palette_frame, '#000000')
        self.black_swatch.grid(pady=5)
        self.black_swatch.bind('<ButtonRelease>', self.set_current_color)

        self.dk_gray_swatch = self.create_color_canvas(self.palette_frame, '#575757')
        self.dk_gray_swatch.grid(pady=5)
        self.dk_gray_swatch.bind('<ButtonRelease>', self.set_current_color)

        self.lt_gray_swatch = self.create_color_canvas(self.palette_frame, '#ababab')
        self.lt_gray_swatch.grid(pady=5)
        self.lt_gray_swatch.bind('<ButtonRelease>', self.set_current_color)

        self.white = self.create_color_canvas(self.palette_frame, '#ffffff')
        self.white.grid(pady=5)
        self.white.bind('<ButtonRelease>', self.set_current_color)

        self.current_color = self.create_color_canvas(self.current_color_frame, '#ffffff')
        self.current_color.grid()

    def text_area(self):
        self.text_frame = LabelFrame(self, labelanchor='s', borderwidth = 2, text = 'Hex Data', padx = 5, pady = 5)
        self.text_frame.grid(column=0, row = 1, padx=5, pady=5, sticky='w', columnspan = 5)
        self.hex_display = Text(self.text_frame, width=53, height=16)
        characters = self.sheet_display.find_all()
        for character in characters:
            index =  str(character) + '.0'
            print(index)
            string = str(character).zfill(3) + ' |\n'
            self.hex_display.insert(index, string)
        self.hex_display.grid()
    ##########################
    ###END WIDGET FUNCTIONS###
    ##########################

NGE = BMP2GBGui()
NGE.master.title('Nintendo Graphics Editor')
NGE.convert_character_to_hex()
NGE.mainloop()