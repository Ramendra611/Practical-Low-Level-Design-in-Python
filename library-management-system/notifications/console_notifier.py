from notifications.listener import LibraryEventListener
from notifications.events import (
    LibraryEvent,
    LoanIssuedEvent,
    LoanReturnedEvent,
    ReservationFulfilledEvent,
    LoanOverdueEvent,
)

## sample of a listener


class ConsoleNotifier(LibraryEventListener):

    def on_event(self, event: LibraryEvent):
        if isinstance(event, LoanIssuedEvent):
            loan = event.loan
            print(
                f"  [notify] Issued {loan.book_item.book.title!r} "
                f"(copy {loan.book_item.copy_id}) to {loan.member.name}. "
                f"Due {loan.due_date.date().isoformat()}."
            )

        elif isinstance(event, LoanReturnedEvent):
            loan = event.loan
            fine_text = (
                f"Fine: Rs. {event.fine_amount:.2f}"
                if event.fine_amount > 0
                else "No fine."
            )
            print(
                f"  [notify] Returned {loan.book_item.book.title!r} "
                f"by {loan.member.name}. {fine_text}"
            )

        elif isinstance(event, ReservationFulfilledEvent):
            print(
                f"  [notify] Reservation ready: {event.member.name!r} — "
                f"{event.book.title!r} is now available. "
                f"(Email would go to {event.member.email}.)"
            )

        elif isinstance(event, LoanOverdueEvent):
            print(
                f"  [notify] Your loan is overdue: {event.loan.member.name!r} — "
                f"(Warning Phone call  would go to {event.loan.member.email}.)"
            )
