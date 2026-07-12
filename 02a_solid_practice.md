# SOLID Principles — Practice Workbook

> **Who this is for:** Anyone who has read `02_solid_principles.md` and now wants to *internalise* the five principles by doing — not just reading. This is a workout, not a textbook.

---

## Table of Contents

1. [Preface — How to Use This Workbook](#preface)
2. [Section 1 — Warm-Up: Name the Violation](#section-1--warm-up-name-the-violation)
   - [Snippet 1 — UserAccount](#snippet-1--useraccount-level-1)
   - [Snippet 2 — ShapeAreaCalculator](#snippet-2--shapeareacalculator-level-1)
   - [Snippet 3 — Ostrich and Bird](#snippet-3--ostrich-and-bird-level-1)
   - [Snippet 4 — Worker and RobotWorker](#snippet-4--worker-and-robotworker-level-1)
   - [Snippet 5 — OrderService](#snippet-5--orderservice-level-1)
3. [Section 2 — Single Responsibility Principle](#section-2--single-responsibility-principle)
   - [Problem 2.1 — BlogPost (Level 1)](#problem-21--blogpost-level-1)
   - [Problem 2.2 — EmployeeReport (Level 2)](#problem-22--employeereport-level-2)
   - [Problem 2.3 — Restaurant Order System (Level 3)](#problem-23--restaurant-order-system-level-3)
4. [Section 3 — Open/Closed Principle](#section-3--openclosed-principle)
   - [Problem 3.1 — PaymentProcessor (Level 1)](#problem-31--paymentprocessor-level-1)
   - [Problem 3.2 — LogFormatter (Level 2)](#problem-32--logformatter-level-2)
   - [Problem 3.3 — E-commerce Promotions (Level 3)](#problem-33--e-commerce-promotions-level-3)
5. [Section 4 — Liskov Substitution Principle](#section-4--liskov-substitution-principle)
   - [Problem 4.1 — Rectangle and Square (Level 1)](#problem-41--rectangle-and-square-level-1)
   - [Problem 4.2 — FileStorage and ReadOnlyStorage (Level 2)](#problem-42--filestorage-and-readonlystorage-level-2)
6. [Section 5 — Interface Segregation Principle](#section-5--interface-segregation-principle)
   - [Problem 5.1 — MultiFunctionPrinter (Level 1)](#problem-51--multifunctionprinter-level-1)
   - [Problem 5.2 — DataManager (Level 2)](#problem-52--datamanager-level-2)
7. [Section 6 — Dependency Inversion Principle](#section-6--dependency-inversion-principle)
   - [Problem 6.1 — NotificationService (Level 1)](#problem-61--notificationservice-level-1)
   - [Problem 6.2 — ReportService (Level 2)](#problem-62--reportservice-level-2)
   - [Problem 6.3 — Hospital Appointment System (Level 3)](#problem-63--hospital-appointment-system-level-3)
8. [Section 7 — Combined Violations](#section-7--combined-violations)
   - [Problem 7.1 — LibrarySystem (SRP + OCP + DIP)](#problem-71--librarysystem-srp--ocp--dip)
   - [Problem 7.2 — Animal Hierarchy (LSP + ISP + DIP)](#problem-72--animal-hierarchy-lsp--isp--dip)
9. [Section 8 — Capstone: Full Refactor Challenge](#section-8--capstone-full-refactor-challenge)
   - [Problem 8.1 — HospitalSystem](#problem-81--hospitalsystem-the-full-refactor)
10. [Summary Checklist](#summary-checklist)

---

## Preface

This file is **not a reading document**. It is a workout. The teaching has already happened in `02_solid_principles.md`. Here, you sweat.

**How to use this workbook:**

1. **Cover the solution.** Use your hand, a piece of paper, your scrollbar — anything. Read the problem first. Always.
2. **Attempt before reading.** Even thirty seconds of "what would *I* do?" is enough to make the solution stick five times harder than passive reading.
3. **The difficulty labels tell you what kind of effort is expected:**
   - **Level 1 (Warm-up)** — read a short snippet, name the violation in one sentence. No coding. These should take you 2–3 minutes each.
   - **Level 2 (Fix it)** — given broken code, refactor it correctly. Expect to spend 10–20 minutes.
   - **Level 3 (Design it)** — given a prose requirement, design the structure from scratch. No broken code is provided. 30–45 minutes.
4. **Don't skip Level 3 because Level 2 felt easy.** Fixing given code and designing from scratch are different skills. The interview tests the second one.
5. **Looking back at `02_solid_principles.md` during Level 3 is fine.** Looking back during Level 1 means you need more reps on the warm-ups.
6. **Do this workbook twice.** Once right after the teaching session. Once again a week later, no notes. The gap between the two attempts is your progress.

**The endgame:** By the time you finish this twice, you should be able to glance at any class and *feel* which principle is straining — and know which direction to push to fix it. That is not knowledge. That is instinct. Instinct only comes from reps.

Let's go.

---

## Section 1 — Warm-Up: Name the Violation

Read each snippet. In one sentence, name the SOLID principle being violated and *why*. No fixing required. The goal is recognition speed.

---

### Snippet 1 — UserAccount (Level 1)

```python
class UserAccount:
    def __init__(self, username, password_hash, email):
        self.username = username
        self.password_hash = password_hash
        self.email = email

    def change_password(self, new_password):
        # Validate strength, hash, update
        ...

    def send_verification_email(self):
        # SMTP connection, MIME setup, send
        ...

    def generate_pdf_statement(self):
        # Use reportlab to render PDF
        ...

    def save_to_database(self):
        # SQL insert
        ...
```

**Your turn.** Which SOLID principle is violated, and why?

---

#### Solution

**Violation:** SRP (Single Responsibility Principle).

This class has *at least four distinct reasons to change*:

1. Authentication policy (password rules → `change_password`)
2. Email infrastructure (SMTP, sender, template → `send_verification_email`)
3. PDF rendering (library, layout → `generate_pdf_statement`)
4. Persistence (database schema, ORM → `save_to_database`)

Each of these is owned by a different concern. If the security team tightens password rules, this class is touched. If marketing changes the email template, this class is touched. If the DBA renames a column, this class is touched. Four unrelated stakeholders all pull on the same file.

> **What to take away:** When a class can be modified for reasons that have nothing to do with its core purpose, SRP is violated.

---

### Snippet 2 — ShapeAreaCalculator (Level 1)

```python
class ShapeAreaCalculator:
    def calculate(self, shape):
        if shape.type == "circle":
            return 3.14159 * shape.radius ** 2
        elif shape.type == "rectangle":
            return shape.width * shape.height
        elif shape.type == "triangle":
            return 0.5 * shape.base * shape.height
        else:
            raise ValueError(f"Unknown shape: {shape.type}")
```

**Your turn.** Which principle is violated?

---

#### Solution

**Violation:** OCP (Open/Closed Principle).

Adding a new shape — say, a `Hexagon` — *requires editing* `calculate`. You cannot extend this calculator without modifying its source. Every new shape carries a small but real risk of breaking the existing `if/elif` ladder. The class is "closed for extension" (you can't extend without editing) and "open for modification" (every new feature edits it) — exactly the opposite of what OCP demands.

> **What to take away:** Look for `if/elif` chains that branch on a type. They almost always signal an OCP violation. The fix is to let each type compute its own answer through a shared interface.

---

### Snippet 3 — Ostrich and Bird (Level 1)

```python
class Bird:
    def fly(self):
        print("Flying through the sky")

    def eat(self):
        print("Eating seeds")


class Ostrich(Bird):
    def fly(self):
        raise NotImplementedError("Ostriches can't fly")
```

**Your turn.** Which principle is violated?

---

#### Solution

**Violation:** LSP (Liskov Substitution Principle).

The `Bird` class promises an implicit contract: *every Bird can fly*. The `Ostrich` subclass breaks this contract by throwing instead of flying. Now any function that accepts a `Bird` and calls `fly()` will silently work for most birds but blow up for ostriches.

The right fix is **not** to wrap calls in `try/except`. That just shifts the bug. The right fix is to redesign the hierarchy so that `fly()` doesn't live on `Bird` at all — instead, only flying birds inherit from a `FlyingBird` subclass (or implement a `Flyable` interface).

> **What to take away:** Subclasses that override inherited methods with `NotImplementedError` are a smell. The base class is promising something the subclass cannot deliver — that promise was wrong.

---

### Snippet 4 — Worker and RobotWorker (Level 1)

```python
from abc import ABC, abstractmethod

class Worker(ABC):
    @abstractmethod
    def work(self): ...

    @abstractmethod
    def eat(self): ...

    @abstractmethod
    def sleep(self): ...


class RobotWorker(Worker):
    def work(self):
        print("Welding parts")

    def eat(self):
        pass  # robots don't eat

    def sleep(self):
        pass  # robots don't sleep
```

**Your turn.** Which principle is violated?

---

#### Solution

**Violation:** ISP (Interface Segregation Principle).

The `Worker` interface is *too fat*. `RobotWorker` is forced to implement two methods (`eat`, `sleep`) it has no use for, just to satisfy the interface contract. Empty `pass` implementations are a clear signal that the interface is doing too much.

The fix is to split the interface along its natural boundaries:

```python
class Workable(ABC):
    @abstractmethod
    def work(self): ...

class Eatable(ABC):
    @abstractmethod
    def eat(self): ...

class Sleepable(ABC):
    @abstractmethod
    def sleep(self): ...
```

`HumanWorker` implements all three. `RobotWorker` implements only `Workable`. No empty methods, no lies.

> **What to take away:** Empty `pass` implementations of inherited abstract methods almost always mean the interface should be split.

---

### Snippet 5 — OrderService (Level 1)

```python
class OrderService:
    def __init__(self):
        self.repository = MySQLOrderRepository(
            host="prod.db.internal", user="root", password="..."
        )
        self.notifier = GmailNotificationService(
            api_key="REAL_KEY_HERE"
        )

    def place_order(self, order):
        self.repository.save(order)
        self.notifier.send(order.customer_email, "Order confirmed")
```

**Your turn.** Which principle is violated?

---

#### Solution

**Violation:** DIP (Dependency Inversion Principle).

The high-level `OrderService` *creates its own* low-level concrete dependencies (`MySQLOrderRepository`, `GmailNotificationService`) inside its constructor. This causes two big problems:

1. **Untestable.** To create an `OrderService`, you need a live MySQL server and valid Gmail credentials. No unit test can run without real infrastructure.
2. **Unswappable.** Want to move from MySQL to PostgreSQL? You're editing `OrderService`. Want to add SMS notifications alongside Gmail? Editing `OrderService` again.

The fix is constructor injection — `OrderService` should accept abstractions (`OrderRepository`, `NotificationService`) through its constructor and let an outer "composition root" decide which concrete implementations to wire in.

> **What to take away:** If a class instantiates its own dependencies, you can usually neither test it nor swap them. DIP fixes both with one move.

---

## Section 2 — Single Responsibility Principle

### Problem 2.1 — BlogPost (Level 1)

A `BlogPost` class has the following methods:

```python
class BlogPost:
    def set_title(self, title): ...
    def set_content(self, content): ...
    def format_as_html(self): ...
    def format_as_markdown(self): ...
    def save_to_db(self): ...
    def email_to_subscribers(self): ...
```

**Your turn:**
1. How many distinct responsibilities does this class carry? Name them.
2. Which of those responsibilities will force a change to this class for reasons that have nothing to do with the blog post itself?

---

#### Solution

This class has **four distinct responsibilities**:

| # | Responsibility | Owner / Reason to change |
|---|---|---|
| 1 | Holding blog data (title, content) | The product/data model |
| 2 | Formatting (HTML / Markdown) | The frontend / publishing layer |
| 3 | Persistence (`save_to_db`) | The DBA / database schema |
| 4 | Notifications (`email_to_subscribers`) | The marketing / email infrastructure team |

**Which of these will cause unrelated changes to this class?**

- The day Marketing switches from SendGrid to AWS SES → `BlogPost` is edited, even though *nothing about a blog post has changed*.
- The day the database schema adds a new column → `BlogPost` is edited.
- The day the frontend wants a new Markdown flavour → `BlogPost` is edited.

Three of those four changes have **nothing to do with what a blog post is**. That's the SRP smell: a single file becoming a battleground for unrelated teams.

> **The fix in shape (no code yet):** `BlogPost` holds only data. `BlogFormatter` (with `HtmlFormatter`, `MarkdownFormatter` subclasses) handles formatting. `BlogRepository` handles persistence. `SubscriberNotifier` handles email. Each can change independently.

---

### Problem 2.2 — EmployeeReport (Level 2)

Here is some real-looking code. Read it, find the trouble, then refactor.

```python
class EmployeeReport:
    def __init__(self, employees):
        self.employees = employees

    def get_top_performers(self):
        return [e for e in self.employees if e.performance_score > 8.0]

    def format_as_table(self):
        header = f"{'Name':<20} {'Score':<10} {'Department':<15}\n"
        rows = "\n".join(
            f"{e.name:<20} {e.performance_score:<10} {e.department:<15}"
            for e in self.employees
        )
        return header + rows

    def save_to_csv(self, filepath):
        import csv
        with open(filepath, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'score', 'department'])
            writer.writeheader()
            for e in self.employees:
                writer.writerow({
                    'name': e.name,
                    'score': e.performance_score,
                    'department': e.department,
                })

    def send_to_hr(self, email_address):
        print(f"Emailing report to {email_address}")
```

**Your turn:**
1. Identify each responsibility crammed into this class.
2. Refactor it into separate classes, each with exactly one reason to change.
3. Show how the refactored pieces are composed together.

---

#### Solution

**Step 1 — Diagnose the responsibilities.**

`EmployeeReport` is doing four very different jobs:

| Method | Responsibility | Reason it might change |
|---|---|---|
| `get_top_performers` | Business analysis — who qualifies | HR raises the performance bar |
| `format_as_table` | Presentation — how it looks | Frontend wants a different layout |
| `save_to_csv` | Persistence — where it lives | Switching to JSON or Parquet |
| `send_to_hr` | Delivery — how HR receives it | Switching from print to SendGrid |

Each of those is a different stakeholder pulling on the same file. Worse, when `save_to_csv` is changed, the diff also touches code related to `format_as_table` — code review noise multiplies.

**Step 2 — Refactor into four focused classes.**

```python
# ---------------------------------------------------------------
# Responsibility 1: Analysis — who qualifies as a top performer?
# ---------------------------------------------------------------
class EmployeeAnalyser:
    """Pure business logic. No I/O. No formatting."""

    def __init__(self, employees):
        self.employees = employees

    def top_performers(self, threshold: float = 8.0):
        # Threshold is a parameter, not a hard-coded constant.
        # HR changes the bar without anyone touching this class.
        return [e for e in self.employees if e.performance_score > threshold]


# ---------------------------------------------------------------
# Responsibility 2: Formatting — how do we display the data?
# ---------------------------------------------------------------
class ReportFormatter:
    """Takes a list of employees, returns a string. That's all."""

    def as_table(self, employees) -> str:
        header = f"{'Name':<20} {'Score':<10} {'Department':<15}\n"
        rows = "\n".join(
            f"{e.name:<20} {e.performance_score:<10} {e.department:<15}"
            for e in employees
        )
        return header + rows


# ---------------------------------------------------------------
# Responsibility 3: Persistence — write to disk
# ---------------------------------------------------------------
class ReportExporter:
    """Takes employees, writes them somewhere durable."""

    def to_csv(self, employees, filepath: str) -> None:
        import csv
        with open(filepath, 'w') as f:
            writer = csv.DictWriter(
                f, fieldnames=['name', 'score', 'department']
            )
            writer.writeheader()
            for e in employees:
                writer.writerow({
                    'name': e.name,
                    'score': e.performance_score,
                    'department': e.department,
                })


# ---------------------------------------------------------------
# Responsibility 4: Delivery — get it to HR
# ---------------------------------------------------------------
class ReportDelivery:
    """Wraps the act of *sending* — print today, SendGrid tomorrow."""

    def email(self, recipient: str, content: str) -> None:
        # Tomorrow this becomes SendGrid or SES.
        # The analyser, formatter, and exporter don't care.
        print(f"Emailing to {recipient}:\n{content}")


# ---------------------------------------------------------------
# Composition — wiring the four pieces together (this is the
# "use site". A function here, a controller in a web app, etc.)
# ---------------------------------------------------------------
def run_weekly_report(employees, hr_email):
    analyser = EmployeeAnalyser(employees)
    formatter = ReportFormatter()
    exporter = ReportExporter()
    delivery = ReportDelivery()

    top = analyser.top_performers()
    table = formatter.as_table(top)

    exporter.to_csv(top, "weekly_top_performers.csv")
    delivery.email(hr_email, table)
```

**Step 3 — Why this is better.**

- **Swap the email system** without touching the formatter or analyser.
- **Add a JSON exporter** (`to_json`) without touching the CSV path.
- **Change the threshold** by passing a different number, not editing the class.
- **Test each piece in isolation** — pass a fake list of employees to `top_performers` and assert the result.

Each class now has exactly one reason to change. That is SRP in practice.

---

### Problem 2.3 — Restaurant Order System (Level 3)

Now design from scratch.

**Scenario:** A restaurant management system needs to handle orders.

- A waiter can **place**, **modify**, and **cancel** an order.
- Once placed, the **kitchen must be notified**.
- When an order is completed, the **billing system generates an invoice** and the **customer receives a receipt** (SMS or email — depending on what the customer prefers).

Design the classes correctly. You don't need to write full implementations for every method — class names, responsibilities, and key method signatures are enough. A short paragraph of design reasoning is mandatory.

---

#### Solution

**Design Decisions.**

The first thing to notice: there are at least *five* concerns hiding in this scenario.

1. **The order itself** — items, status, timestamps. Pure data.
2. **The kitchen** — needs a notification when an order is placed.
3. **Billing** — generates an invoice from an order.
4. **Receipts** — delivered via SMS *or* email; both are "kinds of delivery".
5. **Coordination** — *somebody* has to call these in the right order at the right time.

If we put any two of these in the same class, we've already lost SRP. The temptation to write a single `Order` class with `place()`, `notify_kitchen()`, `generate_invoice()`, `send_receipt()` is exactly what we're refusing.

Design:

- `Order` is data, plus a few state transitions. No I/O.
- `KitchenNotifier` is the kitchen's interface to the rest of the system. Print today; socket-to-kitchen-display tomorrow.
- `BillingService` produces an `Invoice` object from an `Order`.
- `ReceiptSender` is an abstraction; `SmsReceiptSender` and `EmailReceiptSender` are concretes. The customer's preference selects which one.
- `OrderService` is the *coordinator* — the one place where the lifecycle is choreographed.

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import List


# ---------------------------------------------------------------
# 1. Data — the order itself
# ---------------------------------------------------------------
class OrderStatus(Enum):
    PLACED = "placed"
    MODIFIED = "modified"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


@dataclass
class OrderItem:
    name: str
    quantity: int
    unit_price: float


@dataclass
class Order:
    """Pure data. Knows nothing about kitchens, bills, or receipts."""
    order_id: str
    customer_id: str
    items: List[OrderItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.PLACED


# ---------------------------------------------------------------
# 2. Kitchen — the kitchen's notification surface
# ---------------------------------------------------------------
class KitchenNotifier:
    def notify_new_order(self, order: Order) -> None:
        # Today: print. Tomorrow: TCP socket to the kitchen display.
        # The rest of the system doesn't care which.
        print(f"[KITCHEN] New order {order.order_id}: {order.items}")


# ---------------------------------------------------------------
# 3. Billing — produces an invoice from an order
# ---------------------------------------------------------------
@dataclass
class Invoice:
    order_id: str
    line_items: List[OrderItem]
    total: float


class BillingService:
    def generate_invoice(self, order: Order) -> Invoice:
        total = sum(it.unit_price * it.quantity for it in order.items)
        return Invoice(order.order_id, order.items, total)


# ---------------------------------------------------------------
# 4. Receipts — multiple delivery methods, one shape
# ---------------------------------------------------------------
class ReceiptSender(ABC):
    @abstractmethod
    def send(self, customer_id: str, invoice: Invoice) -> None: ...


class SmsReceiptSender(ReceiptSender):
    def send(self, customer_id: str, invoice: Invoice) -> None:
        print(f"[SMS to {customer_id}] Total: ₹{invoice.total}")


class EmailReceiptSender(ReceiptSender):
    def send(self, customer_id: str, invoice: Invoice) -> None:
        print(f"[EMAIL to {customer_id}] Total: ₹{invoice.total}")


# ---------------------------------------------------------------
# 5. Coordination — the only place the lifecycle is choreographed
# ---------------------------------------------------------------
class OrderService:
    """
    The coordinator. This is the one class that knows the order of
    operations — every other class minds its own business.
    """

    def __init__(
        self,
        kitchen: KitchenNotifier,
        billing: BillingService,
        receipt_sender: ReceiptSender,
    ):
        self.kitchen = kitchen
        self.billing = billing
        self.receipt_sender = receipt_sender

    def place_order(self, order: Order) -> None:
        # Order data is already valid by construction.
        self.kitchen.notify_new_order(order)

    def complete_order(self, order: Order) -> None:
        order.status = OrderStatus.COMPLETED
        invoice = self.billing.generate_invoice(order)
        self.receipt_sender.send(order.customer_id, invoice)
```

**Why this design holds up.**

- Switching from SMS to push notifications? Add a `PushReceiptSender(ReceiptSender)`. Wire it at the composition root. Nothing else changes.
- Changing the kitchen from "print" to "TCP socket to kitchen display"? Edit `KitchenNotifier`. Nothing else changes.
- Adding GST to the invoice? Edit `BillingService.generate_invoice`. Nothing else changes.
- `Order` itself never changes when the email format changes, the database schema changes, or the kitchen integration changes. That is SRP working.

---

## Section 3 — Open/Closed Principle

### Problem 3.1 — PaymentProcessor (Level 1)

```python
class PaymentProcessor:
    def process(self, payment):
        if payment.method == "card":
            # 30 lines of card processing
            ...
        elif payment.method == "upi":
            # 25 lines of UPI processing
            ...
        elif payment.method == "netbanking":
            # 40 lines of netbanking processing
            ...
        else:
            raise ValueError(f"Unknown method: {payment.method}")
```

**Your turn:** What happens when the business wants to add **crypto** payments next quarter? Why is that a problem? Which principle is being violated?

---

#### Solution

**Violation:** OCP (Open/Closed Principle).

Every new payment method forces an *edit* to `PaymentProcessor.process`. That's a problem for several reasons that compound:

1. **Regression risk.** Editing a tested method to add a branch can break the existing branches (a misplaced `elif`, a stray dependency import, a shared `try/except` that swallows the wrong exception).
2. **Diff noise.** Every new method puffs up the same file, making code review harder.
3. **Single point of contention.** If three teams add three payment methods in parallel, they'll all merge-conflict on this method.
4. **Testability suffers.** To add a crypto test, you also re-instantiate the entire `PaymentProcessor` — including the card, UPI, and netbanking code paths.

**The fix in shape:** make each payment method its own class implementing a common `PaymentMethod` interface. `PaymentProcessor.process` then becomes one line:

```python
return payment_method.process(payment)
```

Adding crypto is now adding a `CryptoPaymentMethod` class — *extending* the system without *modifying* the processor.

---

### Problem 3.2 — LogFormatter (Level 2)

```python
class LogFormatter:
    def format(self, log_entry, output_format: str) -> str:
        if output_format == "plain":
            return f"[{log_entry.level}] {log_entry.timestamp}: {log_entry.message}"
        elif output_format == "json":
            import json
            return json.dumps({
                "level": log_entry.level,
                "timestamp": str(log_entry.timestamp),
                "message": log_entry.message,
            })
        elif output_format == "csv":
            return f"{log_entry.level},{log_entry.timestamp},{log_entry.message}"
        else:
            raise ValueError(f"Unknown format: {output_format}")
```

**Your turn:** Refactor so that adding an XML or HTML format requires zero changes to existing code.

---

#### Solution

**Step 1 — Diagnose.**

Every new format is a modification. The class is a *change magnet*. The right move is to identify the abstraction: each format is a different way of *converting one log entry into one string*. That sentence is the interface.

**Step 2 — Refactor.**

```python
from abc import ABC, abstractmethod
import json


# ---------------------------------------------------------------
# The abstraction — every formatter shares this shape
# ---------------------------------------------------------------
class LogFormatter(ABC):
    @abstractmethod
    def format(self, log_entry) -> str:
        """Turn a single log entry into a string."""
        ...


# ---------------------------------------------------------------
# Concrete formatters — one per output format
# ---------------------------------------------------------------
class PlainFormatter(LogFormatter):
    def format(self, log_entry) -> str:
        return f"[{log_entry.level}] {log_entry.timestamp}: {log_entry.message}"


class JsonFormatter(LogFormatter):
    def format(self, log_entry) -> str:
        return json.dumps({
            "level": log_entry.level,
            "timestamp": str(log_entry.timestamp),
            "message": log_entry.message,
        })


class CsvFormatter(LogFormatter):
    def format(self, log_entry) -> str:
        return f"{log_entry.level},{log_entry.timestamp},{log_entry.message}"


# ---------------------------------------------------------------
# Adding XML: a NEW class. Zero changes to anything above.
# ---------------------------------------------------------------
class XmlFormatter(LogFormatter):
    def format(self, log_entry) -> str:
        return (
            f"<log>"
            f"<level>{log_entry.level}</level>"
            f"<timestamp>{log_entry.timestamp}</timestamp>"
            f"<message>{log_entry.message}</message>"
            f"</log>"
        )
```

**Step 3 — How the caller looks now.**

```python
def write_log(entry, formatter: LogFormatter, sink):
    """Sink is anything that accepts a string. The formatter is plug-in."""
    sink.write(formatter.format(entry))
```

The caller never asks "what format?". It receives a `LogFormatter` and uses it. The if-chain is gone. The system is **open for extension** (new formatter classes are welcome) and **closed for modification** (existing formatters don't change when new ones are added). That is OCP.

---

### Problem 3.3 — E-commerce Promotions (Level 3)

**Scenario:** An e-commerce platform applies promotions to orders. Today's promotions are:

- **FLAT** — ₹200 off any order above ₹1000
- **PERCENT** — 10% off
- **BUY_ONE_GET_ONE** — buy one item, get 50% off the second

Marketing intends to add a new promotion type every quarter — flash sales, loyalty bonuses, seasonal cashbacks. Design a promotions system where the core pricing engine **never** changes when a new promotion is added.

---

#### Solution

**Design Decisions.**

The naive design would be a `PricingEngine` with a giant `if promo.type == "FLAT"` block — and we already know how that ends. We need each promotion to *be its own object* that knows how to compute its own discount.

What does every promotion have in common? A single method: "given this order, what discount do you apply?" That's the interface.

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


# ---------------------------------------------------------------
# Domain
# ---------------------------------------------------------------
@dataclass
class OrderItem:
    name: str
    price: float
    quantity: int


@dataclass
class Order:
    items: List[OrderItem]

    def subtotal(self) -> float:
        return sum(it.price * it.quantity for it in self.items)


# ---------------------------------------------------------------
# The abstraction — anything that can reduce an order's total
# ---------------------------------------------------------------
class Promotion(ABC):
    @abstractmethod
    def apply(self, order: Order) -> float:
        """Return the discount amount (positive number) for this order."""
        ...


# ---------------------------------------------------------------
# Concrete promotions — one class per kind of deal
# ---------------------------------------------------------------
class FlatDiscount(Promotion):
    def __init__(self, amount: float, min_order_value: float):
        self.amount = amount
        self.min_order_value = min_order_value

    def apply(self, order: Order) -> float:
        if order.subtotal() < self.min_order_value:
            return 0.0
        return self.amount


class PercentDiscount(Promotion):
    def __init__(self, percent: float):
        self.percent = percent

    def apply(self, order: Order) -> float:
        return order.subtotal() * (self.percent / 100)


class BuyOneGetOneHalfOff(Promotion):
    def apply(self, order: Order) -> float:
        # Sum up half-off discount on every 2nd unit of each item.
        discount = 0.0
        for item in order.items:
            pairs = item.quantity // 2
            discount += pairs * item.price * 0.5
        return discount


# ---------------------------------------------------------------
# The pricing engine — never changes when promotions evolve
# ---------------------------------------------------------------
class PricingEngine:
    def __init__(self, promotions: List[Promotion]):
        self.promotions = promotions

    def final_price(self, order: Order) -> float:
        total_discount = sum(p.apply(order) for p in self.promotions)
        return max(0.0, order.subtotal() - total_discount)
```

**The extensibility check.**

Marketing announces a flash sale: "20% off, but only on Saturdays." Adding it is one new class — zero existing files touched:

```python
import datetime

class WeekendFlashSale(Promotion):
    def apply(self, order: Order) -> float:
        if datetime.date.today().weekday() < 5:   # Mon–Fri
            return 0.0
        return order.subtotal() * 0.20
```

**Why this matters.** The five-minute task is "write the new class". There is no code review of `PricingEngine` because `PricingEngine` did not change. There is no regression risk to the existing FLAT or PERCENT logic because their code did not change either. The principle is paying for itself the first time marketing comes with a new idea — and they will, every quarter.

---

## Section 4 — Liskov Substitution Principle

### Problem 4.1 — Rectangle and Square (Level 1)

This is the most famous LSP example in the literature. Read it carefully.

```python
class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    def set_width(self, w):
        self._width = w

    def set_height(self, h):
        self._height = h

    def area(self):
        return self._width * self._height


class Square(Rectangle):
    """A square is a rectangle where width == height. Right?"""

    def set_width(self, w):
        self._width = w
        self._height = w   # keep them equal

    def set_height(self, h):
        self._width = h
        self._height = h   # keep them equal


# Now a function that "should" work with any Rectangle:
def stretch_and_check(rect: Rectangle):
    rect.set_width(5)
    rect.set_height(10)
    assert rect.area() == 50   # ← fails when rect is a Square
```

**Your turn:** What happens when a `Square` is passed to `stretch_and_check`? Why does this violate LSP? What is the correct fix — and what is the *tempting but wrong* fix?

---

#### Solution

**What happens.** When a `Square` is passed in, `set_width(5)` sets both dimensions to 5. Then `set_height(10)` overwrites both to 10. The final area is **100**, not 50. The assertion fails. A function that worked perfectly for any `Rectangle` blows up the moment we substitute a "more specific" subtype.

**Why this violates LSP.** Liskov says: *anywhere your code expects a base type, you should be able to pass any subtype without surprise*. The `Rectangle` contract includes an implicit guarantee: "width and height are independent." `Square` silently breaks that guarantee by linking them.

**The tempting wrong fix.** Add `if isinstance(rect, Square)` checks inside `stretch_and_check`. This is *exactly* the wrong move. It scatters knowledge of `Square` everywhere a `Rectangle` is used, and defeats the purpose of polymorphism.

**The correct fix.** Recognise that `Square` is **not a behavioural subtype** of `Rectangle`. Geometrically it is. Behaviourally it isn't — because behaviourally, a Rectangle promises independent width and height, and a Square cannot honour that promise.

The right hierarchy treats them as siblings, not parent-child:

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2
```

> **The deep lesson:** LSP is about *behaviour*, not about *names* or *taxonomy*. "A square is a rectangle" is a mathematical statement, not a software-engineering one. Inheritance must follow behavioural compatibility, not real-world is-a relationships.

---

### Problem 4.2 — FileStorage and ReadOnlyStorage (Level 2)

```python
from abc import ABC, abstractmethod

class FileStorage(ABC):
    @abstractmethod
    def read(self, path: str) -> bytes: ...

    @abstractmethod
    def write(self, path: str, data: bytes) -> None: ...

    @abstractmethod
    def delete(self, path: str) -> None: ...


class LocalFileStorage(FileStorage):
    def read(self, path): ...
    def write(self, path, data): ...
    def delete(self, path): ...


class ReadOnlyCloudStorage(FileStorage):
    def read(self, path):
        # actual read from S3 or similar
        ...

    def write(self, path, data):
        raise PermissionError("This storage is read-only")

    def delete(self, path):
        raise PermissionError("This storage is read-only")
```

**Your turn:** Why does this violate LSP? Show the fix — and explain why catching the `PermissionError` in the caller is the wrong fix.

---

#### Solution

**The violation.** Any function that receives a `FileStorage` and calls `write()` will silently work for `LocalFileStorage` and blow up for `ReadOnlyCloudStorage`. The base type promises `write` works; a subtype breaks the promise. Classic LSP failure.

**Why "catch the exception" is the wrong fix.** It pushes the problem onto every caller, who must now wrap every `write` in `try/except` and decide what to do. The contract becomes "write may or may not raise depending on what you pass." That's not a contract — that's a guessing game.

**The right fix: redesign the hierarchy so the type system reflects capability.**

```python
from abc import ABC, abstractmethod


# Every storage can read. That is the minimum contract.
class ReadableStorage(ABC):
    @abstractmethod
    def read(self, path: str) -> bytes: ...


# Only writable storage extends Readable with write/delete.
class WritableStorage(ReadableStorage):
    @abstractmethod
    def write(self, path: str, data: bytes) -> None: ...

    @abstractmethod
    def delete(self, path: str) -> None: ...


# Local storage IS writable — full capability.
class LocalFileStorage(WritableStorage):
    def read(self, path):
        ...

    def write(self, path, data):
        ...

    def delete(self, path):
        ...


# Read-only cloud storage doesn't pretend to write. It doesn't
# inherit write at all — so it physically cannot break the contract.
class ReadOnlyCloudStorage(ReadableStorage):
    def read(self, path):
        ...
```

**How the callers change.**

```python
def display_file(path: str, storage: ReadableStorage):
    # Accepts EITHER readable or writable storage — both will work.
    data = storage.read(path)
    print(data)


def archive_file(src_path: str, dst_path: str, storage: WritableStorage):
    # Requires write capability. The type system PREVENTS you from
    # passing a ReadOnlyCloudStorage here. The bug is caught at the
    # call site, not at runtime in production.
    storage.write(dst_path, storage.read(src_path))
```

The exception is gone because the *situation that needed it* is gone. Code that needs writing accepts `WritableStorage`; the type system refuses to compile (or, in Python, mypy complains) if you try to pass a read-only one. That is LSP done right.

---

## Section 5 — Interface Segregation Principle

### Problem 5.1 — MultiFunctionPrinter (Level 1)

```python
from abc import ABC, abstractmethod

class MultiFunctionPrinter(ABC):
    @abstractmethod
    def print_document(self, doc): ...

    @abstractmethod
    def scan_document(self): ...

    @abstractmethod
    def fax_document(self, number): ...

    @abstractmethod
    def photocopy_document(self): ...


class InkjetPrinter(MultiFunctionPrinter):
    def print_document(self, doc):
        print(f"Printing {doc}")

    def scan_document(self):
        raise NotImplementedError("This printer can't scan")

    def fax_document(self, number):
        raise NotImplementedError("This printer can't fax")

    def photocopy_document(self):
        raise NotImplementedError("This printer can't photocopy")
```

**Your turn:** Which principle is violated? Sketch the fix in plain English (no code needed).

---

#### Solution

**Violation:** ISP.

`MultiFunctionPrinter` is a fat interface — it bundles four unrelated capabilities (print, scan, fax, photocopy) into one contract. Any class that wants to implement just one of these is forced to either lie (empty `pass`), throw (`NotImplementedError`), or pretend it can do things it can't.

**Secondary violation — LSP** also kicks in here, because `InkjetPrinter` throws on three of the four methods. ISP violations frequently produce LSP violations as collateral damage.

**The fix in shape.** Split the interface along its natural seams:

- `Printable` — has `print_document`
- `Scannable` — has `scan_document`
- `Faxable` — has `fax_document`
- `Photocopiable` — has `photocopy_document`

Then:

- `InkjetPrinter` implements `Printable` only.
- A `MultiFunctionMachine` implements all four.
- A `Scanner` implements `Scannable` only.

Now a client that just needs to print accepts a `Printable` — and it works with `InkjetPrinter`, `MultiFunctionMachine`, or any future class that learns to print. Nobody is forced to implement methods they cannot honour.

---

### Problem 5.2 — DataManager (Level 2)

```python
from abc import ABC, abstractmethod

class DataManager(ABC):
    @abstractmethod
    def read(self, key: str): ...

    @abstractmethod
    def write(self, key: str, value): ...

    @abstractmethod
    def delete(self, key: str): ...

    @abstractmethod
    def search(self, query: str) -> list: ...

    @abstractmethod
    def backup(self, destination: str) -> None: ...

    @abstractmethod
    def restore(self, source: str) -> None: ...


# Three implementers, each with VERY different needs:
class InMemoryCache(DataManager):       # only needs read/write/delete
    ...

class AnalyticsStore(DataManager):       # only needs write and search
    ...

class ArchiveStorage(DataManager):       # only needs backup and restore
    ...
```

**Your turn:** Refactor the interface hierarchy. Each implementer should declare *only* the capabilities it actually needs.

---

#### Solution

**Diagnose first.** Each of these three classes is dragged into implementing six methods when they each use two or three. When the signature of `backup(destination)` changes — say, it now needs an authentication token — the `InMemoryCache`, which has never backed up anything in its life, still has to be updated. That's friction without value.

**The refactor: split by capability.**

```python
from abc import ABC, abstractmethod
from typing import Any, List


# ---------------------------------------------------------------
# Capability interfaces — one trait per file in real codebases
# ---------------------------------------------------------------
class Readable(ABC):
    @abstractmethod
    def read(self, key: str) -> Any: ...


class Writable(ABC):
    @abstractmethod
    def write(self, key: str, value: Any) -> None: ...


class Deletable(ABC):
    @abstractmethod
    def delete(self, key: str) -> None: ...


class Searchable(ABC):
    @abstractmethod
    def search(self, query: str) -> List[Any]: ...


class Backupable(ABC):
    @abstractmethod
    def backup(self, destination: str) -> None: ...

    @abstractmethod
    def restore(self, source: str) -> None: ...


# ---------------------------------------------------------------
# Concrete classes — each implements ONLY what it needs
# ---------------------------------------------------------------
class InMemoryCache(Readable, Writable, Deletable):
    def __init__(self):
        self._store: dict = {}

    def read(self, key):
        return self._store.get(key)

    def write(self, key, value):
        self._store[key] = value

    def delete(self, key):
        self._store.pop(key, None)


class AnalyticsStore(Writable, Searchable):
    def __init__(self):
        self._events: List[Any] = []

    def write(self, key, value):
        self._events.append((key, value))

    def search(self, query):
        return [e for e in self._events if query in str(e)]


class ArchiveStorage(Backupable):
    def backup(self, destination):
        ...

    def restore(self, source):
        ...
```

**What's gained.**

- `InMemoryCache` no longer has six methods — only three. The class is half the size, with no fakes or stubs.
- A function that needs read access can declare `def fetch(store: Readable)` — and it works with `InMemoryCache`, any future read-only store, or any future read-write store. The function does not care which.
- Changing `backup`'s signature doesn't ripple to classes that don't back up anything.
- Each class's responsibilities are now visible *in its class declaration*: `class InMemoryCache(Readable, Writable, Deletable)` reads like a sentence describing exactly what the class does.

> **The rule of thumb:** if a single inheritance declaration would force a class to implement more than ~3 unrelated methods, split the interface.

---

## Section 6 — Dependency Inversion Principle

### Problem 6.1 — NotificationService (Level 1)

```python
class NotificationService:
    def __init__(self):
        self.sender = TwilioSMSSender(
            account_sid="REAL_SID",
            auth_token="REAL_TOKEN",
        )

    def send_alert(self, phone, message):
        self.sender.send(phone, message)
```

**Your turn:** Name two things that this class makes *impossible*.

---

#### Solution

**Violation:** DIP.

Two impossibilities flow directly from this design:

1. **Impossible to test without real infrastructure.** Try to instantiate `NotificationService()` in a unit test, and the constructor immediately reaches out to Twilio with real credentials. No live SID? Test fails on `__init__` — before any business logic has even run.

2. **Impossible to swap providers.** Twilio raises its prices. The team wants to move to Vonage. Today, doing that means editing `NotificationService`'s constructor. Tomorrow, *every other class that does the same trick* needs to be edited too — death by a thousand sites.

The class and the infrastructure are *fused*. DIP exists exactly to keep them separable.

**The fix in shape:** `NotificationService` should accept a `SmsSender` abstraction through its constructor. Production wires `TwilioSmsSender`; tests wire a `FakeSmsSender` that records calls in a list.

---

### Problem 6.2 — ReportService (Level 2)

```python
class ReportService:
    def __init__(self):
        self.db = PostgresDatabase(host="prod.db.internal", port=5432)
        self.cache = RedisCache(host="prod.cache.internal")
        self.mailer = SendGridMailer(api_key="REAL_KEY_HERE")

    def generate_and_send(self, report_id: str, recipient: str) -> None:
        cached = self.cache.get(f"report:{report_id}")
        if cached:
            content = cached
        else:
            data = self.db.fetch_report(report_id)
            content = self._process(data)
            self.cache.set(f"report:{report_id}", content)
        self.mailer.send(recipient, "Your Report", str(content))

    def _process(self, data):
        return data  # placeholder
```

**Your turn:**
1. What makes this class impossible to test as written?
2. Refactor it to use Dependency Injection.
3. Show a test that proves the refactored version works without any real database, cache, or email service.

---

#### Solution

**Part 1 — Why it's untestable.**

The constructor instantiates three pieces of live infrastructure: a PostgreSQL connection, a Redis client, and a SendGrid API client. *Just creating a `ReportService` object* requires:

- A reachable PostgreSQL server at `prod.db.internal:5432`
- A reachable Redis at `prod.cache.internal`
- A valid SendGrid API key

A unit test runs on a developer's laptop in 30 milliseconds. It cannot satisfy any of those. The class is welded to production.

**Part 2 — The refactor.**

```python
from abc import ABC, abstractmethod
from typing import Any, Optional


# ---------------------------------------------------------------
# Abstractions — the seams DIP creates
# ---------------------------------------------------------------
class Database(ABC):
    @abstractmethod
    def fetch_report(self, report_id: str) -> Any: ...


class Cache(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[Any]: ...

    @abstractmethod
    def set(self, key: str, value: Any) -> None: ...


class Mailer(ABC):
    @abstractmethod
    def send(self, to: str, subject: str, body: str) -> None: ...


# ---------------------------------------------------------------
# The service — depends only on abstractions
# ---------------------------------------------------------------
class ReportService:
    def __init__(self, db: Database, cache: Cache, mailer: Mailer):
        # ↑ The whole DIP fix lives in this signature.
        self.db = db
        self.cache = cache
        self.mailer = mailer

    def generate_and_send(self, report_id: str, recipient: str) -> None:
        cached = self.cache.get(f"report:{report_id}")
        if cached:
            content = cached
        else:
            data = self.db.fetch_report(report_id)
            content = self._process(data)
            self.cache.set(f"report:{report_id}", content)
        self.mailer.send(recipient, "Your Report", str(content))

    def _process(self, data):
        return data
```

In production, `main.py` wires the real concretes:

```python
# main.py — the "composition root"
service = ReportService(
    db=PostgresDatabase(host="prod.db.internal", port=5432),
    cache=RedisCache(host="prod.cache.internal"),
    mailer=SendGridMailer(api_key=os.environ["SENDGRID_KEY"]),
)
```

**Part 3 — A real test, with fakes.**

```python
# ---------------------------------------------------------------
# Fakes — implementations the test fully controls
# ---------------------------------------------------------------
class FakeDatabase(Database):
    def fetch_report(self, report_id):
        return {"id": report_id, "rows": [1, 2, 3]}


class FakeCache(Cache):
    def __init__(self):
        self._store = {}

    def get(self, key):
        return self._store.get(key)

    def set(self, key, value):
        self._store[key] = value


class FakeMailer(Mailer):
    def __init__(self):
        self.sent = []   # record every call for assertions

    def send(self, to, subject, body):
        self.sent.append((to, subject, body))


# ---------------------------------------------------------------
# The test — fast, isolated, deterministic
# ---------------------------------------------------------------
def test_report_is_sent_once():
    db = FakeDatabase()
    cache = FakeCache()
    mailer = FakeMailer()

    service = ReportService(db=db, cache=cache, mailer=mailer)
    service.generate_and_send("R001", "user@example.com")

    assert len(mailer.sent) == 1
    assert mailer.sent[0][0] == "user@example.com"
    assert mailer.sent[0][1] == "Your Report"


def test_second_call_hits_cache():
    db = FakeDatabase()
    cache = FakeCache()
    mailer = FakeMailer()

    service = ReportService(db=db, cache=cache, mailer=mailer)
    service.generate_and_send("R001", "user@example.com")
    service.generate_and_send("R001", "user@example.com")

    # The cache should have been populated after the first call,
    # so the second send should still work without a "fresh" fetch.
    assert len(mailer.sent) == 2
```

**What this proves.**

- No network calls. The test runs in microseconds.
- No shared state outside the test. Two runs cannot interfere.
- Behaviour can be asserted directly (`mailer.sent` is a list we own).
- The test exists *only because DIP was applied* — without it, no instance of `ReportService` could ever be created in the test environment.

---

### Problem 6.3 — Hospital Appointment System (Level 3)

**Scenario:** A hospital appointment system must:

1. Check doctor availability from a **calendar system**.
2. Send appointment confirmations via **WhatsApp or SMS** (per patient preference).
3. **Log every booking** for audit purposes.

The hospital is migrating from an old, in-house calendar API to a new vendor calendar API next quarter. Design the system so that the migration is a one-class swap, not a code-wide rewrite.

---

#### Solution

**Design Decisions.**

This is a case for DIP + a touch of Adapter (which is essentially DIP made polite when the two ends were not designed for each other).

We need three abstractions:

1. `DoctorCalendar` — "can you check this doctor's availability?"
2. `MessageSender` — "can you deliver this string to this person?"
3. `AuditLogger` — "can you record what happened?"

The `AppointmentService` depends only on these three abstractions. The "calendar migration" the brief warns about is solved before it starts: we'll have an `OldCalendarAdapter` today and a `NewCalendarAdapter` tomorrow. Both implement `DoctorCalendar`. The service sees only the abstraction.

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


# ===============================================================
# Abstractions — the contracts AppointmentService relies on
# ===============================================================

class DoctorCalendar(ABC):
    @abstractmethod
    def is_available(self, doctor_id: str, when: datetime) -> bool: ...

    @abstractmethod
    def book(self, doctor_id: str, when: datetime, patient_id: str) -> str:
        """Return a booking reference."""
        ...


class MessageSender(ABC):
    @abstractmethod
    def send(self, to: str, message: str) -> None: ...


class AuditLogger(ABC):
    @abstractmethod
    def log(self, event: str, payload: dict) -> None: ...


# ===============================================================
# Concrete implementations — interchangeable
# ===============================================================

# --- Calendar adapters (the migration story) -------------------
class OldCalendarAdapter(DoctorCalendar):
    """Wraps the in-house legacy calendar API in our interface."""

    def __init__(self, legacy_client):
        self._client = legacy_client

    def is_available(self, doctor_id, when):
        # Legacy API used a slot ID; we adapt it.
        return self._client.check_slot(doctor_id, when.isoformat())

    def book(self, doctor_id, when, patient_id):
        return self._client.create_booking(doctor_id, when.isoformat(), patient_id)


class NewCalendarAdapter(DoctorCalendar):
    """Wraps the new vendor calendar API in the SAME interface."""

    def __init__(self, vendor_sdk):
        self._sdk = vendor_sdk

    def is_available(self, doctor_id, when):
        return self._sdk.availability(doctor_id=doctor_id, datetime_iso=when.isoformat())

    def book(self, doctor_id, when, patient_id):
        return self._sdk.book_appointment(
            doctor=doctor_id, time=when, patient=patient_id
        )


# --- Messaging -------------------------------------------------
class WhatsAppSender(MessageSender):
    def send(self, to, message):
        print(f"[WA → {to}] {message}")


class SmsSender(MessageSender):
    def send(self, to, message):
        print(f"[SMS → {to}] {message}")


# --- Audit -----------------------------------------------------
class FileAuditLogger(AuditLogger):
    def __init__(self, filepath):
        self.filepath = filepath

    def log(self, event, payload):
        with open(self.filepath, "a") as f:
            f.write(f"{datetime.utcnow().isoformat()} {event} {payload}\n")


# ===============================================================
# The service — depends only on the three abstractions
# ===============================================================

@dataclass
class Patient:
    id: str
    contact: str
    prefers_whatsapp: bool


class AppointmentService:
    def __init__(
        self,
        calendar: DoctorCalendar,
        whatsapp: MessageSender,
        sms: MessageSender,
        audit: AuditLogger,
    ):
        self.calendar = calendar
        self.whatsapp = whatsapp
        self.sms = sms
        self.audit = audit

    def book_appointment(
        self, doctor_id: str, when: datetime, patient: Patient
    ) -> str:
        if not self.calendar.is_available(doctor_id, when):
            raise ValueError("Doctor unavailable at requested time")

        ref = self.calendar.book(doctor_id, when, patient.id)

        sender = self.whatsapp if patient.prefers_whatsapp else self.sms
        sender.send(
            patient.contact,
            f"Appointment confirmed with {doctor_id} at {when}. Ref: {ref}",
        )

        self.audit.log(
            "appointment_booked",
            {
                "doctor": doctor_id,
                "patient": patient.id,
                "when": when.isoformat(),
                "ref": ref,
            },
        )
        return ref


# ===============================================================
# Composition root — TODAY (using old calendar)
# ===============================================================
# service = AppointmentService(
#     calendar=OldCalendarAdapter(legacy_client),
#     whatsapp=WhatsAppSender(),
#     sms=SmsSender(),
#     audit=FileAuditLogger("/var/log/hospital/audit.log"),
# )

# ===============================================================
# Composition root — NEXT QUARTER (single-line change)
# ===============================================================
# service = AppointmentService(
#     calendar=NewCalendarAdapter(new_vendor_sdk),   # ← only this changes
#     whatsapp=WhatsAppSender(),
#     sms=SmsSender(),
#     audit=FileAuditLogger("/var/log/hospital/audit.log"),
# )
```

**Why this design satisfies the brief.**

- The migration from old to new calendar is *one line* in `main.py`. `AppointmentService` itself does not change, is not retested, is not redeployed.
- Both calendar adapters share the *same interface* — so the service can't tell which one it's holding.
- This is DIP wearing the costume of the Adapter pattern. They show up together so often that recognising the combination is itself an important skill — a "named pairing" you should expect in real systems.

---

## Section 7 — Combined Violations

Real code rarely violates only one principle. These problems train you to *disentangle* multiple issues, fix them in the right order, and explain each fix.

For every problem in this section, the solution opens with a **Diagnosis** that names each violation separately before any code appears. The refactor that follows uses numbered comments (`# Fix 1: SRP`, `# Fix 2: OCP`) that map back to the diagnosis.

---

### Problem 7.1 — LibrarySystem (SRP + OCP + DIP)

```python
class LibrarySystem:
    def __init__(self):
        self.books = {}
        self.db_conn = MySQLConnector("localhost", "library_db")

    def add_book(self, isbn, title, author, copies):
        self.books[isbn] = {"title": title, "author": author, "copies": copies}
        self.db_conn.execute(
            f"INSERT INTO books VALUES ('{isbn}', '{title}', {copies})"
        )

    def borrow_book(self, isbn, member_id):
        if isbn not in self.books or self.books[isbn]["copies"] < 1:
            print("Not available")
            return
        self.books[isbn]["copies"] -= 1
        self.db_conn.execute(
            f"UPDATE books SET copies=copies-1 WHERE isbn='{isbn}'"
        )
        # send email
        print(
            f"Email sent to member {member_id}: "
            f"you borrowed {self.books[isbn]['title']}"
        )
        # log it
        with open("library.log", "a") as f:
            f.write(f"Member {member_id} borrowed {isbn}\n")

    def generate_report(self, report_type):
        if report_type == "available":
            return {k: v for k, v in self.books.items() if v["copies"] > 0}
        elif report_type == "unavailable":
            return {k: v for k, v in self.books.items() if v["copies"] == 0}
        elif report_type == "all":
            return self.books
```

**Your turn:** Diagnose every violation, name them by principle, then refactor.

---

#### Solution

**Diagnosis.**

1. **SRP violation.** This class is at least four classes glued together:
   - Book state (the `self.books` dict)
   - Persistence (`self.db_conn` and the SQL writes)
   - Notification (the print-as-email)
   - Reporting (`generate_report` with its branches)
2. **OCP violation.** `generate_report` grows an `if/elif` chain for every new kind of report. Adding "most borrowed last 30 days" forces an edit.
3. **DIP violation.** `MySQLConnector` is created inside the constructor. The class can't be tested without MySQL, and a switch to PostgreSQL would mean editing this class.

There's also a latent **SQL injection** risk via the f-string queries, but that's a security concern; we'll fix it by going through a proper repository anyway.

**The refactor (in roughly the order the diagnosis suggests).**

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List


# ---------------------------------------------------------------
# Fix 1: SRP — extract a pure data class
# ---------------------------------------------------------------
@dataclass
class Book:
    isbn: str
    title: str
    author: str
    copies: int


class BookCatalogue:
    """Just the in-memory state of books. No DB, no email, no reports."""

    def __init__(self):
        self._books: Dict[str, Book] = {}

    def add(self, book: Book) -> None:
        self._books[book.isbn] = book

    def get(self, isbn: str) -> Book:
        if isbn not in self._books:
            raise KeyError(isbn)
        return self._books[isbn]

    def all(self) -> List[Book]:
        return list(self._books.values())

    def decrement(self, isbn: str) -> None:
        book = self.get(isbn)
        if book.copies < 1:
            raise ValueError("No copies available")
        book.copies -= 1


# ---------------------------------------------------------------
# Fix 2: DIP — abstract the persistence layer
# ---------------------------------------------------------------
class BookRepository(ABC):
    @abstractmethod
    def save(self, book: Book) -> None: ...

    @abstractmethod
    def update_copies(self, isbn: str, copies: int) -> None: ...


class MySqlBookRepository(BookRepository):
    def __init__(self, connector):
        self._db = connector

    def save(self, book):
        # Parameterised — no SQL injection this time around.
        self._db.execute(
            "INSERT INTO books VALUES (%s, %s, %s, %s)",
            (book.isbn, book.title, book.author, book.copies),
        )

    def update_copies(self, isbn, copies):
        self._db.execute(
            "UPDATE books SET copies=%s WHERE isbn=%s",
            (copies, isbn),
        )


# ---------------------------------------------------------------
# Fix 1 (continued): SRP — extract notifications
# ---------------------------------------------------------------
class BorrowNotifier(ABC):
    @abstractmethod
    def notify(self, member_id: str, book: Book) -> None: ...


class EmailBorrowNotifier(BorrowNotifier):
    def notify(self, member_id, book):
        print(f"[EMAIL → member {member_id}] You borrowed: {book.title}")


# ---------------------------------------------------------------
# Fix 1 (continued): SRP — extract audit logging
# ---------------------------------------------------------------
class AuditLogger(ABC):
    @abstractmethod
    def log(self, message: str) -> None: ...


class FileAuditLogger(AuditLogger):
    def __init__(self, path: str):
        self.path = path

    def log(self, message: str):
        with open(self.path, "a") as f:
            f.write(message + "\n")


# ---------------------------------------------------------------
# Fix 3: OCP — reports become polymorphic
# ---------------------------------------------------------------
class Report(ABC):
    @abstractmethod
    def generate(self, catalogue: BookCatalogue) -> List[Book]: ...


class AvailableReport(Report):
    def generate(self, catalogue):
        return [b for b in catalogue.all() if b.copies > 0]


class UnavailableReport(Report):
    def generate(self, catalogue):
        return [b for b in catalogue.all() if b.copies == 0]


class AllBooksReport(Report):
    def generate(self, catalogue):
        return catalogue.all()


# Adding "MostBorrowedLast30Days" = ONE new class. Zero changes here.

class ReportGenerator:
    """Just dispatches to whichever Report you hand it."""

    def run(self, report: Report, catalogue: BookCatalogue):
        return report.generate(catalogue)


# ---------------------------------------------------------------
# The coordinator — depends only on abstractions
# ---------------------------------------------------------------
class LibraryService:
    def __init__(
        self,
        catalogue: BookCatalogue,
        repo: BookRepository,
        notifier: BorrowNotifier,
        audit: AuditLogger,
    ):
        self.catalogue = catalogue
        self.repo = repo
        self.notifier = notifier
        self.audit = audit

    def add_book(self, book: Book) -> None:
        self.catalogue.add(book)
        self.repo.save(book)

    def borrow_book(self, isbn: str, member_id: str) -> None:
        self.catalogue.decrement(isbn)              # may raise
        book = self.catalogue.get(isbn)
        self.repo.update_copies(isbn, book.copies)
        self.notifier.notify(member_id, book)
        self.audit.log(f"member={member_id} borrowed isbn={isbn}")
```

**What we gained, in concrete terms.**

- **Testability.** `LibraryService` can be unit-tested by passing fakes for `BookRepository`, `BorrowNotifier`, and `AuditLogger`. No MySQL, no file system, no email.
- **Database switch.** Moving from MySQL to PostgreSQL is a new `PostgresBookRepository` class. `LibraryService` is untouched.
- **New report types.** Adding "most borrowed last 30 days" is one new `Report` subclass. The reporting machinery does not change.
- **No more SQL injection.** Centralising queries in the repository made it easy to use parameter binding.

---

### Problem 7.2 — Animal Hierarchy (LSP + ISP + DIP)

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def eat(self): ...

    @abstractmethod
    def sleep(self): ...

    @abstractmethod
    def fly(self): ...

    @abstractmethod
    def swim(self): ...


class Eagle(Animal):
    def eat(self): print("Eagle eats")
    def sleep(self): print("Eagle sleeps")
    def fly(self): print("Eagle soars")
    def swim(self): raise NotImplementedError("Eagles don't swim")


class Fish(Animal):
    def eat(self): print("Fish eats")
    def sleep(self): print("Fish rests")
    def fly(self): raise NotImplementedError("Fish don't fly")
    def swim(self): print("Fish swims")


class Dog(Animal):
    def eat(self): print("Dog eats")
    def sleep(self): print("Dog sleeps")
    def fly(self): raise NotImplementedError("Dogs don't fly")
    def swim(self): raise NotImplementedError("Dogs don't swim")


class ZooSimulator:
    def __init__(self):
        self.animals: list[Animal] = []

    def run_air_show(self):
        for a in self.animals:
            if isinstance(a, Eagle):    # ← the smell
                a.fly()

    def run_aquarium(self):
        for a in self.animals:
            if isinstance(a, Fish):     # ← same smell
                a.swim()
```

**Your turn:** Diagnose every violation, then redesign.

---

#### Solution

**Diagnosis.**

1. **ISP violation.** `Animal` is a fat interface. It promises four capabilities (`eat`, `sleep`, `fly`, `swim`) — but no real animal has all four. Each subclass is forced to implement methods it cannot honour.
2. **LSP violation.** `Eagle`, `Fish`, and `Dog` throw `NotImplementedError` on inherited methods. Any code that holds an `Animal` and calls `fly()` will work for eagles, fail for fish and dogs. The base class's contract is a lie.
3. **DIP violation.** `ZooSimulator` does `isinstance(a, Eagle)` checks to decide what to call. The high-level simulator now *depends on concrete subclasses* and must be edited whenever a new flying or swimming animal is added.

These three violations are interlocking: the fat `Animal` interface (ISP) forces subclasses to break contracts (LSP), which in turn forces clients to use isinstance guards (DIP).

**The fix: capability-based design with Protocols.**

```python
from typing import Protocol, runtime_checkable, List


# ---------------------------------------------------------------
# Fix 1+2: ISP + LSP — split capabilities into small protocols
# ---------------------------------------------------------------
# Using typing.Protocol means classes don't even have to inherit;
# they just need to have the matching method. This is "structural"
# typing — and it pairs perfectly with ISP.

@runtime_checkable
class Eatable(Protocol):
    def eat(self) -> None: ...


@runtime_checkable
class Sleepable(Protocol):
    def sleep(self) -> None: ...


@runtime_checkable
class Flyable(Protocol):
    def fly(self) -> None: ...


@runtime_checkable
class Swimmable(Protocol):
    def swim(self) -> None: ...


# ---------------------------------------------------------------
# Concrete animals — implement EXACTLY what they can do
# ---------------------------------------------------------------
class Eagle:
    def eat(self):
        print("Eagle eats")

    def sleep(self):
        print("Eagle sleeps")

    def fly(self):
        print("Eagle soars")
    # No swim method — and that's fine.


class Fish:
    def eat(self):
        print("Fish eats")

    def sleep(self):
        print("Fish rests")

    def swim(self):
        print("Fish swims")
    # No fly method — and that's fine.


class Dog:
    def eat(self):
        print("Dog eats")

    def sleep(self):
        print("Dog sleeps")
    # No fly, no swim — and that's fine.


# ---------------------------------------------------------------
# Fix 3: DIP — ZooSimulator depends on CAPABILITIES, not types
# ---------------------------------------------------------------
class ZooSimulator:
    def __init__(
        self,
        flyers: List[Flyable],
        swimmers: List[Swimmable],
    ):
        # The simulator accepts lists by capability.
        # It cannot accidentally be handed a dog as a "flyer" —
        # mypy would refuse, and at runtime isinstance() would say no.
        self.flyers = flyers
        self.swimmers = swimmers

    def run_air_show(self):
        for f in self.flyers:
            f.fly()        # No isinstance check. No exception risk.

    def run_aquarium(self):
        for s in self.swimmers:
            s.swim()


# ---------------------------------------------------------------
# Composition root
# ---------------------------------------------------------------
zoo = ZooSimulator(
    flyers=[Eagle(), Eagle()],
    swimmers=[Fish(), Fish(), Fish()],
)
zoo.run_air_show()    # safe — every entry can fly
zoo.run_aquarium()    # safe — every entry can swim
```

**What disappeared.**

- The `NotImplementedError`s — gone, because the methods don't exist on classes that can't do them.
- The `isinstance` guards — gone, because the simulator accepts capability-typed lists.
- The fragile, lying `Animal` base class — gone, because nothing needs to call itself "an Animal" for the simulator to work.

The three violations were really one violation seen from three angles, and they collapse together when you let each animal declare exactly what it can do.

---

## Section 8 — Capstone: Full Refactor Challenge

This is the hardest problem in the file. Set aside **45–60 minutes**.

### Problem 8.1 — HospitalSystem (The Full Refactor)

```python
class HospitalSystem:
    def __init__(self):
        # Hardwired DB connection — DIP issue
        self.db = PostgresDatabase(
            host="prod.db.internal",
            port=5432,
            user="root",
            password="REAL_PASSWORD",
        )
        # Hardwired SMS provider — DIP issue
        self.twilio = TwilioClient(
            account_sid="REAL_SID",
            auth_token="REAL_TOKEN",
        )
        self.patients = {}

    def register_patient(self, patient_id, name, age, contact):
        self.patients[patient_id] = {
            "name": name,
            "age": age,
            "contact": contact,
        }
        self.db.execute(
            f"INSERT INTO patients VALUES "
            f"('{patient_id}', '{name}', {age}, '{contact}')"
        )

    def book_appointment(self, patient_id, doctor_id, appointment_type):
        # OCP issue — if/elif on type
        if appointment_type == "general":
            fee = 500
        elif appointment_type == "specialist":
            fee = 1500
        elif appointment_type == "emergency":
            fee = 3000 + 500  # surcharge
        else:
            raise ValueError("Unknown appointment type")

        # SRP issue — booking, fee calc, SMS, audit all here
        self.db.execute(
            f"INSERT INTO appointments VALUES "
            f"('{patient_id}', '{doctor_id}', '{appointment_type}', {fee})"
        )

        # SRP + DIP issue — SMS hardwired and inline
        contact = self.patients[patient_id]["contact"]
        self.twilio.send_sms(
            to=contact,
            body=f"Appt with {doctor_id} confirmed. Fee: ₹{fee}",
        )

        # SRP issue — audit log directly to file
        with open("/var/log/hospital/audit.log", "a") as f:
            f.write(f"BOOKING {patient_id} {doctor_id} {appointment_type}\n")

        return fee

    def generate_invoice(self, patient_id):
        # SRP issue — this method computes, formats, AND writes
        appointments = self.db.fetch(
            f"SELECT * FROM appointments WHERE patient_id='{patient_id}'"
        )
        total = sum(a["fee"] for a in appointments)
        invoice_text = f"Invoice for {patient_id}\n"
        for a in appointments:
            invoice_text += f"  {a['type']:<15} ₹{a['fee']}\n"
        invoice_text += f"TOTAL: ₹{total}"
        with open(f"invoices/{patient_id}.txt", "w") as f:
            f.write(invoice_text)
        return invoice_text
```

**Your turn:**

1. Identify every SOLID violation by name, referencing specific lines.
2. Draw the class diagram (or write class names + responsibilities + interfaces in a list).
3. Implement the refactored system.
4. Write at least one test proving that a booking can be exercised without a real database, real Twilio, or real filesystem.

---

#### Solution

##### Step 1 — Diagnosis

| # | Principle | Where | What's wrong |
|---|---|---|---|
| 1 | **DIP** | `__init__` lines 4–11 | Constructs `PostgresDatabase` and `TwilioClient` directly — untestable, unswappable. |
| 2 | **SRP** | The whole class | At least five jobs: patient state, persistence, fee calculation, notifications, audit logging, invoice generation. |
| 3 | **OCP** | `book_appointment` lines 25–32 | `if/elif` on `appointment_type` — adding a new type means editing this method. |
| 4 | **SRP + DIP** | `book_appointment` lines 45–48 | SMS dispatch is inline with hardwired Twilio. |
| 5 | **SRP** | `book_appointment` lines 51–53 | Audit logging is opening a file directly. |
| 6 | **SRP** | `generate_invoice` | Three jobs in one method: compute, format, write. |

Also a **security smell**: f-string SQL building everywhere. The refactor pushes all SQL into the repository, where it can be parameterised once and forever.

##### Step 2 — Class Design

| Class | Responsibility | Implements / Inherits |
|---|---|---|
| `Patient` | Data only | dataclass |
| `Appointment` | Data only | dataclass |
| `Invoice` | Data only | dataclass |
| `Database` | Persistence abstraction | ABC |
| `PostgresDatabase` | Concrete Postgres persistence | `Database` |
| `MessageSender` | Notification abstraction | ABC |
| `TwilioSmsSender` | Concrete SMS via Twilio | `MessageSender` |
| `AuditLogger` | Audit abstraction | ABC |
| `FileAuditLogger` | Concrete file-based audit | `AuditLogger` |
| `AppointmentType` | One pricing policy | ABC |
| `GeneralAppointment` / `SpecialistAppointment` / `EmergencyAppointment` | Concrete pricing | `AppointmentType` |
| `InvoiceFormatter` | Turn invoice → string | — |
| `InvoiceStore` | Write invoice somewhere | ABC + `FileInvoiceStore` |
| `HospitalService` | Coordinator | depends on every abstraction |

##### Step 3 — The Refactored Code

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List


# ===============================================================
# Domain — pure data
# ===============================================================
@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    contact: str


@dataclass
class Appointment:
    patient_id: str
    doctor_id: str
    type_name: str
    fee: float


@dataclass
class Invoice:
    patient_id: str
    appointments: List[Appointment]
    total: float


# ===============================================================
# Fix 1: DIP — Database abstraction + Postgres concrete
# ===============================================================
class Database(ABC):
    @abstractmethod
    def save_patient(self, patient: Patient) -> None: ...

    @abstractmethod
    def save_appointment(self, appt: Appointment) -> None: ...

    @abstractmethod
    def list_appointments(self, patient_id: str) -> List[Appointment]: ...


class PostgresDatabase(Database):
    def __init__(self, connector):
        self._conn = connector

    def save_patient(self, patient):
        self._conn.execute(
            "INSERT INTO patients VALUES (%s, %s, %s, %s)",
            (patient.patient_id, patient.name, patient.age, patient.contact),
        )

    def save_appointment(self, appt):
        self._conn.execute(
            "INSERT INTO appointments VALUES (%s, %s, %s, %s)",
            (appt.patient_id, appt.doctor_id, appt.type_name, appt.fee),
        )

    def list_appointments(self, patient_id):
        rows = self._conn.fetch(
            "SELECT * FROM appointments WHERE patient_id=%s",
            (patient_id,),
        )
        return [Appointment(**r) for r in rows]


# ===============================================================
# Fix 1: DIP — Notification abstraction
# ===============================================================
class MessageSender(ABC):
    @abstractmethod
    def send(self, to: str, message: str) -> None: ...


class TwilioSmsSender(MessageSender):
    def __init__(self, twilio_client):
        self._twilio = twilio_client

    def send(self, to, message):
        self._twilio.send_sms(to=to, body=message)


# ===============================================================
# Fix 1: DIP — Audit abstraction
# ===============================================================
class AuditLogger(ABC):
    @abstractmethod
    def log(self, event: str) -> None: ...


class FileAuditLogger(AuditLogger):
    def __init__(self, path):
        self.path = path

    def log(self, event):
        with open(self.path, "a") as f:
            f.write(event + "\n")


# ===============================================================
# Fix 2: OCP — Appointment types as polymorphic objects
# ===============================================================
class AppointmentType(ABC):
    name: str = "abstract"

    @abstractmethod
    def fee(self) -> float: ...


class GeneralAppointment(AppointmentType):
    name = "general"
    def fee(self):
        return 500.0


class SpecialistAppointment(AppointmentType):
    name = "specialist"
    def fee(self):
        return 1500.0


class EmergencyAppointment(AppointmentType):
    name = "emergency"
    def fee(self):
        return 3000.0 + 500.0   # surcharge


# Adding TeleConsult = one new AppointmentType subclass. Zero edits.

# ===============================================================
# Fix 3: SRP — Invoicing split into compute / format / store
# ===============================================================
class InvoiceCalculator:
    def calculate(self, patient_id: str, appts: List[Appointment]) -> Invoice:
        total = sum(a.fee for a in appts)
        return Invoice(patient_id, appts, total)


class InvoiceFormatter:
    def as_text(self, invoice: Invoice) -> str:
        lines = [f"Invoice for {invoice.patient_id}"]
        for a in invoice.appointments:
            lines.append(f"  {a.type_name:<15} ₹{a.fee}")
        lines.append(f"TOTAL: ₹{invoice.total}")
        return "\n".join(lines)


class InvoiceStore(ABC):
    @abstractmethod
    def save(self, patient_id: str, content: str) -> None: ...


class FileInvoiceStore(InvoiceStore):
    def __init__(self, directory):
        self.directory = directory

    def save(self, patient_id, content):
        with open(f"{self.directory}/{patient_id}.txt", "w") as f:
            f.write(content)


# ===============================================================
# The coordinator — owns NO concrete dependencies
# ===============================================================
class HospitalService:
    def __init__(
        self,
        db: Database,
        sms: MessageSender,
        audit: AuditLogger,
        calculator: InvoiceCalculator,
        formatter: InvoiceFormatter,
        invoice_store: InvoiceStore,
    ):
        self.db = db
        self.sms = sms
        self.audit = audit
        self.calculator = calculator
        self.formatter = formatter
        self.invoice_store = invoice_store
        self._patients: Dict[str, Patient] = {}

    def register_patient(self, patient: Patient) -> None:
        self._patients[patient.patient_id] = patient
        self.db.save_patient(patient)
        self.audit.log(f"REGISTER {patient.patient_id}")

    def book_appointment(
        self,
        patient_id: str,
        doctor_id: str,
        appointment_type: AppointmentType,
    ) -> float:
        patient = self._patients[patient_id]
        appt = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            type_name=appointment_type.name,
            fee=appointment_type.fee(),
        )
        self.db.save_appointment(appt)
        self.sms.send(
            patient.contact,
            f"Appt with {doctor_id} confirmed. Fee: ₹{appt.fee}",
        )
        self.audit.log(
            f"BOOKING {patient_id} {doctor_id} {appointment_type.name}"
        )
        return appt.fee

    def generate_invoice(self, patient_id: str) -> str:
        appts = self.db.list_appointments(patient_id)
        invoice = self.calculator.calculate(patient_id, appts)
        text = self.formatter.as_text(invoice)
        self.invoice_store.save(patient_id, text)
        return text
```

##### Step 4 — A Real Test, With Fakes

```python
# ---------------------------------------------------------------
# Fakes — implementations we fully control
# ---------------------------------------------------------------
class FakeDatabase(Database):
    def __init__(self):
        self.saved_patients = []
        self.saved_appointments = []

    def save_patient(self, patient):
        self.saved_patients.append(patient)

    def save_appointment(self, appt):
        self.saved_appointments.append(appt)

    def list_appointments(self, patient_id):
        return [a for a in self.saved_appointments if a.patient_id == patient_id]


class FakeSmsSender(MessageSender):
    def __init__(self):
        self.sent = []

    def send(self, to, message):
        self.sent.append((to, message))


class FakeAuditLogger(AuditLogger):
    def __init__(self):
        self.events = []

    def log(self, event):
        self.events.append(event)


class FakeInvoiceStore(InvoiceStore):
    def __init__(self):
        self.saved = {}

    def save(self, patient_id, content):
        self.saved[patient_id] = content


# ---------------------------------------------------------------
# The test — pure logic. No DB, no Twilio, no filesystem.
# ---------------------------------------------------------------
def test_booking_fires_sms_audit_and_persists():
    db = FakeDatabase()
    sms = FakeSmsSender()
    audit = FakeAuditLogger()
    service = HospitalService(
        db=db,
        sms=sms,
        audit=audit,
        calculator=InvoiceCalculator(),
        formatter=InvoiceFormatter(),
        invoice_store=FakeInvoiceStore(),
    )

    service.register_patient(
        Patient("P001", "Asha", 30, "+91-99999-99999")
    )

    fee = service.book_appointment(
        patient_id="P001",
        doctor_id="D-CARDIO-01",
        appointment_type=SpecialistAppointment(),
    )

    # Fee policy correct?
    assert fee == 1500.0

    # Persisted to DB?
    assert len(db.saved_appointments) == 1
    assert db.saved_appointments[0].doctor_id == "D-CARDIO-01"

    # SMS sent to correct contact?
    assert len(sms.sent) == 1
    assert sms.sent[0][0] == "+91-99999-99999"

    # Audited?
    assert any("BOOKING" in e for e in audit.events)
```

##### What We Gained

In concrete, line-of-code terms:

- **Switch Twilio → Vonage:** one line in `main.py`. Write a `VonageSmsSender(MessageSender)`. Done.
- **Switch Postgres → MySQL:** one line in `main.py`. Write `MySqlDatabase(Database)`. Done.
- **Add a TeleConsult appointment type with a different fee structure:** one new `TeleConsultAppointment(AppointmentType)`. Done.
- **Stop writing invoices to disk and email them instead:** new `EmailInvoiceStore(InvoiceStore)`. The coordinator never knows.
- **Unit tests run in milliseconds** with no network, no disk, no live credentials. CI builds drop from minutes to seconds.

The original 60-line class is now 12 small, focused classes plus 1 coordinator. The total line count is higher — but every individual file is now small enough that a new engineer can fully understand it in five minutes. *That* is the trade SOLID asks you to make.

---

## Summary Checklist

Print this. Keep it next to your monitor. Use it as a code review aid for your own designs.

```
SRP  □ Does this class have more than one reason to change?
     □ Would a name like "XAndY" or "XManager" describe it better than "X"?
     □ Are unrelated stakeholders likely to pull on this file?

OCP  □ Does adding a new variant require modifying this class?
     □ Is there an if/elif chain that grows with new features?
     □ Could I add a new type by writing a new class instead of editing?

LSP  □ Do any subclasses raise NotImplementedError for inherited methods?
     □ Does any code need isinstance checks to "protect" against a subclass?
     □ Do subclasses honour every promise the base class makes?

ISP  □ Do implementers inherit methods they never use?
     □ Would a client that needs 1 method be forced to import 10?
     □ Are there empty pass implementations of abstract methods?

DIP  □ Does this class instantiate its own dependencies?
     □ Is this class impossible to test without real infrastructure?
     □ Are high-level policies coupled to low-level details?
```

### One last piece of advice

You will be tempted, the moment you finish this workbook, to apply SOLID *everywhere*. Don't. The principles have a cost — more classes, more files, more indirection. Pay that cost where the benefit is real (change is likely, testing matters, multiple stakeholders touch the code). For a 30-line script you'll throw away tomorrow, **a function is enough**.

The skill is not "always use SOLID." The skill is "see when SOLID is paying for itself, and apply it then." Reps in this workbook are how you build the eye for it.

---

*This content is part of **Codeverra** — a platform for learning coding, data science, DSA, and AI from scratch.*
*Explore more: https://codeverra.com*
