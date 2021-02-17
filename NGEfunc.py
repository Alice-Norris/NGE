####        NGE FUCNCTIONS        ####
# This file includes the functions   #
# that power the NGE, and also holds #
# important data structures          #
######################################

#this class is used to describe the character data for a single object
class character:
    def __init__(self, objectNum, sheet):
        self.objectNum = objectNum
        self.sheet = sheet
        self.data = [0] * 64

class sheet:
    def __init__(self, sheetNum):
        self.sheetNum = sheetNum
        self.tiles = []

    def addCharacter(self, character):
        self.tiles.append(character)

character1 = character(0, 1)
sheet1 = sheet(1)
sheet1.addCharacter(character1)

print(sheet1.tiles[0].data[62])