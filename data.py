import pandas as pd # To manage books dataframe 
from datetime import datetime, timedelta # for date calculations

# book dataframe contain all books in the library
# user dataframe  contains all users logs
# reservation dataframe  contain users who want to borrow a book not available now 
# borrowed books dataframe contain books that are borrowed by some user



books_df = pd.DataFrame(columns=[ "Title", "Author", "CopiesAvailable"])
users_df = pd.DataFrame(columns=["First Name", "Last Name","Age" , "Role", "Borrowed Books", "Fines"])
reservations_df = pd.DataFrame(columns=[ "Title", "Author", "Reserved By", "Reservation Date", "Queue Position", "Notification Sent"])
borrowed_books_df = pd.DataFrame(columns=["User", "Title", "Author", "Borrow Date", "Due Date"])
transaction_log_df = pd.DataFrame(columns=["Transaction Type", "User", "Title", "Author", "Transaction Date"])
havetoreturn_df = pd.DataFrame(columns=["User", "Book Title", "Author", "Original Due Date", "Days Overdue", "Fines"])


# Fill the library with some books and users



# Function to add books because the lib is empty
def add_book(title, author, copies):
    global books_df
    # Check if the book already exists (based on title and author)
    # if the book exist add it to a dataframe name existing_book .it will have one record if the book exist
    existing_book = books_df[(books_df['Title'] == title) & (books_df['Author'] == author)]

    # if existing_book not empty that means that the book exist then we will update the available copies instead of adding new record
    if not existing_book.empty:
        # If the book already exists, update the CopiesAvailable
        existing_index = existing_book.index[0]
        books_df.loc[existing_index, 'CopiesAvailable'] += copies # increment the number of copies of the book in the book_df
    else:
        # if the book not exist, add a new record with the generated BookID
        new_book_id = len(books_df) + 1
        books_df.loc[new_book_id] = {"Title": title, "Author": author, "CopiesAvailable": copies}

# Adding 10 programming books . A list of books to pass into our function
programming_books = [
    ("Python Programming", "John Doe", 5),
    ("Data Science with Python", "Jane Smith", 3),
    ("Machine Learning Basics", "Michael Brown", 4),
    ("Deep Learning with TensorFlow", "Anna White", 2),
    ("Artificial Intelligence: A Modern Approach", "Peter Green", 6),
    ("Introduction to Algorithms", "Thomas H. Cormen", 7),
    ("Clean Code", "Robert C. Martin", 5),
    ("Design Patterns", "Erich Gamma", 4),
    ("JavaScript: The Good Parts", "Douglas Crockford", 3),
    ("The Pragmatic Programmer", "Andrew Hunt", 8)
]


# loop into the list to call the function for every book to be added
for book in programming_books:
    add_book(*book)




# Function to add users
def add_user(first_name, last_name, age, gender, role="Regular", borrowed_books=None, fines=0):
    global users_df
    borrowed_books = borrowed_books if borrowed_books is not None else pd.DataFrame(columns=["Book Title", "First Date to Borrow", "Last Date to Return"])
    
    # Check if the user already exists based on First Name, Last Name, and Age
    existing_user = users_df[(users_df['First Name'] == first_name) & 
                             (users_df['Last Name'] == last_name) & 
                             (users_df['Age'] == age)]
    
    if not existing_user.empty:
        print(f"User {first_name} {last_name} already exists.")
        return

    # Add the new user to the DataFrame
    new_user = pd.DataFrame({
        "First Name": [first_name],
        "Last Name": [last_name],
        "Age": [age],
        "Gender": [gender],
        "Role": [role],
        "Borrowed Books":  str(borrowed_books), 
        "Fines": [fines]
    })
    users_df = pd.concat([users_df, new_user], ignore_index=True)

# Adding 10 users
users_list = [
    ("Leen", "Samman", 20, "Female"),
    ("Amal", "Taha", 34, "Female"),
    ("Amany", "Awwad", 22, "Female"),
    ("Ahmad", "Bilal", 55, "Male"),
    ("Karam", "Jallad", 19, "Male"),
    ("Qamar", "Sayeed", 33, "Female"),
    ("Hayat", "Najjar", 19, "Female"),
    ("Tamara", "Mousa", 36, "Female"),
    ("Omar", "Bilal", 28, "Male"),
    ("Amjad", "Rami", 41, "Male")
]

# Add users to the DataFrame
for user in users_list:
    add_user(user[0], user[1], user[2], user[3])
