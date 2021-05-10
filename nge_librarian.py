from nge_classes import Shelf, Book, Sheet, Character
####                    THE LIBRARIAN                    ####
# The Librarian is the class that manages all other objects #
# Only one should be created, and only one should be used   #
# Hands data to the user interface upon request.            #
#############################################################

class Librarian:
    __instance = None
    
    def __init__(self):
        if Librarian.__instance != None:
            raise Exception("Only one librarian allowed. You've done something wrong.")
        else:
            Librarian.__instance = self
            self.__shelf = Shelf('unnamed')
            self.__current_book = None
            self.__current_sheet = None
            self.__current_char = None
            


    #takes sheet name as an argument, checks to make sure the sheet name does not alread
    #exist, and then creates and appends it to the book.
    def add_sheet(self, sheet_name): 
        sheet_list = self.__current_book.sheet_dict
        print(sheet_list)
        for sheet in sheet_list.keys():
            if sheet_name == sheet:
                print("This page already exists!")
                sheet_name += '1'
        sheet_list[sheet_name] = Sheet(sheet_name)
        #print(sheet_name, "added")
        return sheet_list[sheet_name]

    def remove_sheet(self, sheet_name): #takes a sheet name as an argument
        #deletes the sheet object and its sheetname from the dictionary
        result = self.__current_book.sheet_dict.pop(sheet_name, False)
        if(not result):
            print("That sheet doesn't exist!")
        else:
            print(sheet_name, "deleted!")

    def add_book(self, book_name):
        book_list = self.__shelf.book_dict
        for book in book_list.keys():
            if book_name == book:
                print("This book already exists!")
                book_name += str(len(book_list.keys()))
        book_list[book_name] = Book(book_name)
        return book_list[book_name]

    def remove_book(self, book_name):
        result = self.__shelf.book_dict.pop(book_name, False)
        if (not result):
            print("That book doesn't exist!")
        else:
            print(book_name, "deleted!") 

    def request_current_book(self):
        return self.__current_book

    def request_book(self, book_name):
        current_book_list = self.__shelf.book_dict
        if (book_name not in current_book_list):
            print(book_name, "doesn't exist!")
        else:
            self.__current_book = current_book_list[book_name]
            return self.__current_book

    def request_current_sheet(self):
        return self.__current_sheet

    def request_sheet(self, sheet_name):
        current_sheet_list = self.__current_book.sheet_dict
        if (sheet_name not in current_sheet_list):
            print(sheet_name, "doesn't exist!")
        else:
            self.__current_sheet = current_sheet_list[sheet_name]
            return self.__current_sheet

    def request_shelf(self):
        return self.__shelf.shelf_name

    def request_book_list(self):
        book_list = [*self.__shelf.book_dict.keys()].copy()
        return book_list

    def request_sheet_list(self):
        sheet_list = [*self.__current_book.sheet_dict.keys()]
        return sheet_list.copy()

    def request_char_list(self):
        return self.__current_sheet.char_list.copy()

    def request_index(self):
        #dictionary to hold data in the format [book name] = list of sheet names
        book_dict = {}
        #for book in shelf dictionary as a tuple (book name : Book object)
        if(not self.__shelf):
            return book_dict
        for book in self.__shelf.book_dict.items():
            #create a list for a key value of each book name
            book_dict[book[0]] = []
            #dictionary to hold sheet data in the format [sheet name] = list of character dictionaries
            sheet_dict = {}
            #for each sheet dictionary in the book object as a tuple (sheet name : Sheet object)
            for sheet in book[1].sheet_dict.items():
                #create a list for a key value of each sheet name
                sheet_dict[sheet[0]] = []
                #dictionary to hold character data in the format [obj_num] = name
                char_dict = {}
                #for each Character object in a Sheet object's char_list
                for char in sheet[1].char_list:
                    #add entry to dictionary in the format [object number] = name
                    char_dict[char.obj_num] = char.name
                #append Character dictionary to the sheet list with the sheet name as a key
                sheet_dict[sheet[0]].append(char_dict)
            #append each Sheet dictionary to the book's dictionary with the book's name as a key
            book_dict[book[0]].append(sheet_dict)
        #index is a dictionary of the format [book name] = sheet dictionaries,
        #each of which is in turn a dictionary of the format [sheet name] = character dictionary
        #there is one character dictionary for each sheet
        index = book_dict
        #return index
        return index