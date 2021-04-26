from nge_classes import Book, Sheet
book = Book("Testing")
sheet1 = Sheet(0, "background", book)
sheet2 = Sheet(1, "foreground", book)
sheet3 = Sheet(2, "HUD", book)
sheet4 = Sheet(3, "projectiles", book)

book.add_sheet(sheet2)
book.add_sheet(sheet4)
book.add_sheet(sheet3)
book.add_sheet(sheet1)


for sheet in book.sheet_list:
    print(sheet.sheet_num, sheet.sheet_name)
book.delete_sheet(sheet3)

for sheet in book.sheet_list:
    print(sheet.sheet_num, sheet.sheet_name)

    
