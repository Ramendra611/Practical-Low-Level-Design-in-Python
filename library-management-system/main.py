from models import Book, BookCopy, Member
from library import Library
from notifications.console_notifier import ConsoleNotifier
from policies.student import StudentPolicy

library = Library()
library.add_listener(ConsoleNotifier())


design_patterns = Book(
    isbn="978-1-111-11111-1",
    title="Design Patterns",
    author="Gamma et al.",
    category="Technology",
)
dsa = Book(
    isbn="978-2-222-22222-2",
    title="DSA for beginners",
    author="Someone",
    category="Technology",
)
dsa.add_copy(BookCopy(dsa, "DSA-001"))
design_patterns.add_copy(BookCopy(design_patterns, "DP-001"))


library.add_book(design_patterns)
library.add_book(dsa)

ramesh = Member("member_01", "Ramesh", "ramesh@gmail.com", StudentPolicy())
mahesh = Member("member_02", "Mahesh", "mamesh@gmail.com", StudentPolicy())

library.add_member(ramesh)
library.add_member(mahesh)

loan_ramesh = library.borrow("member_01", design_patterns.isbn)
loan_mahesh = library.borrow("member_02", dsa.isbn)

## return book

library.return_book(loan_ramesh.id)


reservation = library.reserve("member_01", dsa.isbn)
print(reservation)