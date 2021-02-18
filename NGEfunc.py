####        NGE FUCNCTIONS        ####
# This file includes the functions   #
# that power the NGE, and also holds #
# important data structures          #
######################################


def create2dArray(width, height, array):
    width = width
    height = height
    posx = 0
    posy = 0
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

            
    
    
#this class is used to describe the character data for a single object
class character:
    def __init__(self, objectNum, sheet):
        self.objectNum = objectNum #this should be a hex number
        self.sheet = sheet # this is sheet number is for program purposes and does not (yet) relate to the output data
        self.data = []
        self.createPixelArray() 

class sheet:
    def __init__(self, sheetNum):
        self.sheetNum = sheetNum
        self.tiles =    []

    def addCharacter(self, character):
        self.tiles.append(character)
test = []
create2dArray(10, 2, test)
for row in test:
    print(row)

print(test[4][1])