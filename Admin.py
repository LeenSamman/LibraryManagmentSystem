from data import *
from user import *
"""
All the critical aspects of the library management system are within the full visibility of the admin:
Books, Users, Reservations, Borrowed Books, and Transactions.This will ensure a comprehensive level of control 
and oversight, very essential for effective library managemen
"""

class Admin(users):
    def __init__(self, first_name, last_name, age, gender):
        # Call the __init__ method of the Users class
        super().__init__(first_name, last_name, age, gender, role="Admin")



    # An admin can add a book by passing the title of the book and the author and how many copies of the book he/she want to add

    # An admin can add a book by passing the title of the book and the author and how many copies of the book he/she want to add
    def add_book(self, title, author, copies):
        existing_book = books_df[(books_df["Title"] == title) & (books_df["Author"] == author)]
        
        if existing_book.empty:
            new_book = {"Title": title, "Author": author, "CopiesAvailable": copies}
            books_df.loc[len(books_df)] = new_book
            print(f"Book '{title}' by {author} has been added with {copies} copies.")
        else:
            book_index = existing_book.index[0]
            books_df.at[book_index, "CopiesAvailable"] += copies
            print(f"Copies of '{title}' by {author} have been increased by {copies}. Total copies available: {books_df.at[book_index, 'CopiesAvailable']}")

    
    # admin can delete the record for the book by passing the title and auther
    def delete_book_record(self, title, author):
        book_entry = books_df[(books_df["Title"] == title) & (books_df["Author"] == author)]
        
        if not book_entry.empty:
            books_df.drop(book_entry.index, inplace=True)
            print(f"All copies of '{title}' by {author} have been deleted from the library.")
        else:
            print(f"Book '{title}' by {author} does not exist in the library.") # book not exist to be deleted


    # One of the copies may be damaged so admin can delete one copy not all the book record
    def decrement_copies(self, title, author):
        book_entry = books_df[(books_df["Title"] == title) & (books_df["Author"] == author)]
        
        if not book_entry.empty:
            book_index = book_entry.index[0]
            available_copies = books_df.at[book_index, "CopiesAvailable"]
            
            if available_copies > 1:
                books_df.at[book_index, "CopiesAvailable"] -= 1
                print(f"One copy of '{title}' by {author} has been deleted. {available_copies - 1} copies remain.")
            else:
                # If there's only one copy left, notify admin to  delete the entire record
                print(f"Only one copy of '{title}' by {author} remains. Consider deleting the entire record instead.")
        else:
            print(f"Book '{title}' by {author} does not exist in the library.") # book  not exist to be deleted



    # admin can display all books 
    def display_all_books(self):
        if not books_df.empty:
            print("All Books in the Library:")
            print(books_df.to_string(index=False))
        else:
            print("No books available in the library.")


    #admin can display all users
    def display_all_users(self):
        """Display data for all users."""
        if not users_df.empty:
            print("All Users Data:")
            print(users_df.to_string(index=False))
        else:
            print("No users found.")




    # admin can display all current reservations
    def display_all_reservations(self):
        if not reservations_df.empty:
            print("All Reservations:")
            print(reservations_df.to_string(index=False))
        else:
            print("No reservations found.")




    # admin can display all borrowed books
    def display_all_borrowed_books(self):
        if not borrowed_books_df.empty:
            print("All Borrowed Books:")
            print(borrowed_books_df.to_string(index=False))
        else:
            print("No borrowed books found.")



    # admin can display all transactions done by users
    def display_all_transactions(self):
        if not transaction_log_df.empty:
            print("All Transactions:")
            print(transaction_log_df.to_string(index=False))
        else:
            print("No transactions found.")

