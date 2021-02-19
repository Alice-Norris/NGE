####                    NGE PROGRAM                     ####
# This file includes the methods that power the NGE,       #
# and also holds data structures                           #
############################################################

####                    NGE VARIABLES                   ####
# This section contains the functions that power the NGE   #
############################################################
workingSheet = 0 #This holds the current sheet object displayed in the GUI
workingCharacter = 0 #This holds the current character displayed in the GUI
currentTool = 'none' #This holds the active tool (pencil, eraser, fill, or none)
############################################################
####              END NGE VARIABLE SECTION              ####
############################################################

####                    NGE FUNCTIONS                   ####
# This section contains the functions that power the NGE   #
############################################################

def create2dArray(width, height):
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

#this class is used to describe the character data for a single object
class character:
    def __init__(self, objectNum, sheet):
        self.objectNum = objectNum #this should be a hex number
        self.sheet = sheet # this is sheet number is for program purposes and does not (yet) relate to the output data
        self.data = create2dArray(8, 8)

class sheet:
    def __init__(self, sheetNum):
        self.sheetNum = sheetNum #This integer identifies the number of the sheet, for storage in Books
        self.characterArray = create2dArray(16, 8) #16x8 list, used to store characters.

    def addCharacter(self, character, x, y):
        self.characterArray[x][y] = character #adds given character at the x, y position provided

    def deleteCharacter(self, character, x, y): #sets given position in character list to 0, overwriting the character.
        self.characterArray[x][y] = 0

    def addRectangle(self, rectangle, x, y): #adds a rectangle canvas object to the two-dimensional list of rectangles.
        self.rectangleArray[x][y] = rectangle

############################################################
####               END NGE CLASSES SECTION              ####
############################################################


character1 = character(0, 1)

sheet1 = sheet(0)

sheet1.addCharacter(character1, 0, 0)

print(sheet1.characterArray[0][0].data[7][7])