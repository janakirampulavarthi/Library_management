import os
import sys
import time
import random

## Gobal variables accessed across module
global book_records
global user_records
global allocated_books

book_records = list()
user_records = list()
allocated_books = dict()


class Books:
    '''
    Template for books, stored in book_records
    '''
    
    def __init__(self, title, author, publication, \
                 description, copies):
        
        self.bid = random.randint(20001,30000)
        self.title = title
        self.author= author
        self.publication = publication
        self.description = description
        self.copies = copies
        self.availed = 0
        self.available_copies = self.copies - self.availed
        self.lended = False
        

class User_details:
    '''
    Template for user data, stored in user_records
    '''
    
    def __init__(self, uname, passwd, utype):
        self.uid = random.randint(10000,20000)
        self.uname = uname
        self.passwd = passwd
        self.utype = utype


def clear_screen():
    os.system("clear")


def exit_script():
    sys.exit()
    

def get_input(messg=None):
    '''
    input: message displayed to get input from user
    output: return if valid integer is passed by user
    return false on exception/invalid input
    '''
    
    messg = messg if messg else "Enter your choice : "
    val = input(messg)
        
    try:
        val = int(val)
        if val <= 0:
            return
        return val
    except ValueError:
        print("Invalid Input")
        time.sleep(1)
        if not messg:
            clear_screen()
        return False

def get_student_id():
    '''
    method to get student id and validate on suid existance
    with user_records
    '''
    
    suid = None
    while not suid:
        suid = get_input("Enter Student ID: ")

    for i in user_records:
        if i.uid == suid and i.utype == 'student':
            return suid
    print(
    ''' Student ID not matched

    chose 1 or 2

    1. Re-enter student id
    2. Back to menu\n''')
    choice = get_input()
    if choice and choice == 1:
        return get_student_id()
    elif choice and choice ==2:
        return
    else:
        print("Invalid input\n")
        return get_student_id()

def lended_books_by_uid(uid):
    '''
    input: user id of student
    output: print all books which are allocated to particular student
    '''
    
    print(f"\nBelow books are with student {uid}")
    for index, book in enumerate(book_records, start=1):
        if book.bid in allocated_books[uid]:
            print(f"{index}. {book.title}")
    
    
class Admin:
    def __init__(self):
        pass
    
    def add_book(self):
        '''
        get required details from admin and update in book_records
        '''
        
        def _add():
            book = Books(title, author, publication,
                         description, copies)
            book_records.append(book)
            
        clear_screen()
        title = input("\nEnter book title: ")
        author = input("Enter book author: ")
        publication = input("Enter book publication: ")
        description = input("Enter description: ")
        copies = None
        
        while not copies:
            copies = get_input("Enter number of copies: ")

        for book in book_records:
            if book.title == title:
                print(
                '''\nBook with Title exists in records

                Choose 1 or 2
                
                1. Overwrite existing
                2. return back to menu''')
                
                choice = get_input()
                if choice and choice == 1:
                    if book.lended:
                        print("Book allocated to student, Cannot be modified")
                        return
                    book.author = author
                    book.publication = publication
                    book.description = description
                    book.copies = copies
                    print("Modified existing data successfuly")
                elif choice and choice ==2:
                    print("Changes discarded")
                else:
                    print("\nInvalid input")
                return
        _add()
        print("Book added to records, returning back\n")
        time.sleep(1)

        
    def remove_book(self):
        '''
        get book title from admin to remove from book records
        '''

        def _delete(obj):
            for index, book in enumerate(book_records):
                if book.bid == obj.bid:
                    del book_records[index]
            print("Deleted book successfully")
            
        clear_screen()
        book_obj = self.get_book()
        if not book_obj:
            return

        if book_obj.lended:
            print(
                '''\nBook allocated to student, cannot be deleted

                choose 1 or 2

                1. Delete forcefull
                2. return back to menu''')
            choice = get_input()
            if choice and choice == 2:
                return
        _delete(book_obj)


    def lend_book(self):
        '''
        get input(book title and student id) from admin and update
        book records and allocated book 
        '''
        
        clear_screen()
        book_obj = self.get_book()
        if not book_obj:
            return
        
        suid = get_student_id()
        if not suid:
            return
        
        if book_obj.copies < 1 or book_obj.available_copies < 1:
            print("No copies are available")
        
        for book in book_records:
            if book.bid == book_obj.bid:
                book.lended = True
                book.available_copies = book.available_copies - 1
                book.availed = book.availed + 1
                if suid in allocated_books:
                    if book_obj.bid in allocated_books[suid]:
                        print(f"Book {book_obj.title} is already"
                              "allocated to student {suid}")
                    else:
                        allocated_books[suid].append(book_obj.bid)
                else:
                    allocated_books[suid] = []
                    allocated_books[suid].append(book_obj.bid)
                print(f"\nBook {book_obj.title} allocated to student {suid}")
                lended_books_by_uid(suid)
                time.sleep(1)
                break


    def return_book(self):
        '''
        get input(book title and student id) from admin and update
        data accoring to it, deallocate book from student
        '''
        
        clear_screen()
        book_obj = self.get_book()
        if not book_obj:
            return
        
        if not book_obj.lended:
            print(f"Book {book_obj.title} not allocated to any student")
            time.sleep(1)
            return
        
        suid = get_student_id()
        if not suid:
            return

        if allocated_books[suid]:
            if book_obj.bid in allocated_books[suid]:
                for book in book_records:
                    if book.bid == book_obj.bid:
                        book.available_copies = book.available_copies +1
                        book.availed = book.availed -1
                        if book.availed < 1:
                            book.lended = False
                        allocated_books[suid].remove(book_obj.bid)
                        print(f"Book {book_obj.title} deallocated from student {suid}")
                        break
            else:
                print(f"Book {book_obj.title} not allocated to student {suid}")
            lended_books_by_uid(suid)
            time.sleep(1)
        else:
            print(f"No Books are allocated to student {suid}")
                
                    
    def get_book(self):
        '''
        Based on user selection print list of books or
        print only titles matches with word input from user
        '''
        
        size = len(book_records)
        if size < 1:
            print("No Books found")
            time.sleep(2)
            return

        print(
        '''
        To select book choose 1 or 2 to proceed further
        
        1. List all books
        2. Search with letter start with\n''')
        choice = get_input()
        if choice:
            if choice == 1:
                return self.get_record(book_records)
            elif choice == 2:
                string = input("Enter match string: ")
                matches = [book for book in book_records \
                           if book.title.startswith(string)]
                if matches:
                    return self.get_record(matches)
                else:
                    print("No matches found, Listed all books")
                    return self.get_record(book_records)
            else:
                print("Invalid input")
        clear_screen()
        return self.get_book()
    
    def get_record(self, data):
        '''
        Input: List of book records
        Output: Based on user selection return object
        '''
        
        clear_screen()
        size = len(data)
        print(
        '''
        choose book number between 1-{}\n'''.format(len(data)))
        for i, book in enumerate(data, start=1):
            print(str(i),'. ', book.title)
            
        choice = None
        while not choice:
            choice = get_input("\nEnter book number: ")

        if choice > size or choice < 1:
            print("Invalid input")
            return self.get_record(data)
        
        return data[choice-1]


    def _print(self, records):
        # common print method which takes input list
        # and print on console
        
        for book in records:
            print(
            f'''{book.title.upper()}
            Author : {book.author}
            Publication. : {book.publication}
            Description: {book.description}
            Total copies : {book.copies}
            Avalailable copies: {book.available_copies}''')
        time.sleep(5)

            
    def list_all(self):
        # pint all available books in registered
        
        if not book_records:
            print("No records found, returning back")
        else:
            self._print(book_records)


    def available(self):
        # print only books which are not lended by any student
        
        data = [i for i in book_records if not i.lended]
        if not data:
            print("No books are available, returning back")
        else:
            self._print(data)

          
    def unavailable(self):
        # print only if no copies are available
        
        data = [i for i in book_records if i.lended and i.available_copies< 1]
        if not data:
            print("Books are not allocated to any student, returning back")
        else:
            self._print(data)

    def student_availed(self, uid):
        lended_books_by_uid(uid)     
        
            
            
class Login:
    def __init__(self, utype):
        self.utype = utype

    def login(self):
        '''
        if existing user checks for existance
        register new user accounts
        print student id required to get books
        '''
        
        clear_screen()
        print(
        '''Select any option to proceed further
        1. Login
        2. Register
        3. exit\n''')
        choice = get_input()
        if choice:
            if choice == 1:
                udata = None
                while not udata:
                    uname = input("\nEnter Username: ")
                    for user in user_records:
                        if user.uname == uname:
                            udata = user
                    if not udata:
                        clear_screen()
                        print("\nUser not found, retry again..!\n")
                while True:
                    passwd = input("Enter Password: " )
                    if passwd == udata.passwd:
                        print("\nLogin successfull")
                        time.sleep(1)
                        return udata.uid
                    print("\nIncorrect Password, reenter password again..!")
            elif choice == 2:
                while True:
                    udata = None
                    uname = input("Enter Username: ")
                    if uname:
                        for user in user_records:
                            if user.uname == uname:
                                udata = user
                    else:
                        print("Invalid username, retry again..!")    
                    if udata:
                        print("User with name already exists, use unique")
                    else:
                        break
                    
                while True:
                    passwd = input("Enter Password: ")
                    if passwd:
                        break
                udetails = User_details(uname, passwd, self.utype)
                user_records.append(udetails)
                print("User added successfully")
                if self.utype == 'student':
                    print(f"Student ID:{udetails.uid} required to lend books")
            elif choice ==3:
                exit_script()
        self.login()


class Main(Login, Admin):
    # main class where actual execution
    # of script starts
    def __init__(self):
        self.login_page()
        self.uid = None

    def menu(self, menu, option):
        '''
        Input: either Admin menu/Student menu and
        choice of user input.
        Output: return method based on user choice
        '''
        
        clear_screen()
        return {
            'admin_menu': {
                1: self.add_book,
                2: self.remove_book,
                3: self.lend_book,
                4: self.return_book,
                5: self.list_all,
                6: self.available,
                7: self.unavailable,
                8: exit_script,
                9: self.login_page,
            },
            'student_menu' : {
                1: self.list_all,
                2: self.available,
                3: self.student_availed,
                4: exit_script,
                5: self.login_page,
            },
        }.get(menu).get(option, False)
    
    
    def login_page(self):
        '''
        calls login method for student/admin execute method as per user
        choice. If failed to excute/invalid user input returns to menu
        '''
        
        clear_screen()
        print(
        '''\nPYTHON LIBRARY MANAGEMENT SYSTEM

        Choose 1 or 2
        1. Librarian
        2. Student
        3. Exit\n''')
        choice = get_input()
        if not choice:
            self.login_page()
            
        if choice == 1:
            super().__init__('admin')
            self.uid = self.login()
            self.admin_menu()
        elif choice ==2:
            super().__init__('student')
            self.uid = self.login()
            self.student_menu()
        elif choice == 3:
            exit_script()
        print("Invalid Input")
        time.sleep(1)
        self.login_page()
        
        
    def main_menu(self):
        '''
        Input from user and call admin/student login page
        '''
        
        clear_screen()
        print(
        '''PYTHON LIBRARY MANAGEMENT SYSTEM

        Choose between (1-3)
    
        1. Librarian
        2. Student
        3. Exit\n''')
        choice = get_input()
        if choice:
            func = self.menu('main_menu', choice)
            if func:
                func()
        self.main_menu()
        
            
    def admin_menu(self):
        '''
        Method is called when admin loged successfully
        calls methods from Admin class based on user choice.
        Return to same method if invalid input.
        '''
        
        clear_screen()
        print(
        '''
        Choose between (1-7)
        
        1. Add new book in library
        2. Remove book from library
        3. Lend book
        4. Return Lended book
        5. List all books
        6. List available books
        7. List lended books
        8. Exit
        9. Return to Main menu\n''')
        choice = get_input()
        if choice:
            func = self.menu('admin_menu', choice)
            if func:
                func()
            else:
                print("\nInvalid valid.")
        self.admin_menu()
        
                
    def student_menu(self):
        '''
        Method is called when Student loged successfully
        calls methods from Admin class based on user choice.
        Return to same method if invalid input.
        '''
        clear_screen()
        print(
        '''
        Choose between (1-7)
        1. List all books
        2. List available books
        3. List lended books
        4. Exit
        5. Return to Main menu\n''')
        choice = get_input()
        if choice:
            if choice == 3:
                lended_books_by_uid(self.uid)
            else:
                func = self.menu('student_menu', choice)
                if func:
                    func()
                else:
                    print("\nInvalid value.")
        self.student_menu()


if __name__ == '__main__':
    # uncomment below if default data is required
    # admin/admin is created for librarian or admin user
    # student/student is created for accessing student user
    
    for count in range(1,5):
        book = Books("Title" + str(count), "Author" + str(count), \
                     "Publication" + str(count), "Description" + str(count), count)
        book_records.append(book)

    ud = User_details ('admin','admin','admin')
    user_records.append(ud)
    ud = User_details ('student','student','student')
    user_records.append(ud)
    print(f"{user_records[1].uid} Default student ID required for "
          "allocating book using admin account")
    

    Main()
    

