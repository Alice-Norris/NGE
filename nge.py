####                    NGE PROGRAM                     ####
# This file includes the methods that power the NGE,       #
# and also holds data structures                           #
############################################################

####                    NGE FUNCTIONS                   ####
# This section contains the functions that power the NGE   #
############################################################

def create_2d_array(width, height):
    width = width
    height = height
    posx = 0
    posy = 0
    array = []
    while (posx < width):
        array.append([])
        posx += 1
    posx = 0
    for column in array:
        while (posy < height):
            coordinate = str(posx) + ", " + str(posy)
            column.append(coordinate)
            posy += 1
        posx +=1
        posy = 0
    return array

############################################################
####              END NGE FUNCTION SECTION              ####
############################################################

####                     NGE CLASSES                    ####
# This section contains the classes for the NGE            #
############################################################

class Tool:
    def __init__(cls, name, bitmap):
        cls.tool_name = name
        cls.tool_bitmap = bitmap

#This class is used to store all temporary program data.
class Workspace:
    def __init__(cls, tool):
        cls.current_character = None
        cls.current_sheet = None
        cls.current_book = None
        cls.current_tool = tool
        cls.current_color = None

#this class is used to describe the character data for a single object
class Character: 
    def __init__(cls, object_num, sheet):
        cls.object_num = object_num #this should be a hex number
        cls.sheet = sheet # this is sheet number is for program purposes and does not (yet) relate to the output data
        cls.data = create_2d_array(8, 8) #8x8 list, used to store individual pixel information. Should be 0 to 3.

class Sheet:
    def __init__(cls, sheet_num):
        cls.sheet_num = sheet_num #This integer identifies the number of the sheet, which holds individual characters. Sheets are stored in Books
        cls.character_array = create_2d_array(16, 8) #16x8 list, used to store characters.

    def add_character(cls, character, x, y):
        cls.character_array[x][y] = character #adds given character at the x, y position provided

    def delete_character(cls, character, x, y): #sets given position in character list to 0, overwriting the character.
        cls.character_array[x][y] = 0

    def add_rectangle(cls, rectangle, x, y): #adds a rectangle canvas object to the two-dimensional list of rectangles.
        cls.rectangle_array[x][y] = rectangle

class Book:
    def __init___(cls, book_name):
        cls.book_name = book_name #This string is the name of the book. Books hold sheets.
        cls.sheet_array = [] #This list contains the Sheet objects that it is a part of.
############################################################
####               END NGE CLASSES SECTION              ####
############################################################
