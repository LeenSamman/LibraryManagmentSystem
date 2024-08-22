# Library_Managment_System
A python based project that support OOP concepts . it is a real world example that handle
book managment , user managment , borrowing and returning , reservations , and log all transactions .
There is 2 kind of users in this system each have some privileges depending on their roles (regular user , admin).

# Project_Structure
- data.py -> The libraries and some users and books are added to the library (book_df) in this file.
- users.py -> The user specific operations and functionalities available to regular users and admin as admin is considered a user.
- Admin.py -> The Admin specific operations and functionalities.
- TestCases.ipynb -> As much as possible of test cases that the system function.
- FullCode.ipynb -> The full code in Jupyter notebook format to be github user-friendly.
- FunctionalRequirments.pdf -> Functional requirments for the project in details.


#Admin Functions
Admin is a user that can borrow a book with some more functions and privileges 
- add_book: a function for admin to add a book by passing the book title and author.
- delete_book_record : a function for admin to delete the book completely by passing the book title and author.
- decrement_copies : a function for admin to remove one copy from a specific book by passing the book title and author.
- display_all_books : a function to display all books in the library. All books can be displayed by printing the books_df.
- display_all_users : a function to display all users in the library. All users can be displayed by printing the users_df.
- display_all_borrowed_books :  a function to display borrowed books. All borrowed books can be displayed by printing the borrowed_books_df.
- display_all_transactions :  a function to display transactions (borrowing and returning). All transactions can be displayed by printing transaction_log_df.

  *Note : for better practice books_df, users_df , reservations_df , borrowed_books_df , transaction_log_df , havetoreturn_df
  All these dataframes should be private only to admins but they are not in this project.


#User Functions
- _update_global_overdue_books :  a afunction that is automatically called during functions like borrow_book, return_book to update overdue books and apply fines.
- borrow_book : a function for user to borrow a book by passing book title and author name and how many days he/she want to borrow the book.
- return_book : a function for user to borrow a book by passing book title and author name .
- display_my_overdue_books : a function that enable the user to display books he/she is late to return .
- view_borrowed_books : a function that enable the user to display books he/she borrowing now .
- reserve_book : a function to enable user to reserve a book if not available yet by passing the book title and author.
- cancel_reservation : a function to enable user to cancel reservation if no longer wanting the book by passing the book title and author.
- display_user_details : a function to display user details .




Acknowledgements
This project was developed as part of a Python course. Special thanks to Eng. Omar Alhory for supervision and guidance.

