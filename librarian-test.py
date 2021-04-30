from nge_librarian import Librarian
the_librarian = Librarian("Sample Shelf")
the_librarian.add_sheet("default_2")
the_librarian.add_sheet("default_3")
the_librarian.add_sheet("default_4")
the_librarian.add_book("test")
the_librarian.request_book("test")
the_librarian.add_sheet("test_1")
the_librarian.add_sheet("test_2")
the_librarian.add_sheet("test_3")
the_librarian.add_sheet("test_4")
the_librarian.add_book("impossible")
the_librarian.request_book("impossible")
the_librarian.add_sheet("impossible_1")
the_librarian.add_sheet("impossible_2")
the_librarian.add_sheet("impossible_3")
the_librarian.add_sheet("impossible_4")
index = the_librarian.request_index()

#unpack book dictionary, book[0] is book name, book[1] is list of sheet dictionaries
# for book in index.items():
#     book_name =  book[0]
#     print(book_name)
#     for sheets in book[1]:
#         for sheet_dict in sheets.items(): 
#             sheet_name = sheet_dict[0]
#             print("\t",  sheet_name)
#             char_dicts = sheet_dict[1]
#             for char_dict in char_dicts:
#                 print("\t\tCharacters:", len(char_dict))

book_list = []
for books in index.items():
    print(books[0])
    for sheets in next(iter(books[1])).items():
        print(sheets[0])
        for chars in next(iter(sheets[1])).items():
            print(chars)
                

for char in print(next(iter(next(iter(next(iter(next(iter(index[next(iter(index))])).values())))).values())))
print(next(iter(next(iter(next(iter(index[next(iter(index))])).values())).values())