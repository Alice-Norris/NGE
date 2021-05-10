from nge_const import NGE_BLACK, NGE_DK_GRAY, NGE_LT_GRAY, NGE_WHITE
####                     NGE CLASSES                    ####
# This section contains the classes for the NGE            #
############################################################
#this class creates tools with specified name and bitmap
class Tool:
    def __init__(cls, name, cursor):
        cls.tool_name = name
        cls.tool_cursor = cursor

#this class is used to describe the character data for a single object
class Character: 
    def __init__(cls, obj_num, name = "unnamed"):
        cls.obj_num = obj_num #this should be a hex number
        cls.data = [] #64 member list, used to store individual pixel information. Should be 0 to 3.
        cls.name = name + "_" + str(obj_num)
        while (len(cls.data) < 64):
            cls.data.append(3)

#this class holds "sheets" of characters. 
class Sheet:
    def __init__(cls, sheet_name):
        cls.sheet_name = sheet_name
        cls.char_list = [] #list used to store characters.
        char_num = 0
        while(len(cls.char_list) <= 127):
            char = Character(char_num, sheet_name)
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
        cls.book_dict = {}