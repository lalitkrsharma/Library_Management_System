import mysql.connector as mys
mycon = mys.connect(host='localhost',user='root',password='sharma@1999',database='Library_Management_System')
mycur = mycon.cursor()


def search_book():
  a = input('Enter Book ID or Book Name : \n'
  "#      '*' to see all books      # \n"
  "# '$' to see all available books # \n"
  "#  '$$' to see all issued books  # \n")
  while True:
    if a.upper() == 'EXIT':
      break
    elif a == '*':
      query = "select * from books"
    elif a == '$':
      query = "select * from books where issued_to IS NULL"
    elif a == '$$':
      query = "select * from books where issued_to IS NOT NULL"
    elif a.isnumeric():
      query = "select * from books where id = {}".format(int(a))
    else :
      query = "select * from books where name = '{}'".format(a)
    mycur.execute(query)
    dt = mycur.fetchall()
    if dt != []:
      print('-'*80)
      print('%5s'%'ID', '%30s'%'Name', '%20s'%"Author's Name", '%20s'%'Issued To' )
      print('-'*80)
      for R in dt:
        print('%5s'%R[0], '%30s'%R[1], '%20s'%R[2], '%20s'%R[3])
      break
    else:
      print('No such book found.\n')
      print('.'*85)
      a = input('Enter a valid Book ID or Book Name : ')

def search_user():
  a = input('Enter User ID or User Name : '
  "#             '*' to see all users              # \n"
  "# '$' to see all users who haven't issued books # \n"
  "#  '$$' to see all users who have issued books  # \n")
  while True:
    if a.upper() == 'EXIT':
      break
    elif a == '*':
      query = "select * from users"
    elif a == '$':
      query = "select * from users where books_assigned IS NULL"
    elif a == '$$':
      query = "select * from books where books_assigned IS NOT NULL"
    elif a.isnumeric():
      query = "select * from users where id = {}".format(int(a))
    else :
      query = "select * from users where name = {}".format(a)
    mycur.execute(query)
    dt = mycur.fetchall()
    if dt != []:
      print('-'*80)
      print('%5s'%'ID', '%30s'%'Name', '%20s'%"Phone Number", '%20s'%'Books Borrowed' )
      print('-'*80)
      for R in dt:
        print('%5s'%R[0], '%30s'%R[1], '%20s'%R[2], '%20s'%R[3])
      break
    else:
      print('No such User found. \n')
      print('.'*85)
      a = input('Enter a Valid User ID or User Name : ')

def issue_book():
  a = input('Enter Book ID : ')
  b = input('Enter User ID : ')
  while True:
    if a.upper() == 'EXIT':
      break
    if b.upper() == 'EXIT':
      break
    query = "select id from books where issued_to IS NULL"
    mycur.execute(query)
    dt = mycur.fetchall()
    query = "select id from users"
    ut = mycur.fetchall()
    if (int(a),) in dt:
      query = "update books set issued_to = {} where id = {}".format(int(b),int(a))
      mycur.execute(query)
      query = "update users set books_assigned = {} where id = {}".format(int(a),int(b))
      mycur.execute(query)
      mycon.commit()
      query = "select books.name, users.name from books, users where books.issued_to = users.id"
      mycur.execute(query)
      dt = mycur.fetchone()
      print(dt[0],'is Issued to',dt[1])
      break
    elif (int(b),) not in ut:
      print('User Not Found.')
      print('.'*85)
      b = input('Enter a Valid User ID : ')
    else:
      print('Sorry, but the Book is unavailable.')
      break

def return_book():
  a = input('Enter Book ID : ')
  while True:
    if a.upper() == 'EXIT':
      break
    query = "select id from books where issued_to IS NOT NULL"
    mycur.execute(query)
    dt = mycur.fetchall()
    if (int(a),) in dt:
      query = "update books set issued_to = NULL where id = {}".format(int(a))
      mycur.execute(query)
      query = "update users set books_assigned = NULL where books_assigned = {}".format(int(a))
      mycur.execute(query)
      mycon.commit()
      print('The Book is Returned.')
      break
    else:
      print('The Book was Not Issued.')
      print('.'*85)
      a = input('Enter Book ID of an Issued Book : ')
 
def add_books():
  query = "select Max(id) from books"
  mycur.execute(query)
  dt = mycur.fetchone()
  while True:
    nm = input('Enter Book Name : ').upper()
    if nm.upper() == 'EXIT':
      break
    an = input('Enter Author Name : ').capitalize()
    if an.upper() == 'EXIT':
      break
    query = "insert into books (name,author_name) values('{}','{}')".format(nm,an)
    mycur.execute(query)
    mycon.commit()
  query = "select * from books where id > {}".format(dt[0])
  mycur.execute(query)
  dt = mycur.fetchall()
  print('Following Books have been added')
  print('-'*80)
  print('%5s'%'ID', '%30s'%'Name', '%20s'%"Author's Name", '%20s'%'Issued To' )
  print('-'*80)
  for R in dt:
    print('%5s'%R[0], '%30s'%R[1], '%20s'%R[2], '%20s'%R[3])
def del_books():
  while True:
    a = input('Enter ID of the Book to be Deleted : ')
    if a.upper() == 'EXIT':
      break
    else:
      query = "delete from books where id = {}".format(int(a))
      mycur.execute(query)
      mycon.commit()
      print('Book of the Given ID has been removed from Inventory.')
def mod_books():
  while True:
    a = int(input('Enter Book ID : '))
    if a.upper() == 'EXIT':
      break
    else:
      b = int(input('What would you like to change? \n'
      '   [1] Book Name \n'
      '   [2] Author Name \n'))
      while True:
        if b == 1:
          nm = input('Enter New Name : ')
          query = "update books set name = '{}' where id = {}".format(nm,a)
          break
        elif b == 2:
          an = input('Enter New Author Name : ')
          query = "update books set author_name = '{}' where id = {}".format(an,a)
          break
        else :
          b = int(input('Please Enter a Valid Choice : '))
      mycur.execute(query)
      mycon.commit()
      query = "select * from books where id = {}".format(a)
      mycur.execute(query)
      dt = mycur.fetchone()
      print('Changes have been made')
      print('-'*80)
      print('%5s'%'ID', '%30s'%'Name', '%20s'%"Author's Name", '%20s'%'Issued To' )
      print('-'*80)
      print('%5s'%dt[0], '%30s'%dt[1], '%20s'%dt[2], '%20s'%dt[3])

def update_books():
  print(
  '  [1] Add Books \n'
  '  [2] Delete Books \n'
  '  [3] Modify Details of Books')
  x = input('Enter Desired Number Option : ')

  while True:
    if x.upper() = 'EXIT':
      break
    elif int(x) == 1:
      print('.'*85)
      add_books()
      print('.'*85)
      break
    elif int(x) == 2:
      print('.'*85)
      del_books()
      print('.'*85)
      break
    elif int(x) == 3:
      print('.'*85)
      mod_books()
      print('.'*85)
      break
    else:
      x = input('Please Enter a Valid Choice : ')

def add_users():
  query = "select Max(id) from users where id is not null"
  mycur.execute(query)
  dt = mycur.fetchone()
  while True:
    nm = input('Enter User Name : ').capitalize()
    if nm.upper() == 'EXIT':
      break
      x = 'EXIT'
    pn = input('Enter Phone Number : ')
    if pn.upper() == 'EXIT':
      break
      x = 'EXIT'
    query = "insert into users (name,phone_no) values('{}','{}')".format(nm,pn)
    mycur.execute(query)
    mycon.commit()
  query = "select * from users where id > {}".format(dt[0])
  mycur.execute(query)
  dt = mycur.fetchall()
  print('Following Users have been added')
  print('-'*80)
  print('%5s'%'ID', '%30s'%'Name', '%20s'%"Phone Number", '%20s'%'Books Borrowed' )
  print('-'*80)
  for R in dt:
     print('%5s'%R[0], '%30s'%R[1], '%20s'%R[2], '%20s'%R[3])

def del_users():
  while True:
    a = input('Enter ID of the User to be Deleted : ')
    if a.upper() == 'EXIT':
      break
    else :
      a = int(a)
    query = "select id from users"
    mycur.execute(query)
    dt = mycur.fetchall()
    if (a,) in dt :
      query = "delete from users where id = {}".format(a)
      mycur.execute(query)
      mycon.commit()
      print('User of the Given ID has been removed from the User List. \n')
    else:
      print('There is no such User.')
    print('.'*85)

def mod_users():
  while True:
    a = input('Enter User ID : ')
    if a.upper() == 'EXIT':
      break
    else:
      a = int(a)
    b = input('What would you like to change? \n'
    '   [1] Name \n'
    '   [2] Phone Number \n')
    if b.upper() == 'EXIT':
      break
    else:
      b = int(b)
      
    if b == 1:
      nm = input('Enter New Name : ')
      query = "update users set name = '{}' where id = {}".format(nm,a)
      break
    elif b == 2:
      an = input('Enter New Phone Number : ')
      query = "update users set phone_no = '{}' where id = {}".format(an,a)
      break
    else :
      b = input('Please Enter a Valid Choice : ')
      
    mycur.execute(query)
    mycon.commit()
    query = "select * from users where id = {}".format(a)
    mycur.execute(query)
    dt = mycur.fetchone()
    print('-'*80)
    print('%5s'%'ID', '%30s'%'Name', '%20s'%"Phone Number", '%20s'%'Books Borrowed' )
    print('-'*80)
    print('%5s'%dt[0], '%30s'%dt[1], '%20s'%dt[2], '%20s'%dt[3])

def update_user():
  print(
  '  [1] Add User \n'
  '  [2] Delete User \n'
  '  [3] Modify Details of User')
  x = input('Enter Desired Number Option : ')
  while True:
    if x.upper() == 'EXIT':
      break
    elif int(x) == 1:
      print('.'*85)
      add_users()
      print('.'*85)
      break
    elif int(x) == 2:
      print('.'*85)
      del_users()
      print('.'*85)
      break
    elif int(x) == 3:
      print('.'*85)
      mod_users()
      print('.'*85)
      break
    else:
      print('.'*85)
      x = input('Enter a Valid Choice : ')


while True:
  print(
  'Hey, What would you like to do?\n'
  ' [1] Search book from record\n'
  ' [2] Search user from record\n' 
  ' [3] Issue a Book\n'
  ' [4] Return a Book\n'
  ' [5] Update Inventory\n'
  ' [6] Update User Records\n'
  )
  n = int(input('Enter Desired Number Option: '))

  while True:
    if n == 1:
      print('='*100)
      print(' '*40, 'BOOK SEARCH MENU \n')
      search_book()
      print('='*100)
      break
    elif n == 2:
      print('='*100)
      print(' '*40, 'USER SEARCH MENU \n')
      search_user()
      print('='*100)
      break
    elif n == 3:
      print('='*100)
      print(' '*40, 'ISSUE BOOK MENU \n')
      issue_book()
      print('='*100)
      break
    elif n == 4:
      print('='*100)
      print(' '*40, 'RETURN BOOK MENU \n')
      return_book()
      print('='*100)
      break
    elif n == 5:
      print('='*100)
      print(' '*40, 'UPDATE INVENTORY MENU \n')
      update_books()
      print('='*100)
      break
    elif n == 6:
      print('='*100)
      print(' '*40, 'UPDATE USER LIST MENU \n')
      update_user()
      print('='*100)
      break
    else:
      n = int(input('Please Enter a Valid Choice: '))