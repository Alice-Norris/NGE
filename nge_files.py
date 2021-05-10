import os
from nge_librarian import Librarian
import mmap
import re
the_librarian = Librarian()
the_librarian.add_book('Test')
the_librarian.request_book('Test')
the_librarian.add_sheet('Test_1')
the_librarian.add_sheet('Test_2')
the_librarian.add_sheet('Test_3')
the_librarian.add_book('Fire')
the_librarian.request_book('Fire')
the_librarian.add_sheet('Fire_1')
the_librarian.add_sheet('Fire_2')
the_librarian.add_sheet('Fire_3')
the_librarian.add_book('Tester')
the_librarian.request_book('Tester')
the_librarian.add_sheet('Tester_1')
the_librarian.add_sheet('Tester_2')
the_librarian.add_sheet('Tester_3')
the_librarian.add_sheet('TestSheet')
index = the_librarian.request_index()
def write_file_data(directory, file, index, shelf_name):
    shelf_name = the_librarian.request_shelf()
    if (os.path.exists(directory)):
        file_to_write = open(directory + file, 'wb')
        file_to_write.write(bytes('\x1C' + shelf_name, encoding = 'utf-8'))
        for book in index.items():
            the_librarian.request_book(book[0])
            file_to_write.write(bytes('\x1D' + book[0], encoding = 'utf-8'))
            for sheet_dict in book[1]:
                for sheet in sheet_dict.items():
                    file_to_write.write(bytes('\x1E' + sheet[0], encoding = 'utf-8'))
                    current_sheet = the_librarian.request_sheet(sheet[0])
                    for character in current_sheet.char_list:
                        file_to_write.write(bytes('\x1F', encoding = 'utf-8'))
                        file_to_write.write(bytes([character.obj_num]))
                        file_to_write.write(bytes(character.name + '\x10', encoding = 'utf-8'))
                        for pixel in character.data:
                            file_to_write.write(bytes([pixel]))
                        file_to_write.write(bytes('\x1F', encoding = 'utf-8'))
                    file_to_write.write(bytes('\x1E', encoding = 'utf-8'))
            file_to_write.write(bytes('\x1D', encoding = 'utf-8'))
        file_to_write.write(bytes('\x1C', encoding = 'utf-8'))
        file_to_write.close()

def read_file_data(directory, file):
    shelf_name = ''
    book_names = []
    if (os.path.exists(directory)): #if the file and directory exist:
        file_size = os.path.getsize(directory + file)
        with open(directory + file, 'r+b') as nge_file: #open file as nge_file
            shelf_name_start = 0
            shelf_name_end = 0
            curr_position = 0
            hex_data_end = 0
            read_data = nge_file.read(256)
            if (nge_file.endswith(bytes('\x1F\x1E\x1D\x1C', encoding = 'utf-8'))):
                shelf_name_start = read_data.find(bytes('\x1C', encoding = 'utf-8'))
                shelf_name_end = read_data.find(bytes('\x1D', encoding = 'utf-8'))
                print(shelf_name_start, shelf_name_end)
                shelf_name = read_data[shelf_name_start + 1:shelf_name_end].decode()
                curr_position = shelf_name_ends
                while len(read_data) == 256:
                    print(curr_position)

            else:
                print("malformed file!")
                

            



write_file_data('C:/Users/zakn/AimlessEntertainment/', 'test.nge', index, the_librarian.request_shelf())
read_file_data('C:/Users/zakn/AimlessEntertainment/', 'test.nge')