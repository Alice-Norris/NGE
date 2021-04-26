from nge_functions import character_to_hex, character_row_to_hex, update_character_data #import functions from nge
from nge_const import NGE_BLACK, NGE_DK_GRAY, NGE_LT_GRAY, NGE_WHITE, COLOR_DICT, REVERSE_COLOR_DICT
from tkinter import *
from math import ceil, floor
from nge_classes import Character, Sheet, Book, Shelf, Tool
class NGE:
    def __init__(cls):
        #Create working objects for NGE instance
        cls.currentShelf = Shelf("unsaved")
        cls.currentBook = Book("unsaved")
        cls.currentSheet = Sheet(0, "unsaved", cls.currentBook)
        cls.currentChar = cls.currentSheet.char_list[0]
        cls.currentBook.add_sheet(cls.currentSheet)
        character_to_hex(cls.currentChar)
        
        #create Tool objects
        cls.Select = Tool('none', '@empty.xbm')
        cls.Pencil = Tool('pencil', '@pencil.xbm')
        cls.Bucket = Tool('bucket', '@bucket.xbm')
        cls.Eraser = Tool('eraser', '@eraser.xbm')

class nge_interface(Frame):
    #Constructor, calls functions to create GUI
    def __init__ (self, master=None):
        #setting top level window to a variable
        self.NGE = NGE()
        Frame.__init__(self, master, width=1024, height = 768, bg='#F0F0F0')
        self.TLW = self.winfo_toplevel()
        self.grid_propagate(0)
        self.grid()
        self.TLW.title("Nintendo Graphics Editor")
        #Creating menu along top of window
        self.create_menu(self.TLW)
        
        #Creates different areas of the GUI
        self.sheet_area()    #populates sheet frame
        self.tile_area()     #populates tile frame
        self.tool_area()     #populates tool frame 
        self.color_area()    #populate color frame with available colors and current color tools
        self.text_area()

        #create variables for UI
        self.current_tool = self.NGE.Select
        self.current_color = self.current_color_swatch.cget('bg')

        #create grids in sheet and character canvases
        self.create_canvas_rectangles(self.tile_display)
        self.create_canvas_rectangles(self.sheet_display)
        self.create_sheet_display_pixels()

    ###################
    ###GUI FUNCTIONS###
    ###################
    def create_canvas_rectangles(self, canvas):
        row = 0
        column = 0
        while(column < floor(int(canvas.cget('height')) / 33)):
            canvas.create_rectangle(row*33, column*33, row*33+33, column*33+33, tags="grid", fill = "#ffffff")
            row += 1
            if (row == floor(int(canvas.cget('width')) / 33)):
                row= 0
                column += 1
        
    def text_area_setup(self):
        grid = self.sheet_display.find_all()
        hex_loc = 0
        header = "       0"
        line_num = 2
        while len(header) < self.hex_display.cget('width'):
            header += "  " + hex(hex_loc + 1)[2:4]
            hex_loc += 1
        self.hex_display.insert('1.0', header + '\n')
        for character in self.NGE.currentSheet.char_list:
            hex_line = ""
            line_index = 5
            byte_num = 0
            index = str(line_num) + "." + str(line_index)
            character_data = character_to_hex(character)
            self.hex_display.insert(str(line_num) + ".0", str(hex(character.obj_num)).rjust(4) + "|")
            while(byte_num < 32):
                if(byte_num < 32):
                    hex_line += " " + (character_data[byte_num : byte_num + 2])
                elif (byte_num == 32):
                    hex_line += (character_data[byte_num : byte_num + 2])
                byte_num += 2
            self.hex_display.insert(index, hex_line + "\n")
                
            
            line_num += 1

    def create_sheet_display_pixels(self):
        characters = self.sheet_display.find_all()
        for character in self.NGE.currentSheet.char_list:
            coords = self.sheet_display.coords(character.obj_num+1)
            pixel_start_x = int(coords[0]+1)
            pixel_start_y = int(coords[1]+1)
            character = self.NGE.currentSheet.char_list[0]
            row = 0
            column = 0
            pixel_num = 0
            while(row <= 7):
                pixel_num = floor(row / 8) + column
                pixel_value = character.data[pixel_num]
                fill_color = REVERSE_COLOR_DICT[pixel_value]
                self.sheet_display.create_rectangle(pixel_start_x, pixel_start_y, 
                                                    pixel_start_x+3, pixel_start_y + 3, 
                                                    fill = fill_color, outline = fill_color, 
                                                    width = 1, tags = str(character.obj_num) + " pixels")
                pixel_start_x += 4
                column += 1
                if(column == 8):
                    pixel_start_x = int(coords[0]+1)
                    column = 0
                    pixel_start_y += 4
                    row += 1

    def update_sheet_display_pixels(self, pixel, color):
        character = self.NGE.currentChar
        sheet_tile = character.obj_num + 1
        sheet_tile_coords = self.sheet_display.coords(sheet_tile)
        sheet_tile_pixels = self.sheet_display.find_overlapping(sheet_tile_coords[0] + 1, sheet_tile_coords[1] + 1, sheet_tile_coords[2] - 1, sheet_tile_coords[3] - 1)
        self.sheet_display.itemconfigure(sheet_tile_pixels[pixel], fill = color, outline = color)

    def update_tile_display_pixels(self):
        tile_display_pixels = self.tile_display.find_all()
        character_pixels = self.NGE.currentChar.data
        index = 0
        while(index < len(character_pixels)):
            pixel_color = character_pixels[index]
            self.tile_display.itemconfig(index + 1, fill = REVERSE_COLOR_DICT[pixel_color])
            index += 1

    def update_text_area(self):
        character = self.NGE.currentChar
        character_data = character.data
        hex_line = ""
        byte_num = 0
        start_index = str(character.obj_num + 2) + ".5"
        end_index = str(character.obj_num + 2) + ".53"
        character_data = character_to_hex(character)
        while(byte_num < 32):
            if(byte_num < 32):
                hex_line += " " + (character_data[byte_num : byte_num + 2])
            elif (byte_num == 32):
                hex_line += (character_data[byte_num : byte_num + 2])
            byte_num += 2
        self.hex_display.replace(start_index, end_index, hex_line)

            
            
    #######################
    ###HANDLER FUNCTIONS###
    #######################
    def color_swatch_clicked(self, event):
        self.current_color_swatch.configure(bg = event.widget.cget('bg'))
        self.current_color = event.widget.cget('bg')

    def tool_button_clicked(self, event):
        clicked_tool = event.widget.winfo_name()
        if (clicked_tool == 'select'):
            self.current_tool = self.NGE.Select
        elif (clicked_tool == 'pencil'):
            self.current_tool = self.NGE.Pencil
        elif (clicked_tool == 'eraser'):
            self.current_tool = self.NGE.Eraser
        elif (clicked_tool == 'bucket'):
            self.current_tool = self.NGE.Bucket
        print(self.current_tool.tool_bitmap)

    #makes an image of the current tool follow the mouse cursor
    def mouse_over_tile_display(self, event):
        cursor_image =self.current_tool.tool_bitmap
        tile_display_x= self.tile_display.canvasx(event.x)
        tile_display_y = self.tile_display.canvasx(event.y)
        if(not self.tile_display.find_withtag(65)):
            self.tile_display.create_bitmap(tile_display_x - 36, tile_display_y - 36, bitmap = cursor_image)
        else:
            self.tile_display.itemconfigure(65, bitmap = cursor_image)
            pencil_coords = self.tile_display.coords(65)
            self.tile_display.move(65, event.x - pencil_coords[0] - 36, event.y - pencil_coords[1] - 36)

    #sets bitmap to a transparent bitmap when mouse leaves tile display
    def mouse_left_tile_display(self, event):
        self.tile_display.itemconfigure(65, bitmap = '@empty.xbm')

    #detects when the tile display is clicked and applies the appropriate action given a selected tool
    def tile_display_clicked(self, event):
        click_x = self.tile_display.canvasx(event.x)
        click_y = self.tile_display.canvasy(event.y)
        clicked_rectangle = self.tile_display.find_closest(click_x, click_y, start=1)[0]
        if self.current_tool == self.NGE.Pencil:
            color = self.current_color
            update_character_data(self.NGE.currentChar, self.current_color, clicked_rectangle)
            self.tile_display.itemconfigure(clicked_rectangle, fill = self.current_color_swatch.cget('bg'))
            self.update_sheet_display_pixels(clicked_rectangle, color)
        if self.current_tool == self.NGE.Eraser:
            update_character_data(self.NGE.currentChar, '#ffffff', clicked_rectangle)
            self.tile_display.itemconfigure(clicked_rectangle, fill = NGE_WHITE)
            self.update_sheet_display_pixels(clicked_rectangle, '#ffffff')
        character_to_hex(self.NGE.currentChar)
        self.update_text_area()
    
    def sheet_display_clicked(self, event):
        click_x = self.sheet_display.canvasx(event.x)
        click_y = self.sheet_display.canvasy(event.y)
        clicked_character = self.sheet_display.find_overlapping(click_x, click_y, click_x + 1, click_y + 1)[0]
        self.NGE.currentChar = self.NGE.currentSheet.char_list[clicked_character-1]
        self.update_tile_display_pixels()
        print(self.NGE.currentChar.obj_num)

    ###########################
    ###END HANDLER FUNCTIONS###
    ###########################       


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
        self.sheet_label = Label(self.sheet_frame, text="Sheet View")
        self.sheet_display.bind('<ButtonRelease-1>', self.sheet_display_clicked)
        self.sheet_label.grid()

    def tile_area(self):
        self.tile_frame = LabelFrame(self, labelanchor = 's', borderwidth = 2, text = 'Character View', padx=5, pady=5)
        self.tile_frame.grid(column = 1, row = 0, padx = 5, pady = 5, sticky = 'n')

        self.tile_display = Canvas(self.tile_frame, height = 266, width = 266, bg = '#FFFFFF', borderwidth = 0, highlightthickness=0)
        self.tile_display.bind('<Motion>', self.mouse_over_tile_display)
        self.tile_display.bind('<Leave>', self.mouse_left_tile_display)
        self.tile_display.bind('<ButtonRelease-1>', self.tile_display_clicked)
        self.tile_display.grid()

        self.tile_display_label = Label(self.tile_frame, text = "Object Number: " + str(self.NGE.currentChar.obj_num))
        self.tile_display_label.grid()

    def tool_area(self):
        self.tool_frame = LabelFrame(self, labelanchor = 's', borderwidth = 2, text = 'Tools', padx = 5, pady = 5)
        self.tool_frame.grid(column = 2, row = 0, padx=5, pady=5, sticky = 'n')

        self.select_button = Button(self.tool_frame, name = self.NGE.Select.tool_name, bitmap = '@select.xbm', width = 64, height = 64)
        self.select_button.bind('<ButtonRelease-1>', self.tool_button_clicked)
        self.select_button.grid()
        
        self.pencil_button = Button(self.tool_frame, name = self.NGE.Pencil.tool_name, bitmap=self.NGE.Pencil.tool_bitmap, width=64, height=64)
        self.pencil_button.bind('<ButtonRelease-1>', self.tool_button_clicked)
        self.pencil_button.grid()
        
        self.eraser_button = Button(self.tool_frame, name = self.NGE.Eraser.tool_name, bitmap=self.NGE.Eraser.tool_bitmap, width=64, height = 64)
        self.eraser_button.bind('<ButtonRelease-1>', self.tool_button_clicked)
        self.eraser_button.grid()
        
        self.bucket_button = Button(self.tool_frame, name = self.NGE.Bucket.tool_name, bitmap=self.NGE.Bucket.tool_bitmap, width = 64, height = 64)
        self.bucket_button.bind('<ButtonRelease-1>', self.tool_button_clicked)
        self.bucket_button.grid()

    def color_area(self):
        self.color_frame = LabelFrame(self, labelanchor = 's', borderwidth = 2, text = 'Colors', padx=5, pady=5)
        self.color_frame.grid(column = 3, row = 0, padx=5, pady=5, sticky = 'n')

        self.palette_frame = LabelFrame(self.color_frame, labelanchor = 'n', borderwidth = 0, text= 'Palette', padx=5, pady=5)
        self.palette_frame.grid()

        self.current_color_frame = LabelFrame(self.color_frame, labelanchor='n', borderwidth = 0, text='Current', padx = 5, pady = 5)
        self.current_color_frame.grid()

        self.black_swatch = Canvas(self.palette_frame, height = 32, width = 32, borderwidth = 3, relief = 'sunken', bg = NGE_BLACK)
        self.black_swatch.bind('<ButtonRelease-1>', self.color_swatch_clicked)
        self.black_swatch.grid(pady=5)

        self.dk_gray_swatch = Canvas(self.palette_frame, height = 32, width = 32, borderwidth = 3, relief = 'sunken', bg = NGE_DK_GRAY)
        self.dk_gray_swatch.bind('<ButtonRelease-1>', self.color_swatch_clicked)
        self.dk_gray_swatch.grid(pady=5)
        
        self.lt_gray_swatch = Canvas(self.palette_frame, height = 32, width = 32, borderwidth = 3, relief = 'sunken', bg = NGE_LT_GRAY)
        self.lt_gray_swatch.bind('<ButtonRelease-1>', self.color_swatch_clicked)        
        self.lt_gray_swatch.grid(pady=5)

        self.white_swatch = Canvas(self.palette_frame, height = 32, width = 32, borderwidth = 3, relief = 'sunken', bg = NGE_WHITE)
        self.white_swatch.bind('<ButtonRelease-1>', self.color_swatch_clicked)        
        self.white_swatch.grid(pady=5)

        self.current_color_swatch = Canvas(self.palette_frame, height = 32, width = 32, borderwidth = 3, relief = 'sunken', bg = NGE_WHITE)
        self.current_color_swatch.grid()

    def text_area(self):
        self.text_frame = LabelFrame(self, labelanchor='s', borderwidth = 2, text = 'Hex Data', padx = 5, pady = 5)
        self.text_frame.grid(column=0, row = 1, padx=5, pady=5, sticky='w', columnspan = 5)
        self.hex_display = Text(self.text_frame, width=53, height=16)
        self.hex_display.grid()
        self.text_area_setup()
    ##########################
    ###END WIDGET FUNCTIONS###
    ##########################