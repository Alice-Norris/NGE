from nge_classes import Shelf, Book, Sheet, Character
####                    THE LIBRARIAN                    ####
# The Librarian is the class that manages all other objects #
# Only one should be created, and only one should be used   #
# Hands data to the user interface upon request.            #
#############################################################

class Librarian:
    __instance = None
    
    self.curr_shelf = None
    self.current_book = None
    self.current_sheet = None
    self.current_char = None

    def __init__(self):
        if Librarian.__instance != None:
            raise Exception("Only one librarian allowed. You've done something wrong.")
        else:
            Librarian.__instance = self

    def
    #takes sheet name as an argument, checks to make sure the sheet name does not alread
    #exist, and then creates and appends it to the book.
    def add_sheet(sheet_name): 
        sheet_list = self.current_book.sheet_dict
        for sheet in sheet_list.keys():
            if sheet_name == sheet:
                print("This page already exists!")
                break
            else: 
                sheet_list[sheet_name] = new Sheet()

    def delete_sheet(sheet_name): #takes a sheet name as an argument
        #deletes the sheet object and its sheetname from the dictionary
        self.current_book.sheet_dict.pop(sheet_name)
            