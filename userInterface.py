from nge_functions import character_to_hex, character_row_to_hex, update_character_data #import functions from nge
from nge_const import NGE_BLACK, NGE_DK_GRAY, NGE_LT_GRAY, NGE_WHITE, COLOR_DICT, REVERSE_COLOR_DICT
from tkinter import Menu, Canvas, Text, BitmapImage, Button, Scrollbar, StringVar
from tkinter.constants import *
from tkinter import ttk
from math import ceil, floor
from nge_classes import Tool

class nge_interface(ttk.Frame):
    #Constructor, calls functions to create GUI
    def __init__ (self, NGE, index, master=None):
        self.application = NGE
        self.index = index
        self.current_book = self.application.the_librarian.request_current_book()
        self.current_sheet = self.application.the_librarian.request_current_sheet()
        self.current_char = self.current_sheet.char_list[0]

        #style setup
        nge_style = ttk.Style()
        nge_style.theme_use('winnative')

        #setting top level window to a variable
        ttk.Frame.__init__(self, master, width=1024, height = 768, class_ = 'application_window')
        self.TLW = self.winfo_toplevel()
        self.grid()
        self.columnconfigure(0, minsize = 512)
        self.columnconfigure(1, minsize = 512)
        self.rowconfigure(0, minsize=384)
        self.rowconfigure(1, minsize=384)
        self.TLW.title("Nintendo Graphics Editor")
        #Creating menu along top of window
        self.create_menu(self.TLW)
        self.Select = Tool('select', BitmapImage('@empty.xbm', foreground = 'black', background = 'white'))
        self.Pencil = Tool('pencil', BitmapImage('@pencil.xbm', foreground = 'black', background = 'white'))
        self.Bucket = Tool('bucket', BitmapImage('@bucket.xbm', foreground = 'black', background = 'white'))
        self.Eraser = Tool('eraser', BitmapImage('@eraser.xbm', foreground = 'black', background = 'white'))
        
        #Creates different areas of the GUI
        self.active_book = StringVar()
        self.active_sheet = StringVar()
        self.entry_text = StringVar()
        self.organization_frames()
        self.sheet_area()    #populates sheet frame
        self.tile_area()     #populates tile frame
        self.tool_area()     #populates tool frame 
        self.color_area()    #populate color frame with available colors and current color tools
        self.tree_area()
        self.text_area()

        #create variables for UI
        self.current_tool = self.Select
        self.current_color = self.current_color_swatch.cget('bg')

        #create grids in sheet and character canvases
        self.create_canvas_rectangles(self.tile_display)
        self.create_canvas_rectangles(self.sheet_display)
        self.create_sheet_display_pixels()

    ###################
    ###GUI FUNCTIONS###
    ###################
    def highlight_text(self):
        self.hex_display.tag_delete('current_char')
        current_char_num = self.current_char.obj_num
        self.hex_display.tag_add('current_char', str(current_char_num + 2) + '.0', str(current_char_num + 2) + '.53')
        self.hex_display.tag_config('current_char', background = '#c0c0c0')

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
        for character in self.current_sheet.char_list:
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
        self.highlight_text()

    def create_sheet_display_pixels(self):
        characters = self.sheet_display.find_all()
        for character in self.current_sheet.char_list:
            coords = self.sheet_display.coords(character.obj_num+1)
            pixel_start_x = int(coords[0]+1)
            pixel_start_y = int(coords[1]+1)
            character = self.current_sheet.char_list[0]
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
                                                    width = 1, tags = (str(character.obj_num) + " pixels"))
                pixel_start_x += 4
                column += 1
                if(column == 8):
                    pixel_start_x = int(coords[0]+1)
                    column = 0
                    pixel_start_y += 4
                    row += 1

    def update_sheet_display_pixels(self, pixel = None, color = None):
        character = self.current_char
        sheet_tile = character.obj_num + 1
        sheet_tile_coords = self.sheet_display.coords(sheet_tile)
        sheet_tile_pixels = self.sheet_display.find_overlapping(sheet_tile_coords[0] + 1, sheet_tile_coords[1] + 1, sheet_tile_coords[2] - 1, sheet_tile_coords[3] - 1)
        self.sheet_display.itemconfigure(sheet_tile_pixels[pixel], fill = color, outline = color)

    def update_tile_display_pixels(self):
        self.entry_text.set(self.current_char)
        tile_display_pixels = self.tile_display.find_all()
        character_pixels = self.current_char.data
        index = 0
        while(index < len(character_pixels)):
            pixel_color = character_pixels[index]
            self.tile_display.itemconfig(index + 1, fill = REVERSE_COLOR_DICT[pixel_color])
            index += 1

    def update_text_area(self):
        character = self.current_char
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
        self.hex_display.tag_config('current_char', background = '#c0c0c0')

            
    def tree_view_setup(self):
        self.index = self.application.the_librarian.request_index()
        self.active_book.set('Active Book: \n' + self.current_book.book_name)
        self.active_sheet.set('Active Sheet: \n' + self.current_sheet.sheet_name)
        self.tree_view_update()

    def tree_view_update(self):
        self.index = self.application.the_librarian.request_index()
        shelf_name = self.application.the_librarian.request_shelf()
        if self.tree_view.exists('shelf'):
            self.tree_view.delete('shelf')
        self.tree_view.insert('', 0, iid = 'shelf', text = shelf_name)
        for book in self.index.items():
            book_id = book[0]
            page_count = len(book[1][0].keys())
            self.tree_view.insert('shelf', 'end', iid = 'book_'+book_id, values = (book_id, '', page_count))
            for sheets in next(iter(book[1])):
                self.tree_view.insert('book_'+book_id, 'end', iid = book_id+sheets, values=('', sheets, ''))       

    def actives_changed(self, book_name, sheet_name):
        self.current_book = self.application.the_librarian.request_book(book_name)
        self.current_sheet = self.application.the_librarian.request_sheet(sheet_name)
        self.current_char = self.current_sheet.char_list[0]
        self.update_tile_display_pixels()
        self.change_sheet()

    def change_sheet(self):
        i = 128
        sheet_pixels = self.sheet_display.find_all()
        for char in self.current_sheet.char_list:
            for pixel in char.data:
                sheet_char_coords = self.sheet_display.coords(char.obj_num + 1)
                color = REVERSE_COLOR_DICT[pixel]
                self.sheet_display.itemconfigure(sheet_pixels[i], fill = color, outline = color)
                i += 1

            
    #######################
    ###HANDLER FUNCTIONS###
    #######################
    def color_swatch_clicked(self, event):
        self.current_color_swatch.configure(bg = event.widget.cget('bg'))
        self.current_color = event.widget.cget('bg')

    def tool_button_clicked(self, event):
        clicked_tool = event.widget.winfo_name()
        if (clicked_tool == 'select'):
            self.current_tool = self.Select
        elif (clicked_tool == 'pencil'):
            self.current_tool = self.Pencil
        elif (clicked_tool == 'eraser'):
            self.current_tool = self.Eraser
        elif (clicked_tool == 'bucket'):
            self.current_tool = self.Bucket

    #makes an image of the current tool follow the mouse cursor
    def mouse_over_tile_display(self, event):
        cursor_image =self.current_tool.tool_bitmap
        tile_display_x= self.tile_display.canvasx(event.x)
        tile_display_y = self.tile_display.canvasx(event.y)
        if(not self.tile_display.find_withtag(65)):
            self.tile_display.create_bitmap(tile_display_x - 36, tile_display_y - 36, bitmap = self.current_tool.tool_bitmap)
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
        if self.current_tool == self.Pencil:
            color = self.current_color
            update_character_data(self.current_char, self.current_color, clicked_rectangle)
            self.tile_display.itemconfigure(clicked_rectangle, fill = self.current_color_swatch.cget('bg'))
            self.update_sheet_display_pixels(clicked_rectangle, color)
        if self.current_tool == self.Eraser:
            update_character_data(self.current_char, '#ffffff', clicked_rectangle)
            self.tile_display.itemconfigure(clicked_rectangle, fill = NGE_WHITE)
            self.update_sheet_display_pixels(clicked_rectangle, '#ffffff')
        character_to_hex(self.current_char)
        self.update_text_area()
        self.highlight_text()
    
    def sheet_display_clicked(self, event):
        click_x = self.sheet_display.canvasx(event.x)
        click_y = self.sheet_display.canvasy(event.y)
        clicked_character = self.sheet_display.find_overlapping(click_x, click_y, click_x + 1, click_y + 1)[0]
        self.current_char = self.current_sheet.char_list[clicked_character - 1]
        current_char_num = self.current_char.obj_num
        self.tile_display_label.config(text = "Object Number: " + str(current_char_num))
        self.hex_display.see(str(current_char_num + 2) + '.0')
        self.highlight_text()
        self.update_tile_display_pixels()
        tile_display_string = "Object " + str(self.current_char.obj_num) + ": "
        self.tile_display_label.config(text = tile_display_string)
        self.entry_text.set(self.current_char.name)

    def tile_name_enter(self, event):
        self.current_char.name = self.entry_text.get()

    def add_remove_items(self, event):
        widget_name = event.widget._name
        if widget_name == 'add_book':
            self.application.the_librarian.add_book(self.current_book.book_name)
        elif widget_name == 'add_sheet':
            self.application.the_librarian.add_sheet(self.current_sheet.sheet_name)
        elif widget_name == 'remove_book':
            self.application.the_librarian.remove_book(self.current_book.book_name)
        elif widget_name == 'remove_sheet':
            self.application.the_librarian.remove_sheet(self.current_sheet.sheet_name)
        self.tree_view_update()
        

    def make_active(self, event):
        item_type = self.tree_view.identify_column(event.x)
        item_iid = self.tree_view.identify_row(event.y)
        if item_type == '#1':
            parent_iid = self.tree_view.parent(item_iid)
            first_sheet = self.tree_view.get_children([item_iid])[0]
            book_name = self.tree_view.item(item_iid, option = 'values')[0]
            sheet_name = self.tree_view.item(first_sheet, option = 'values')[1]
            self.active_book.set('Active Book: \n' + book_name)
            self.active_sheet.set('Active Sheet: ' + sheet_name)
            self.actives_changed(book_name, sheet_name)

        elif item_type == '#2':
            parent_iid = self.tree_view.parent(item_iid)
            book_name = self.tree_view.item(parent_iid, option = 'values')[0]
            sheet_name = self.tree_view.item(item_iid, option = 'values')[1]
            self.active_book.set('Active Book: \n' + book_name)
            self.active_sheet.set('Active Sheet: \n' + sheet_name)
            self.actives_changed(book_name, sheet_name)
            
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

    def organization_frames(self):
        self.top_left_frame = ttk.Frame(self)
        self.top_left_frame.grid(row = 0, column = 0, sticky = N+S+E+W)
        self.bottom_left_frame = ttk.Frame(self)
        self.bottom_left_frame.grid(row = 1, column = 0, sticky = N+S+E+W)
        self.top_right_frame = ttk.Frame(self)
        self.top_right_frame.grid(row = 0, column = 1, sticky = N+S+E+W)
        self.bottom_right_frame = ttk.Frame(self)
        self.bottom_right_frame.grid(row=1, column = 1, sticky = N+S+E+W)

    def sheet_area(self):
        self.sheet_frame = ttk.LabelFrame(self.top_left_frame, labelanchor = 's', borderwidth = 2, text = "Sheet View")
        self.sheet_frame.grid(row = 0, column = 0, in_ = self.top_left_frame, padx =5, pady = 5, ipadx = 5, ipady = 5)
        self.sheet_frame.grid_columnconfigure(0, weight = 1)
        self.sheet_frame.grid_columnconfigure(2, weight = 1)
        
        self.sheet_display = Canvas(self.sheet_frame, 
                                    height=266, 
                                    width=530, 
                                    bg='#FFFFFF', 
                                    border=0, 
                                    borderwidth = 0, 
                                    highlightthickness=0, 
                                    cursor='tcross')
        self.sheet_display.grid(in_ = self.sheet_frame, row = 0, column = 1)

        self.sheet_label = ttk.Label(self.sheet_frame, text= "Sheet: " + self.current_sheet.sheet_name)
        self.sheet_display.bind('<ButtonRelease-1>', self.sheet_display_clicked)
        self.sheet_label.grid(in_ = self.sheet_frame, row = 1, column = 1)

    def tile_area(self):
        self.tile_frame = ttk.LabelFrame(self.top_right_frame, labelanchor = 's', borderwidth = 2, text = 'Character View')
        self.tile_frame.grid(row = 0, column = 1, in_ = self.top_right_frame)

        self.tile_display = Canvas(self.tile_frame, height = 266, width = 266, bg = '#FFFFFF', borderwidth = 0, highlightthickness=0)
        self.tile_display.bind('<Motion>', self.mouse_over_tile_display)
        self.tile_display.bind('<Leave>', self.mouse_left_tile_display)
        self.tile_display.bind('<ButtonRelease-1>', self.tile_display_clicked)
        self.tile_display.grid(row = 1, columnspan = 2, in_=self.tile_frame)

        tile_display_string = "Object " + str(self.current_char.obj_num) + ": "
        self.tile_display_label = ttk.Label(self.tile_frame, text = tile_display_string)
        self.tile_display_label.grid(row = 2, column = 0, sticky = E, in_ = self.tile_frame)

        self.entry_text.set(self.current_char.name)
        self.tile_name_box = ttk.Entry(self.tile_frame, textvariable = self.entry_text)
        self.tile_name_box.bind('<Return>', self.tile_name_enter)
        self.tile_name_box.grid(row = 2, column = 1, sticky = W, in_ = self.tile_frame)

    def tool_area(self):
        self.tool_frame = ttk.LabelFrame(self.top_right_frame, labelanchor = 's', borderwidth = 2, text = 'Tools')
        self.tool_frame.grid(row = 0, column = 3, in_ = self.top_right_frame, sticky = N+S)

        self.select_button = Button(self.tool_frame, name = self.Select.tool_name, bitmap = '@select.xbm', width = 64, height = 64)
        self.select_button.bind('<ButtonRelease-1>', self.tool_button_clicked)
        self.select_button.grid(in_ = self.tool_frame)

        self.pencil_button = Button(self.tool_frame, name = self.Pencil.tool_name, bitmap = self.Pencil.tool_bitmap, width = 64, height = 64)
        self.pencil_button.bind('<ButtonRelease-1>', self.tool_button_clicked)
        self.pencil_button.grid(in_ = self.tool_frame)
        
        self.eraser_button = Button(self.tool_frame, name = self.Eraser.tool_name, bitmap = self.Eraser.tool_bitmap, width = 64, height = 64)
        self.eraser_button.bind('<ButtonRelease-1>', self.tool_button_clicked)
        self.eraser_button.grid(in_ = self.tool_frame)
        
        self.bucket_button = Button(self.tool_frame, name = self.Bucket.tool_name, bitmap = self.Bucket.tool_bitmap, width = 64, height = 64)
        self.bucket_button.bind('<ButtonRelease-1>', self.tool_button_clicked)
        self.bucket_button.grid(in_ = self.tool_frame)

    def color_area(self):
        self.color_frame = ttk.LabelFrame(self.top_right_frame, labelanchor = 's', borderwidth = 2, text = 'Colors')
        self.color_frame.grid(row = 0, column = 2, in_ = self.top_right_frame, sticky = N+S)

        self.palette_frame = ttk.LabelFrame(self.color_frame, labelanchor = 's', borderwidth = 0, text= 'Palette')
        self.palette_frame.grid(in_ = self.color_frame)
        self.palette_frame.columnconfigure(0, weight = 1)
        self.palette_frame.columnconfigure(2, weight = 1)

        self.current_color_frame = ttk.LabelFrame(self.color_frame, labelanchor='s', borderwidth = 0, text='Current')
        self.current_color_frame.grid(in_ = self.color_frame)
        self.current_color_frame.columnconfigure(0, weight = 1)
        self.current_color_frame.columnconfigure(2, weight = 1)

        self.black_swatch = Canvas(self.palette_frame, height = 32, width = 32, borderwidth = 3, relief = 'sunken', bg = NGE_BLACK)
        self.black_swatch.bind('<ButtonRelease-1>', self.color_swatch_clicked)
        self.black_swatch.grid(pady=5, in_ = self.palette_frame, row = 0, column = 1)

        self.dk_gray_swatch = Canvas(self.palette_frame, height = 32, width = 32, borderwidth = 3, relief = 'sunken', bg = NGE_DK_GRAY)
        self.dk_gray_swatch.bind('<ButtonRelease-1>', self.color_swatch_clicked)
        self.dk_gray_swatch.grid(pady=5, in_ = self.palette_frame, row = 1, column = 1)
        
        self.lt_gray_swatch = Canvas(self.palette_frame, height = 32, width = 32, borderwidth = 3, relief = 'sunken', bg = NGE_LT_GRAY)
        self.lt_gray_swatch.bind('<ButtonRelease-1>', self.color_swatch_clicked)        
        self.lt_gray_swatch.grid(pady=5, in_ = self.palette_frame, row = 2, column = 1)

        self.white_swatch = Canvas(self.palette_frame, height = 32, width = 32, borderwidth = 3, relief = 'sunken', bg = NGE_WHITE)
        self.white_swatch.bind('<ButtonRelease-1>', self.color_swatch_clicked)        
        self.white_swatch.grid(in_ = self.palette_frame, row = 3, column = 1)

        self.current_color_swatch = Canvas(self.current_color_frame, height = 32, width = 32, borderwidth = 3, relief = 'sunken', bg = NGE_WHITE)
        self.current_color_swatch.grid(in_ = self.current_color_frame, row = 1, column = 1)
        

    def text_area(self):

        self.text_frame = ttk.LabelFrame(self.bottom_right_frame, labelanchor='s', borderwidth = 2, text = 'Hex Data')
        self.text_frame.grid(row = 1, column = 1, in_ = self.bottom_right_frame, columnspan = 3)
        self.hex_display = Text(self.text_frame, width=53, height=16)
        self.hex_display.grid(row = 0, column = 0, in_ = self.text_frame)
        self.hex_display_scrollbar = Scrollbar(self.text_frame, orient = VERTICAL, command=self.hex_display.yview)
        self.hex_display_scrollbar.grid(row = 0, column = 1, sticky=N+S, in_ = self.text_frame)
        self.hex_display['yscrollcommand'] = self.hex_display_scrollbar.set
        self.text_area_setup()

    def tree_area(self):
        self.tree_area_frame = ttk.LabelFrame(self.bottom_left_frame, labelanchor='s', borderwidth = 2, text = 'Information')
        self.tree_area_frame.grid(row = 1, column = 0, in_ = self.bottom_left_frame)
        self.tree_view_frame = ttk.Frame(self.tree_area_frame)
        self.tree_view_frame.grid(row = 0, column = 0, in_ = self.tree_area_frame)
        self.info_frame = ttk.LabelFrame(self.tree_area_frame, labelanchor = 's', text = 'Active Items')
        self.info_frame.grid(row = 0, column = 2, in_ = self.tree_area_frame, sticky = N+S)
        
        self.tree_view = ttk.Treeview(self.tree_area_frame, columns = ('Books', 'Sheets', 'Length'), displaycolumns='#all')
        self.tree_view.column('#0', width=150)
        self.tree_view.heading('#0', text = 'Shelf')
        self.tree_view.column('Books', width = 150)
        self.tree_view.heading('Books', text = 'Books')
        self.tree_view.column('Sheets', width= 150)
        self.tree_view.heading('Sheets', text='Sheets')
        self.tree_view.column('Length', width = 60)
        self.tree_view.heading('Length', text='Length')
        self.tree_view.grid(column=0, row =0, columnspan = 2, in_ = self.tree_area_frame)
        self.tree_view.bind('<Double-ButtonRelease-1>', self.make_active)

        self.book_controls = ttk.Frame(self.tree_area_frame)
        self.book_controls.grid(row = 1, column = 0, in_ = self.tree_area_frame)
        self.add_book_button = ttk.Button(self.book_controls, name = 'add_book', text = '+', width = 2)
        self.add_book_button.grid(row = 0, column = 0, in_ = self.book_controls)
        self.add_book_button.bind('<ButtonRelease-1>', self.add_remove_items)
        self.book_label = ttk.Label(self.book_controls, text = "Book")
        self.book_label.grid(row = 0, column = 1, in_ = self.book_controls)
        self.remove_book_button = ttk.Button(self.book_controls, name = 'remove_book', text = '-', width = 2)
        self.remove_book_button.grid(row = 0, column = 2, in_ = self.book_controls)
        self.remove_book_button.bind('<ButtonRelease-1>', self.add_remove_items)

        self.sheet_controls = ttk.Frame(self.tree_area_frame)
        self.sheet_controls.grid(row=1, column = 1, in_ = self.tree_area_frame)
        self.add_sheet_button = ttk.Button(self.sheet_controls, name = 'add_sheet', text = '+', width = 2)
        self.add_sheet_button.grid(row = 0, column = 0, in_ = self.sheet_controls)
        self.add_sheet_button.bind('<ButtonRelease-1>', self.add_remove_items)
        self.sheet_label = ttk.Label(self.sheet_controls, text = "Sheet")
        self.sheet_label.grid(row = 0, column = 1, in_ = self.sheet_controls)
        self.remove_sheet_button = ttk.Button(self.sheet_controls, name = 'remove_sheet', text = '-', width = 2)
        self.remove_sheet_button.grid(row = 0, column = 2, in_ = self.sheet_controls)
        self.remove_sheet_button.bind('<ButtonRelease-1>', self.add_remove_items)

        self.active_book_name = ttk.Label(self.info_frame, textvariable = self.active_book)
        self.active_book_name.grid(column = 0, row = 0, in_=self.info_frame)
        self.active_sheet_name = ttk.Label(self.info_frame, textvariable = self.active_sheet)
        self.active_sheet_name.grid(column = 0, row = 1, in_=self.info_frame)
        self.tree_view_setup()
    ##########################
    ###END WIDGET FUNCTIONS###
    ##########################