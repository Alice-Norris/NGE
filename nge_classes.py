from nge_const import NGE_BLACK, NGE_DK_GRAY, NGE_LT_GRAY, NGE_WHITE
####                     NGE CLASSES                    ####
# This section contains the classes for the NGE            #
############################################################
#this class creates tools with specified name and bitmap
class Tool:
    def __init__(cls, name, bitmap):
        cls.tool_name = name
        cls.tool_bitmap = bitmap

#this class is used to describe the character data for a single object
class Character: 
    def __init__(cls, obj_num, sheet, name = "none"):
        cls.obj_num = obj_num #this should be a hex number
        cls.sheet = sheet #stores the sheet object this character is a member of
        cls.data = [] #64 member list, used to store individual pixel information. Should be 0 to 3.
        cls.name = name
        while (len(cls.data) < 64):
            cls.data.append(3)

#this class holds "sheets" of characters. 
class Sheet:
    def __init__(cls):
        cls.char_list = [] #list used to store characters.
        cls.book = book #This variable stores the book object an instance of Sheet is a member of.
        char_num = 0
        while(len(cls.char_list) <= 127):
            char = Character(char_num, cls.sheet_num)
            cls.char_list.append(char)
            char_num += 1

class Book:
    def __init__(cls, book_name):
        cls.book_name = book_name #This string is the name of the book. Books hold sheets.
        cls.sheet_dict = {} #This Dictionary follows the format of sheet_name : sheet_object

class Shelf:
    def __init__(cls, shelf_name):
        cls.shelf_name = shelf_name
        cls.num_books = 0
        cls.sheet_list = []