
from data import *
# A class to create entities involved in the library managment system (regular users + Admins)
class users:
    def __init__(self,first_name,last_name,age,gender,role="Regular"): #first name,last name ,age ,gender and role are needed to create the user
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.role = role
        self.borrowed_books = pd.DataFrame(columns=["Book Title", "Author","Borrow Date", "Return Date"])  # when create the user he/she have no borrowed books yet
        self.havetoreturn = pd.DataFrame(columns=["Book Title", "Original Due Date", "Days Overdue"]) #This DataFrame will store books that the user is late to return, including the necessary details like the book title, the original due date, and the number of days overdue.
        self.reserved_books = pd.DataFrame(columns=["Book Title", "Reservation Date"])  # if the book not available the user can reserve it .......
        self.fines = 0  # Start with zero fines because when creating a user . user did not borrow any book yet
       
        # As soon a user is created will be add  to the users_df
        # Add user to users_df
        new_user = pd.DataFrame({
            "First Name": [self.first_name],
            "Last Name": [self.last_name],
            "Age": [self.age],
            "Gender": [self.gender],
            "Role": [self.role],
            "Borrowed Books": [self.borrowed_books],
            "Fines": [self.fines]
        })
        global users_df
        users_df = pd.concat([users_df, new_user], ignore_index=True)
        
       

        


#----------------------------------------------------------------------------------------------------------------------------------------------------



    # Method to check and update overdue books (automatically called)
    # function automatically tracks books that have passed their return dates and marks them as overdue.
    # _update_global_overdue_books is automatically called during functions like borrow_book, return_book, user_login, daily checks, or system startup to update overdue books and apply fines.
    
    def _update_global_overdue_books(self):
        global havetoreturn_df
        current_date = datetime.now()
        print(f"Current Date: {current_date}")
    
        # Ensure dates are in datetime format
        self.borrowed_books["Return Date"] = pd.to_datetime(self.borrowed_books["Return Date"])
    
        # overdue_books are the books that are overdue from the user borrowed books
        overdue_books = self.borrowed_books[self.borrowed_books["Return Date"] < current_date]  # the user specify the borrowed_books["Return Date"] when borrowing a book
        
        print(f"Identified Overdue Books:\n{overdue_books}")
    
        # A loop for fine calculation
        # access the "Return Date" for the current book in each row. The "Return Date" was set when the book was borrowed.
        # then we calculate the time difference between the current date (current_date) and the "Return Date" for the book.
        # .days is an attribute of a timedelta object returns the difference in days between the two dates to calculate overdue days.
        for _, row in overdue_books.iterrows():  # no index "_" to ignore it
            days_overdue = (current_date - row["Return Date"]).days
    
            # Check if the book is already in the global overdue DataFrame to avoid duplication
            # if not exist
            if not ((havetoreturn_df["User"] == f"{self.first_name} {self.last_name}") & 
                    (havetoreturn_df["Book Title"] == row["Book Title"]) & 
                    (havetoreturn_df["Author"] == row["Author"])).any():
                # then add the book to overdue_entry dataframe then it will be added to the global havetoreturn_df  
                overdue_entry = pd.DataFrame([{
                    "User": f"{self.first_name} {self.last_name}",
                    "Book Title": row["Book Title"],
                    "Author": row["Author"],
                    "Original Due Date": row["Return Date"].strftime("%Y-%m-%d"),
                    "Days Overdue": days_overdue,
                    "Fines": days_overdue  # Fine calculated based on days overdue
                }])
    
                # The global havetoreturn_df DataFrame is updated to include all overdue books across all users
                # we already calculate the fines for overdue books based on the number of days past the return date. 
                # This fine is added to the user's total fines.
                havetoreturn_df = pd.concat([havetoreturn_df, overdue_entry], ignore_index=True)
                self.fines += days_overdue
                print(f"Added '{row['Book Title']}' to overdue with {days_overdue} days overdue.")
            else:
                print(f"{row['Book Title']} is already recorded as overdue.")




#----------------------------------------------------------------------------------------------------------------------------------------------------
    


    # user want to borrow a book .he/she should pass the book name and auther and how many days he/she want to borrow the book
    # user cannot borrow the book for more than 30 days
    # ex. leen.borrow_book("Python Programming", "John Doe", 15) 
    def borrow_book(self, book_title, book_author, borrow_duration=30):
        borrow_date = datetime.now()
        # Ensure the borrow duration does not exceed 30 days. if it does then set to 30
        borrow_duration = min(borrow_duration, 30)
        # the book need to be available so the user can borrow it
        # first check if the book  available by the book title and its auther.
        # we will  filter the rows of books_df where the Title and Author match the 
        # book_title and book_author provided by the user .book_entry is a dataframe that contain matched books
        # only one book should be matched 
        book_entry = books_df[(books_df["Title"] == book_title) & (books_df["Author"] == book_author)]

        # if match then book_entry is not empty .the book is in the library and we need to check if their exist a copy from the book
        if not book_entry.empty:
            book_index = book_entry.index[0]     # the dataframe book entry should have one record but if their is duplicates for some reason maybe spelling. the first record will be retrieved
            if books_df.at[book_index, "CopiesAvailable"] > 0:                # if there is a copy available
                books_df.at[book_index, "CopiesAvailable"] -= 1               #then Decrement the available copies by one
                                                                            # at faster than iloc when accessin a single scaler value
                
                return_date = borrow_date + timedelta(days=borrow_duration)    # Calculate the return date

                
                # Adding the borrowed book details to the user's DataFrame
                self.borrowed_books.loc[len(self.borrowed_books)] = [
                    book_title,
                    book_author,
                    borrow_date.strftime("%Y-%m-%d"),
                    return_date.strftime("%Y-%m-%d")
                ]
                # the is book available . the user is going to borrow the book then -> 
                # 1) Add the borrowed book details to the borrowed_books_df
                borrowed_books_df.loc[len(borrowed_books_df)] = [
                    f"{self.first_name} {self.last_name}",
                    book_title,
                    book_author,
                    borrow_date.strftime("%Y-%m-%d"),
                    return_date.strftime("%Y-%m-%d")
                ]

                
                # 2) Log the borrowing transaction
                transaction_log_df.loc[len(transaction_log_df)] = [
                    "Borrow",
                    f"{self.first_name} {self.last_name}",
                    book_title,
                    book_author,
                    borrow_date.strftime("%Y-%m-%d")
                ]


                
                print(f"{book_title} by {book_author} has been borrowed until {return_date.strftime('%Y-%m-%d')}.")

                # Check if the user is late returning the book
                current_date = datetime.now()
                if current_date > return_date:
                    late_days = (current_date - return_date).days  # Calculate how many days the user is late
                    fine = late_days                            # One dollar fine per late day *1
                    print(f"You are {late_days} days late to return the book. A fine of ${fine} has been applied.")
                    
            
            else:
                print(f"No copies of '{book_title}' by {book_author} are currently available.") # there is a match but no available copies
        else:
            print(f"'{book_title}' by {book_author} is not in the library.")   # if there is no match. book entry is empty

        # Update global overdue books after borrowing
        self._update_global_overdue_books()


#----------------------------------------------------------------------------------------------------------------------------------------------------

    def return_book(self, book_title, book_author):
        # search for the book in the borrowed books df to update it
        # when find it assign the book to borrowed_entry
        borrowed_entry = borrowed_books_df[
            (borrowed_books_df["User"] == f"{self.first_name} {self.last_name}") & 
            (borrowed_books_df["Title"] == book_title) & 
            (borrowed_books_df["Author"] == book_author)
        ]
        
        # when we find the book then the borrowed_entry is not empty ->
        # 1) drop the record that tell that the user borrowed the book 
        if not borrowed_entry.empty:
            borrowed_books_df.drop(borrowed_entry.index, inplace=True)
            self.borrowed_books = self.borrowed_books[
                ~((self.borrowed_books["Book Title"] == book_title) & 
                  (self.borrowed_books["Author"] == book_author))
            ]
            
            # 2) update the books_df . the book is return then there is another available copy
            book_entry = books_df[(books_df["Title"] == book_title) & (books_df["Author"] == book_author)]
            if not book_entry.empty:
                book_index = book_entry.index[0]
                books_df.at[book_index, "CopiesAvailable"] += 1
                print(f"{book_title} by {book_author} has been returned.")
    
                # 3) Log the returning transaction
                transaction_log_df.loc[len(transaction_log_df)] = [
                    "Return",
                    f"{self.first_name} {self.last_name}",
                    book_title,
                    book_author,
                    datetime.now().strftime("%Y-%m-%d")
                ]
            else:
                print(f"Error: The book '{book_title}' by {book_author} was not found in the library records.")
            
            # 4) check if anyone reserved the book to notify the first on the queue if they are not notified
            reservations_for_book = reservations_df[
                (reservations_df["Title"] == book_title) & 
                (reservations_df["Author"] == book_author) & 
                (reservations_df["Notification Sent"] == False)
            ]
            if not reservations_for_book.empty:
                first_in_queue = reservations_for_book.loc[reservations_for_book["Queue Position"].idxmin()]
                print(f"Notification: '{book_title}' by {book_author} is now available for {first_in_queue['Reserved By']}.")
                reservations_df.at[first_in_queue.name, "Notification Sent"] = True
                
                # Simulate the borrower borrowing the book
                borrower_name = first_in_queue['Reserved By']
                borrower_first_name, borrower_last_name = borrower_name.split()
                
                # Find the user in the users_df
                borrower = users_df[
                    (users_df["First Name"] == borrower_first_name) & 
                    (users_df["Last Name"] == borrower_last_name)
                ]
                
                if not borrower.empty:
                    # Simulate the borrower borrowing the book
                    borrower_user = users(borrower_first_name, borrower_last_name, borrower['Age'].iloc[0], borrower['Gender'].iloc[0])
                    borrower_user.borrow_book(book_title, book_author)
                    
        else:
            print(f"No record of borrowing '{book_title}' by {book_author} found.")
        
        # Update global overdue books after returning
        self._update_global_overdue_books()
    


    
    
#----------------------------------------------------------------------------------------------------------------------------------------------------    
    
    
    #  function for user to display his/her overdue books
    def display_my_overdue_books(self):
        my_overdue_books = havetoreturn_df[havetoreturn_df["User"] == f"{self.first_name} {self.last_name}"]
        if not my_overdue_books.empty:
            print("Your Overdue Books:")
            print(my_overdue_books)
        else:
            print("You have no overdue books.")

    

 #----------------------------------------------------------------------------------------------------------------------------------------------------  



    #user should be able to see all the books he/she currently borrowing
    def view_borrowed_books(self):
        """Display all currently borrowed books by the user."""
        user_borrowed_books = borrowed_books_df[borrowed_books_df["User"] == f"{self.first_name} {self.last_name}"]
        if user_borrowed_books.empty:
            print("No books currently borrowed.")
        else:
            print("Currently Borrowed Books:")
            print(user_borrowed_books)
    
#----------------------------------------------------------------------------------------------------------------------------------------------------  


    # user may want to reserve a book if all copies are currently borrowed
    # the reservation date will be the current date 
    def reserve_book(self, book_title, book_author):
        # check if there is no copy available . we need to find the book in book_df
        book_entry = books_df[(books_df["Title"] == book_title) & (books_df["Author"] == book_author)]
    
        # if we find the book and the copies are 0 the user will wait on a queue
        # the reservation date will be the current date 
        if not book_entry.empty:
            book_index = book_entry.index[0]
            if books_df.at[book_index, "CopiesAvailable"] == 0:
                # Automatically set the reservation date to the current date
                reservation_date = datetime.now().strftime("%Y-%m-%d")
                
                # Add the reservation to the user reserved_books df
                new_reservation = pd.DataFrame([{
                    "Book Title": book_title,
                    "Reservation Date": reservation_date
                }])
                self.reserved_books = pd.concat([self.reserved_books, new_reservation], ignore_index=True)
                
                # Add the reservation to the global reservations DataFrame
                reservations_df.loc[len(reservations_df)] = [
                    book_title, 
                    book_author, 
                    f"{self.first_name} {self.last_name}", 
                    reservation_date, 
                    None,  # Queue position will be determined after sorting
                    False  # Notification Sent flag
                ]
                
                # call a function to Sort the reservations by Reservation Date and update the queue positions
                self.update_queue_positions(book_title, book_author)
                
                print(f"'{book_title}' by {book_author} has been reserved.")
            else:
                print(f"'{book_title}' by {book_author} is currently available, no need to reserve.")
        else:
            print(f"'{book_title}' by {book_author} does not exist in the library.")


    # a function to Sort the reservations by Reservation Date and update the queue positions
    def update_queue_positions(self, book_title, book_author):
        book_reservations = reservations_df[(reservations_df["Title"] == book_title) & 
                                            (reservations_df["Author"] == book_author)]
        
        # Sort by reservation date and reset queue positions
        sorted_reservations = book_reservations.sort_values(by="Reservation Date").reset_index(drop=True)
        
        # Update the queue positions in the reservations DataFrame
        for position, (index, reservation) in enumerate(sorted_reservations.iterrows(), start=1):
            reservations_df.at[index, "Queue Position"] = position
        
        print(f"Queue positions updated for '{book_title}' by {book_author}.")

#-----------------------------------------------------------------------------------------------------------------------------------


    # Method to display all reserved books for the user
    def display_reserved_books(self):
        """Display all books the user has reserved."""
        if self.reserved_books.empty:
            print("No books currently reserved.")
        else:
            print("Reserved Books:")
            print(self.reserved_books.to_string(index=False))

#----------------------------------------------------------------------------------------------------------------------------------------------------
# a user may want to cancel reservations . if so and he is notified that the book is available 
# the nontification will be sent to the next person on the queue 
    def cancel_reservation(self, book_title, book_author):
        # Find the user's reservation in the global reservations DataFrame
        reserved_book = reservations_df[(reservations_df["Title"] == book_title) & 
                                        (reservations_df["Author"] == book_author) & 
                                        (reservations_df["Reserved By"] == f"{self.first_name} {self.last_name}")]
        # if we find the reservation then we need to 1) Remove the user from the queue
        if not reserved_book.empty: 
            reservations_df.drop(reserved_book.index, inplace=True)
            
            # 2) Remove the reservation from the user's reserved_books DataFrame
            self.reserved_books = self.reserved_books[self.reserved_books["Book Title"] != book_title]
            
            # 3) Update the queue positions for other users
            queue_position = reserved_book.iloc[0]["Queue Position"]
            reservations_df.loc[(reservations_df["Title"] == book_title) & 
                                (reservations_df["Author"] == book_author) & 
                                (reservations_df["Queue Position"] > queue_position), 
                                "Queue Position"] -= 1
            
            print(f"Reservation for '{book_title}' by {book_author} has been canceled.")
            
            # 4) Check if the book is currently available
            book_entry = books_df[(books_df["Title"] == book_title) & (books_df["Author"] == book_author)]
            if not book_entry.empty and books_df.at[book_entry.index[0], "CopiesAvailable"] > 0:
                # If the book is available, notify the first user in the queue
                next_reservation = reservations_df[(reservations_df["Title"] == book_title) & 
                                                   (reservations_df["Author"] == book_author)].sort_values("Queue Position").head(1)
                if not next_reservation.empty:
                    next_user = next_reservation.iloc[0]["Reserved By"]
                    print(f"Notification: '{book_title}' by {book_author} is now available for {next_user}.")
                    reservations_df.at[next_reservation.index[0], "Notification Sent"] = True
            else:
                print(f"'{book_title}' by {book_author} is still borrowed by another user, but your cancellation was successful.")
        else:
            print(f"No reservation found for '{book_title}' by {book_author}.")


#----------------------------------------------------------------------------------------------------------------------------------------------------

# Function to display the user's details, including basic information, borrowed books, reserved books, and overdue books.

    def display_user_details(self):
        """Display the details of the user."""
        print(f"User Details for {self.first_name} {self.last_name}:")
        print(f"Age: {self.age}")
        print(f"Gender: {self.gender}")
        print(f"Role: {self.role}")
        print(f"Fines: ${self.fines}")
    
        print("\nBorrowed Books:")
        if self.borrowed_books.empty:
            print("No books currently borrowed.")
        else:
            print(self.borrowed_books.to_string(index=False))
    
        print("\nReserved Books:")
        if self.reserved_books.empty:
            print("No books currently reserved.")
        else:
            print(self.reserved_books.to_string(index=False))
    
        print("\nOverdue Books:")
        if self.havetoreturn.empty:
            print("No overdue books.")
        else:
            print(self.havetoreturn.to_string(index=False))
    


