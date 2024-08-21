# Library_Managment_System
A python based project that support OOP concepts . it is a real world example that is used for
book managment , user managment , borrowing and returning , reservations , and loo all transactions
There is 2 kind of users each have some privileges depending on their roles (regular user , admin) 

Admin Functions
Admin is a user that can borrow a book with some more functions and privileges 
- 
-
-
-


User Functions
- _update_global_overdue_books :  an automatically called function that update the overdue books log
- borrow_book : a function for user to borrow a book by passing book title and auther name and how many days he/she want to borrow the book
- return_book : a function for user to borrow a book by passing book title and auther name
- display_my_overdue_books : a function that enable the user to display books he/she is late to return
- view_borrowed_books : a function that enable the user to display books he/she borrowing now
- reserve_book : a function to enable user to reserve a book if not available yet
- cancel_reservation : a function to enable user to cancel reservation if no longer waanting the book
- display_user_details : a function to display user details



Functional requirments for the system
- System Can add user
- admin can add a book
- admin can delete a book
- admin can display all user information
- admin can display all borrowed books and by who
- admin can display all reservations for books
- user can borrow a book :
                            - we need to search for the book
                            - the book may not be exist
                            - the book may be exist but all the copies of the book are borrowed by someone
                            - if the book is borrowed by someone the user may want to reserve the book
                            - if the book is available the user should specify a day to return the book
                            - the book should be returned on time
                            - the user may be late to return the book so for every day late a 1 $ fine will 
                                  be set to the user to pay.

Acknowledgements
This project was developed as part of a Python course. Special thanks to Eng. Omar Alhory for supervision and guidance.

