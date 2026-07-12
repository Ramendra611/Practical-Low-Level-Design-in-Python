# SOLID Principles — A Deep Dive

> **Who this is for:** Anyone comfortable with Python OOP (classes, inheritance, polymorphism, abstraction) who now wants to write code that *scales* — code that welcomes change rather than fights it.

---

## Table of Contents

1. [Why SOLID Exists — The Pain of "Just Classes"](#1-why-solid-exists)
2. [What SOLID Stands For](#2-what-solid-stands-for)
3. [S — Single Responsibility Principle (SRP)](#3-single-responsibility-principle-srp)
4. [O — Open/Closed Principle (OCP)](#4-openclosed-principle-ocp)
5. [L — Liskov Substitution Principle (LSP)](#5-liskov-substitution-principle-lsp)
6. [I — Interface Segregation Principle (ISP)](#6-interface-segregation-principle-isp)
7. [D — Dependency Inversion Principle (DIP)](#7-dependency-inversion-principle-dip)
8. [How the Five Principles Reinforce Each Other](#8-how-the-five-principles-reinforce-each-other)
9. [A Capstone Example — Applying All Five Together](#9-capstone-example)
10. [Common Pitfalls and Anti-Patterns](#10-common-pitfalls)
11. [When NOT to Apply SOLID](#11-when-not-to-apply-solid)
12. [Summary & Key Takeaways](#12-summary)
13. [Self-Assessment Test](#13-self-assessment-test)
14. [Practice Exercises with Solutions](#14-practice-exercises)

---

## 1. Why SOLID Exists

You've learned OOP. You can build classes. You know inheritance and polymorphism. So why isn't that enough?

Let's see with a story.

You join a startup. The codebase has 50 classes. You add a new payment method — it takes two days, touches six files, breaks two unrelated tests. You fix them. The next week, someone else adds a feature; it breaks *your* feature. A month later, the word "refactor" strikes fear in the team. Sprint after sprint, velocity drops. Bugs multiply.

This is not a "Python problem" or an "OOP problem." It's a **design** problem. The classes exist, but they're entangled. Change propagates like wildfire.

OOP gave you the raw materials — classes, objects, inheritance, polymorphism. But raw materials don't guarantee good architecture, just as owning bricks doesn't guarantee a good house.

**SOLID is a set of five principles that tell you how to arrange those raw materials so the resulting system is:**

- **Flexible** — easy to extend with new features.
- **Robust** — a change in one place doesn't ripple everywhere.
- **Testable** — you can test pieces in isolation.
- **Readable** — each piece has a clear purpose.

### An Analogy

Think of SOLID as the "grammar" of OOP. OOP gives you vocabulary (nouns = classes, verbs = methods). SOLID tells you how to arrange them into sentences that make sense and don't collapse under their own weight.

Or: OOP is knowing *how* to build walls; SOLID is knowing *where* to put walls so the building doesn't fall down when you renovate the kitchen.

### A Historical Note

The principles were popularized by **Robert C. Martin** (a.k.a. "Uncle Bob") in the early 2000s. The acronym SOLID was coined later by Michael Feathers. These aren't laws — they're *heuristics* distilled from decades of industry pain. Follow them *thoughtfully*, not dogmatically.

---

## 2. What SOLID Stands For

| Letter | Name | One-Line Essence |
|---|---|---|
| **S** | Single Responsibility Principle | A class should have one, and only one, reason to change. |
| **O** | Open/Closed Principle | Open for extension, closed for modification. |
| **L** | Liskov Substitution Principle | Subtypes must be substitutable for their base types. |
| **I** | Interface Segregation Principle | Clients shouldn't be forced to depend on interfaces they don't use. |
| **D** | Dependency Inversion Principle | Depend on abstractions, not concretions. |

Let's understand each deeply.

---

## 3. Single Responsibility Principle (SRP)

> **"A class should have one, and only one, reason to change."**
> — Robert C. Martin

### What it really means

At first glance people misread SRP as *"a class should do only one thing."* That's too vague. What counts as "one thing"? A `User` class "does" lots of things — has a name, has an email, maybe validates the email, maybe saves itself, maybe sends notifications.

The precise formulation is:

> **A class should have exactly one stakeholder (or reason) that would ever demand changes to it.**

"Reason to change" = "a stakeholder asks for a change." Different stakeholders = different reasons = different responsibilities.

### The Pain Without SRP

Consider this class:

```python
class Employee:
    def __init__(self, name, hours_worked, hourly_rate):
        self.name = name
        self.hours_worked = hours_worked
        self.hourly_rate = hourly_rate

    def calculate_pay(self):
        return self.hours_worked * self.hourly_rate

    def save_to_database(self):
        # Opens DB connection, writes employee, closes connection
        print(f"Saving {self.name} to DB...")

    def generate_report(self, format):
        if format == "pdf":
            print(f"Generating PDF for {self.name}...")
        elif format == "html":
            print(f"Generating HTML for {self.name}...")
```

This `Employee` class has **three stakeholders**:

1. **Finance** — they own "how we calculate pay."
2. **DBA / Infra team** — they own "how we persist data."
3. **Reporting team** — they own "how we present data."

When Finance changes pay rules, we touch `Employee`. When DB team migrates to a new database, we touch `Employee`. When reporting adds CSV format, we touch `Employee`. The class is a **hot file** — always being edited, always risky.

### Applying SRP

Split each responsibility into its own class:

```python
class Employee:
    def __init__(self, name, hours_worked, hourly_rate):
        self.name = name
        self.hours_worked = hours_worked
        self.hourly_rate = hourly_rate


class PayrollCalculator:
    def calculate_pay(self, employee):
        return employee.hours_worked * employee.hourly_rate


class EmployeeRepository:
    def save(self, employee):
        print(f"Saving {employee.name} to DB...")


class EmployeeReportGenerator:
    def generate(self, employee, format):
        if format == "pdf":
            print(f"PDF for {employee.name}")
        elif format == "html":
            print(f"HTML for {employee.name}")
```

Now:
- Finance changes pay rules → only `PayrollCalculator` changes.
- DBA migrates DB → only `EmployeeRepository` changes.
- Reporting team adds CSV → only `EmployeeReportGenerator` changes.
- **Each class has one reason to change.**

### Analogy

Think of a Swiss Army knife vs. a professional chef's kit.

A Swiss Army knife does many things poorly. When the knife blade dulls, the can opener also gets affected (you throw the whole thing out). A professional kit has separate knives for fish, vegetables, meat — each optimized and independently replaceable.

Classes that violate SRP are Swiss Army knives. Each responsibility drags the others into every change.

### A Common Misreading

SRP is **not** "a class should have only one method" or "classes must be tiny." A well-designed class can have many methods — as long as they all serve **one cohesive purpose**.

For example, a `ShoppingCart` class with `add_item`, `remove_item`, `update_quantity`, `total_price`, `clear` has many methods but one responsibility: managing cart state. That's fine.

### Signs You're Violating SRP

- The class name has "and" in it (`UserAndEmailSender`).
- Some methods never share state with other methods.
- Multiple teams keep editing the same class for unrelated reasons.
- The class has both business logic AND I/O (DB, network, file).
- Changing one method breaks tests for unrelated features.

### SRP Applies Beyond Classes

SRP is fractal. It applies to:
- **Methods** — one method, one job. Avoid 300-line monsters.
- **Modules/packages** — a module should serve one purpose.
- **Microservices** — a service should own one business capability.

Different scales, same principle.

---

## 4. Open/Closed Principle (OCP)

> **"Software entities (classes, modules, functions) should be open for extension, but closed for modification."**
> — Bertrand Meyer (1988), popularized by Martin

### What it really means

You should be able to **add new behavior** to a system **without modifying existing code**.

Why? Because modified code is risky code. Every time you open a working class and change it, you risk:
- Breaking existing functionality (regression bugs).
- Re-running and updating tests that used to pass.
- Triggering downstream changes in dependent code.

"Closed for modification" ≠ "you can never edit it." It means: once a class is working and tested, the *design* should let you extend it *without* reopening it.

### The Pain Without OCP

Imagine a discount calculator:

```python
class DiscountCalculator:
    def calculate(self, customer_type, amount):
        if customer_type == "regular":
            return amount * 0.05
        elif customer_type == "premium":
            return amount * 0.10
        elif customer_type == "vip":
            return amount * 0.20
        else:
            return 0
```

Today: a new customer type `corporate` is introduced with 15% discount. You open this file and add another `elif`.

Tomorrow: `student` customer type, 8% discount. Another `elif`.

A month later: seasonal discounts, regional discounts, first-time-buyer logic. The method becomes a 300-line beast of `elif`s. Every change risks breaking every other case. Every addition requires rewriting tests.

### Applying OCP

Use **polymorphism** to extend behavior without modifying existing code.

```python
from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, amount): pass

class RegularDiscount(DiscountStrategy):
    def calculate(self, amount): return amount * 0.05

class PremiumDiscount(DiscountStrategy):
    def calculate(self, amount): return amount * 0.10

class VIPDiscount(DiscountStrategy):
    def calculate(self, amount): return amount * 0.20


class DiscountCalculator:
    def calculate(self, strategy, amount):
        return strategy.calculate(amount)
```

Now, to add `CorporateDiscount`:

```python
class CorporateDiscount(DiscountStrategy):
    def calculate(self, amount): return amount * 0.15
```

**Zero changes to `DiscountCalculator` or existing strategies.** The system is *extended*, not *modified*.

### Analogy

Think of a smartphone. You want new capabilities — photo editing, step tracking, language learning? You install new apps. You don't take apart the phone's motherboard.

The phone is **closed for modification** (nobody's soldering new chips onto your iPhone) but **open for extension** (install an app).

OCP is the engineering equivalent: design systems with "app slots" (abstract interfaces) so new features plug in cleanly.

### How OCP Relates to OOP

OCP is polymorphism's best friend. Polymorphism is the mechanism that makes OCP possible. Without polymorphism, you'd have to check types explicitly (`if isinstance(x, Regular)`), which inherently modifies existing code every time a new type appears.

### A Subtler Point

OCP doesn't mean "never modify code." Bug fixes obviously require modification. And sometimes a design needs reworking. OCP means: the **common, expected axis of change** (like "new discount types") should be extensible without modification.

You can't make everything extensible — that would create infinite abstraction. The skill is identifying *which* axes are likely to change and protecting those.

### Signs You're Violating OCP

- Every new feature requires editing an existing `if`/`elif` chain or switch.
- Adding a type requires updating multiple files that check the type.
- You keep re-testing old code after every new feature.
- Code has comments like `# Remember to update here when adding X`.

---

## 5. Liskov Substitution Principle (LSP)

> **"If S is a subtype of T, then objects of type T in a program may be replaced with objects of type S without altering any desirable properties of the program."**
> — Barbara Liskov (1987)

### What it really means in plain English

**Any code that works with a parent class should still work correctly when given a child class — without knowing it got a child.**

If subclass `Sparrow` extends `Bird`, then anywhere you use a `Bird`, passing a `Sparrow` should Just Work. No surprises, no special cases.

LSP is the principle that ensures inheritance is **honest**. It separates "this subclass is really an X" from "this subclass vaguely resembles X but breaks when used like one."

### The Classic Violation — The Square/Rectangle Problem

"A square is a rectangle, right?" — mathematically, yes. Programmatically, watch what happens:

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set_width(self, w):
        self.width = w

    def set_height(self, h):
        self.height = h

    def area(self):
        return self.width * self.height


class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)

    def set_width(self, w):
        self.width = w
        self.height = w   # Keep it square

    def set_height(self, h):
        self.width = h
        self.height = h
```

Now consider code using `Rectangle`:

```python
def stretch_rectangle(rect: Rectangle):
    rect.set_width(10)
    rect.set_height(5)
    assert rect.area() == 50   # Expected for a rectangle
```

Pass a `Rectangle(1, 1)` → area = 50 ✓
Pass a `Square(1)` → area = **25**, assertion fails!

The `Square` silently broke the contract that `Rectangle` implied: "width and height are independent." Any code written against `Rectangle` now has a landmine if given a `Square`.

**LSP is violated.** Mathematics be damned — from a behavioral standpoint, `Square` is **not** substitutable for `Rectangle`.

The fix: don't inherit. `Rectangle` and `Square` are separate shapes with their own contracts. If they share anything, it's a common abstraction (`Shape`) that promises only what *both* can honor — `area()` — and says nothing about mutable, independent dimensions.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    # The shared contract is intentionally minimal: every shape can report its
    # area. We do NOT put set_width/set_height here, because that's exactly the
    # promise a Square cannot keep. An interface should only promise what every
    # implementer can truly deliver.
    @abstractmethod
    def area(self):
        ...

class Rectangle(Shape):
    # Rectangle owns the "two independent sides" contract. Nothing inherits it,
    # so no subclass can silently violate the independence of width and height.
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set_width(self, w):
        self.width = w

    def set_height(self, h):
        self.height = h

    def area(self):
        return self.width * self.height

class Square(Shape):
    # Square is a sibling, not a child, of Rectangle. It exposes a single
    # `side`, so there's no set_width/set_height to misimplement — the API
    # itself makes the illegal state (independent sides) unrepresentable.
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2
```

Now `stretch_rectangle` only ever accepts a `Rectangle`, and there's no `Square` that can be passed where a `Rectangle` is expected. We traded a tempting but false "is-a" for an honest type hierarchy.

### Another Classic — The Bird/Penguin Problem

```python
class Bird:
    def fly(self):
        print("Flying!")

class Sparrow(Bird):
    pass

class Penguin(Bird):
    def fly(self):
        raise NotImplementedError("Penguins can't fly!")
```

Code using `Bird`:

```python
def make_birds_fly(birds):
    for bird in birds:
        bird.fly()
```

Pass in a list with a `Penguin` → crash. LSP violated.

Fix: restructure the hierarchy so the contract makes sense.

```python
class Bird(ABC):
    @abstractmethod
    def move(self): pass

class FlyingBird(Bird):
    def move(self): print("Flying!")

class FlightlessBird(Bird):
    def move(self): print("Walking!")

class Sparrow(FlyingBird): pass
class Penguin(FlightlessBird): pass
```

Now substitution works. Any `Bird` can `move()`. No surprises.

### Rules Subclasses Must Follow (to respect LSP)

1. **Preconditions cannot be strengthened.** If parent accepts any integer, child cannot suddenly require only positive integers.
2. **Postconditions cannot be weakened.** If parent guarantees a sorted list, child cannot return an unsorted one.
3. **Invariants must be preserved.** If parent's balance is always ≥ 0, child cannot allow negative balances.
4. **History constraint.** A child shouldn't allow state transitions the parent forbids.

### Analogy

Imagine hiring a "driver." The job description says: *"Turn up at 9 AM, drive from A to B, no questions asked."*

You hire Driver A — works perfectly.
You hire Driver B who says: *"I only drive on Tuesdays and refuse highways."*

Driver B *calls themselves* a driver but **cannot be substituted** for a driver. If you build your schedule around "any driver can do this," Driver B will break it.

LSP says: don't hire Driver B as a Driver. If Driver B's contract is fundamentally different, they belong to a different role (e.g., "part-time city driver").

### Why LSP Matters

Violating LSP undermines the entire promise of polymorphism. If subtypes aren't truly substitutable, you can't safely write generic code — you always have to check "what kind of X do I really have?" This defeats the point of OCP too.

LSP is the invisible contract that makes polymorphism trustworthy.

### Signs You're Violating LSP

- A subclass throws `NotImplementedError` for a method the parent supports.
- A subclass overrides a method and returns a different type (or a much weaker guarantee).
- Users of a base class need `isinstance()` checks to handle subclasses differently.
- Overridden methods silently change the object's state in unexpected ways.

---

## 6. Interface Segregation Principle (ISP)

> **"Clients should not be forced to depend on interfaces they do not use."**
> — Robert C. Martin

### What it really means

**Don't lump unrelated methods into one big interface. Split large interfaces into smaller, focused ones so clients only know about what they actually use.**

### The Pain Without ISP

Suppose you build an office equipment interface:

```python
from abc import ABC, abstractmethod

class OfficeMachine(ABC):
    @abstractmethod
    def print(self, doc): pass

    @abstractmethod
    def scan(self, doc): pass

    @abstractmethod
    def fax(self, doc): pass
```

Now a multifunction printer:

```python
class AllInOnePrinter(OfficeMachine):
    def print(self, doc): print(f"Printing {doc}")
    def scan(self, doc): print(f"Scanning {doc}")
    def fax(self, doc): print(f"Faxing {doc}")
```

Fine. Now a simple printer:

```python
class BasicPrinter(OfficeMachine):
    def print(self, doc): print(f"Printing {doc}")
    def scan(self, doc): raise NotImplementedError("Can't scan!")
    def fax(self, doc): raise NotImplementedError("Can't fax!")
```

`BasicPrinter` is **forced to implement methods it has no business implementing**. This creates two problems:

1. **Wasted code** — stub methods that just throw exceptions.
2. **Lies in the type system** — `BasicPrinter` claims to be an `OfficeMachine`, but breaks if you treat it as one (LSP violation!).

Notice how ISP and LSP intertwine: a bloated interface often forces subtypes to lie, which violates LSP.

### Applying ISP

Split into focused interfaces:

```python
class Printer(ABC):
    @abstractmethod
    def print(self, doc): pass

class Scanner(ABC):
    @abstractmethod
    def scan(self, doc): pass

class Fax(ABC):
    @abstractmethod
    def fax(self, doc): pass


class BasicPrinter(Printer):
    def print(self, doc): print(f"Printing {doc}")


class AllInOnePrinter(Printer, Scanner, Fax):
    def print(self, doc): print(f"Printing {doc}")
    def scan(self, doc): print(f"Scanning {doc}")
    def fax(self, doc): print(f"Faxing {doc}")
```

Now:
- `BasicPrinter` only implements what it can.
- `AllInOnePrinter` composes multiple focused interfaces.
- Client code requiring only printing can depend on `Printer`, oblivious to scan/fax.

### Analogy

Imagine a restaurant that gives every customer the full 80-page menu including kids' meals, vegan options, cocktails, wedding catering, and corporate orders. Overwhelming, confusing, and slow.

Better: customers see **the menu relevant to them** — a drink menu for the bar, a kids' menu for families, an event menu for corporate clients.

ISP says: segregate interfaces by client, not by implementer convenience.

### ISP in Pythonic Terms

Python's duck typing softens this. Since you don't *have to* declare interfaces, you can just accept anything that has the method you need. But when you *do* define ABCs or Protocols, keep them narrow.

```python
from typing import Protocol

class Printable(Protocol):
    def print(self, doc): ...

def print_many(docs, printer: Printable):
    for doc in docs:
        printer.print(doc)
```

Any object with a `print` method satisfies `Printable`. Narrow, focused, composable.

### Signs You're Violating ISP

- Subclasses raise `NotImplementedError` for methods they don't need.
- Interfaces have many methods that rarely get used together.
- Client code imports a big interface but uses only 1–2 methods.
- Test doubles/mocks have to stub out many unused methods.

---

## 7. Dependency Inversion Principle (DIP)

> **"High-level modules should not depend on low-level modules. Both should depend on abstractions. Abstractions should not depend on details. Details should depend on abstractions."**
> — Robert C. Martin

### What it really means

**Depend on *interfaces*, not on *concrete implementations*.** That way, you can swap implementations without touching the code that uses them.

"High-level" = business logic (what the app does).
"Low-level" = mechanics (database, file system, network, etc.).

Naively, high-level depends on low-level: business logic *uses* the database. DIP says: **invert** that. Make both depend on an abstraction in the middle.

### The Pain Without DIP

```python
class MySQLDatabase:
    def save(self, data):
        print(f"Saving {data} to MySQL")


class UserService:
    def __init__(self):
        self.db = MySQLDatabase()   # Hardcoded dependency

    def register_user(self, name):
        self.db.save({"name": name})
```

Problems:

1. **Tight coupling.** `UserService` can only work with MySQL. Want to switch to PostgreSQL? Rewrite `UserService`.
2. **Untestable.** You can't test `UserService` without a real MySQL server running. Unit tests become integration tests.
3. **Rigid.** Want to log to a file for development? Send events to Kafka instead? Every variation requires code surgery inside `UserService`.

`UserService` — the "high-level" business logic — directly depends on `MySQLDatabase` — a "low-level" mechanism. Any change to how we store data forces `UserService` to change.

### Applying DIP

Introduce an abstraction:

```python
from abc import ABC, abstractmethod

class Database(ABC):    # The abstraction
    @abstractmethod
    def save(self, data): pass


class MySQLDatabase(Database):
    def save(self, data):
        print(f"Saving {data} to MySQL")


class PostgresDatabase(Database):
    def save(self, data):
        print(f"Saving {data} to Postgres")


class InMemoryDatabase(Database):    # Handy for tests!
    def __init__(self):
        self.data = []
    def save(self, data):
        self.data.append(data)


class UserService:
    def __init__(self, db: Database):   # Depends on the abstraction
        self.db = db

    def register_user(self, name):
        self.db.save({"name": name})
```

Now look what we can do:

```python
# Production
service = UserService(MySQLDatabase())

# Dev
service = UserService(PostgresDatabase())

# Tests
fake_db = InMemoryDatabase()
service = UserService(fake_db)
service.register_user("Amit")
assert fake_db.data == [{"name": "Amit"}]
```

`UserService` doesn't care what's behind the `Database` interface. Swapping implementations is a one-line change at the boundary (usually in a config or startup script), not a rewrite.

### Dependency Injection

The technique we just used — passing dependencies in through the constructor instead of creating them internally — is called **dependency injection** (DI).

DI is the primary *practical* way to achieve DIP. When dependencies come in from outside:
- You can substitute them (for tests, for environments).
- Your class's internals don't know or care which implementation is used.

Three common injection styles:
1. **Constructor injection** (most common) — pass dependencies in `__init__`.
2. **Setter/method injection** — pass dependencies via a setter or method parameter.
3. **Framework-based injection** — a framework wires dependencies automatically (e.g., FastAPI's `Depends`).

We've already seen constructor injection above. Here's **setter injection** — useful when the dependency is optional, or might be swapped *after* the object already exists:

```python
class UserService:
    def __init__(self):
        # Start with a sensible default so the object is usable immediately,
        # even if nobody injects a different db later.
        self.db: Database = InMemoryDatabase()

    def set_database(self, db: Database):
        # Inject (or re-inject) the dependency at any point in the object's
        # life. The tradeoff vs constructor injection: more flexible, but the
        # object can exist in a "not yet configured" state, so it's easier to
        # forget to wire it up. Prefer constructor injection unless you
        # specifically need to change the dependency after construction.
        self.db = db

service = UserService()
service.set_database(PostgresDatabase())   # Swap in a real db when ready
```

### Analogy

Think of laptop charging.

**Without DIP:** Your laptop's charging port is hardwired to only work with one specific brand of charger. Lose the charger? Buy another identical one. Travel abroad? Hope they sell your exact brand.

**With DIP:** USB-C. Your laptop depends on an *abstraction* — "any USB-C power source." You can plug into a wall adapter, a power bank, another laptop, an airplane seat, even a monitor that doubles as a charger.

The laptop (high-level) doesn't know or care what's on the other end. It only depends on the **interface** (USB-C spec). Suppliers of power (low-level) also depend on that interface. Both sides conform to the abstraction; neither side dictates the other.

### Why "Inversion"?

In the naive approach, the dependency arrow points *downward*:

```
UserService  →  MySQLDatabase
 (high)          (low)
```

After DIP, the arrow is *inverted* — both point *upward* to the abstraction:

```
UserService     MySQLDatabase
     ↓                ↑
     Database (abstraction)
```

This inversion is the key: the low-level detail now depends on (conforms to) the abstraction, not the other way around.

### Signs You're Violating DIP

- Your class constructs its dependencies internally (`self.db = MySQL()`).
- You can't unit-test a class without real databases, APIs, or files.
- Swapping an implementation requires changing many files.
- Business logic imports things like `import psycopg2` or `import requests` directly.

---

## 8. How the Five Principles Reinforce Each Other

SOLID isn't a checklist of five independent items. The principles **feed into each other**:

- **SRP** forces you to split classes by responsibility. This naturally leads to small, focused classes.
- Small, focused classes make it easier to define small, focused interfaces → **ISP**.
- Small interfaces are easier to respect with honest subclasses → **LSP**.
- When classes are honest and interfaces small, swapping implementations becomes safe → **DIP**.
- When you depend on abstractions, adding new features means adding new implementations (not modifying old ones) → **OCP**.

Think of them as a **reinforcing cycle**:

```
SRP → small classes → small interfaces (ISP) → honest subclasses (LSP)
                                                       ↓
                                           safe polymorphism
                                                       ↓
                                   abstractions trusted (DIP)
                                                       ↓
                                     extension over modification (OCP)
                                                       ↓
                              system stays maintainable → easier SRP next time
```

Conversely, violating one often cascades into violating others. A god class (SRP violation) usually has a bloated interface (ISP violation) that subclasses can't honestly implement (LSP violation), which makes it unsafe to depend on (DIP violation), which forces `if/elif` chains everywhere (OCP violation).

---

## 9. Capstone Example

Let's build a **notification system** applying all five principles, starting from a messy version and refactoring step by step.

### Messy Version (violates everything)

```python
class NotificationService:
    def send(self, user, message, channel):
        if channel == "email":
            # Hardcoded SMTP stuff
            print(f"Connecting to smtp.example.com...")
            print(f"Email to {user.email}: {message}")
        elif channel == "sms":
            # Hardcoded Twilio stuff
            print(f"Calling Twilio API...")
            print(f"SMS to {user.phone}: {message}")
        elif channel == "push":
            print(f"Push to {user.device_id}: {message}")

        # Also log to database
        print(f"Logging notification to MySQL...")

        # Also update user's last_notified_at
        user.last_notified_at = "now"
```

What's wrong:
- **SRP:** mixes sending, logging, and user updates.
- **OCP:** adding Slack/Telegram requires modifying this class.
- **LSP:** N/A directly, but the monolith makes substitution impossible.
- **ISP:** not applicable yet — no interfaces defined.
- **DIP:** hardcoded SMTP, Twilio, MySQL. Can't test without real services.

### Refactored Version

Step 1 — Extract interfaces (ISP: each interface narrow).

```python
from abc import ABC, abstractmethod

class NotificationChannel(ABC):
    # ISP in action: this interface promises exactly ONE thing — send(). A
    # channel never has to know about logging, formatting, or anything else.
    # Narrow interfaces mean implementers depend on nothing they don't use.
    @abstractmethod
    def send(self, recipient, message): pass

class NotificationLogger(ABC):
    # A SECOND narrow interface rather than bolting log() onto the channel.
    # Keeping send and log apart is both ISP (small interfaces) and SRP
    # (sending and recording are different responsibilities).
    @abstractmethod
    def log(self, recipient, message, channel_name): pass
```

Step 2 — Implement each channel independently (OCP: add new channels without modifying others).

```python
# OCP in action: each channel is a self-contained extension point. The set of
# channels is OPEN to extension (add a new class) but the existing classes are
# CLOSED to modification — adding SMS never forces an edit to Email.
class EmailChannel(NotificationChannel):
    def send(self, recipient, message):
        print(f"Email to {recipient.email}: {message}")

class SMSChannel(NotificationChannel):
    def send(self, recipient, message):
        print(f"SMS to {recipient.phone}: {message}")

class PushChannel(NotificationChannel):
    def send(self, recipient, message):
        print(f"Push to {recipient.device_id}: {message}")
```

Adding `SlackChannel` or `TelegramChannel` tomorrow? Just create a new class — no existing code is touched.

Step 3 — Implement logger separately (SRP: logging is its own responsibility).

```python
class DatabaseLogger(NotificationLogger):
    def log(self, recipient, message, channel_name):
        print(f"DB log: {channel_name} to {recipient}: {message}")

class InMemoryLogger(NotificationLogger):    # For tests
    def __init__(self):
        self.entries = []
    def log(self, recipient, message, channel_name):
        self.entries.append((recipient, message, channel_name))
```

Step 4 — The orchestrator (DIP: depends on abstractions, not concretions).

```python
class NotificationService:
    def __init__(self, channel: NotificationChannel, logger: NotificationLogger):
        # DIP in action: the type hints point at ABSTRACTIONS, not concrete
        # classes. This high-level orchestrator has zero knowledge of Email vs
        # SMS, DatabaseLogger vs InMemoryLogger. The concrete choice is injected
        # from outside (constructor injection), so swapping implementations is a
        # call-site change, never an edit to this class.
        self.channel = channel
        self.logger = logger

    def notify(self, recipient, message):
        # notify() reads as pure coordination: send, then log. Because both
        # collaborators satisfy their contracts (LSP), this body never changes
        # regardless of which concrete channel/logger is passed in.
        self.channel.send(recipient, message)
        self.logger.log(recipient, message, self.channel.__class__.__name__)
```

Step 5 — Verify LSP: can we swap any `NotificationChannel` for another? Yes — all honor the same contract (`send(recipient, message)`).

### Using It

```python
# Production
email_service = NotificationService(EmailChannel(), DatabaseLogger())
email_service.notify(user, "Your order has shipped")

# Tests
test_logger = InMemoryLogger()
test_service = NotificationService(EmailChannel(), test_logger)
test_service.notify(fake_user, "hello")
assert len(test_logger.entries) == 1
```

### Observations

- Each class has **one reason to change** (SRP).
- We can add new channels/loggers **without modifying** existing code (OCP).
- Any channel is **substitutable** for another (LSP).
- Interfaces are **narrow** — `NotificationChannel` only has `send`, `Logger` only has `log` (ISP).
- `NotificationService` depends on **abstractions** (DIP).

The design is flexible, testable, and additive.

---

## 10. Common Pitfalls

### Over-engineering

"Applying SOLID" can become an excuse to create layers of unnecessary abstraction. If your app has exactly one kind of discount and will never have more, `DiscountCalculator` with 4 classes and an ABC is overkill.

**Rule:** apply SOLID when the axis of change *actually exists* or *is reasonably anticipated*. Not speculatively.

### Confusing "small class" with SRP

"I'll split this class in two" doesn't automatically obey SRP. Ask: *do these two classes have different reasons to change?* If both still change together for the same reasons, you've just scattered one responsibility across two files — worse than before.

### Interface explosion from ISP

Over-applying ISP leads to hundreds of two-method interfaces, each used in one place. That's noise, not design. Segregate when there are **genuinely different clients** with different needs.

### Forcing inheritance to enable polymorphism

LSP violations often come from forcing inheritance where it doesn't fit ("well, a Square *is* a Rectangle…"). When "is-a" doesn't hold behaviorally, use composition or separate hierarchies.

### DIP taken too far

Not every little thing needs an interface. `datetime.now()`? Probably fine to call directly. A remote API that may change, or a DB that you test without? Absolutely inject.

**Rule of thumb:** abstract the *boundaries* (I/O, third-party services, volatile dependencies). Keep pure business logic concrete.

### Dogma vs judgment

SOLID is a *heuristic*, not a law. A tiny script, a throwaway prototype, or a config parser doesn't need five abstractions. Use SOLID when the **lifetime and complexity** of the code justify the overhead.

---

## 11. When NOT to Apply SOLID

- **Prototypes and spikes.** You're exploring — don't prematurely abstract.
- **Small scripts.** A 50-line automation? Just write it.
- **Performance-critical tight loops.** Virtual calls and abstractions can add overhead where every nanosecond counts.
- **Stable, never-changing domains.** If math constants never change, don't design for extension.
- **When abstraction hides more than it reveals.** If the abstraction makes the code harder to read for the maintainer, it's worse, not better.

The art is **judgment**: apply SOLID where change is likely; skip it where it would add friction without benefit.

---

## 12. Summary

**Mental map to carry forward:**

| Principle | Core Idea | Main Benefit |
|---|---|---|
| **SRP** | One reason to change per class | Localized changes; less ripple |
| **OCP** | Extend, don't modify | Add features without breaking existing ones |
| **LSP** | Subclasses honor parent contracts | Reliable polymorphism |
| **ISP** | Small, focused interfaces | No forced implementations; cleaner contracts |
| **DIP** | Depend on abstractions | Swappable implementations; testable code |

### Key Takeaways

1. **SOLID is how OOP scales.** OOP gives you classes; SOLID tells you how to arrange them for maintainability.
2. **Change is the enemy.** Every principle is really about **minimizing the blast radius of change**.
3. **The principles reinforce each other.** Violations tend to cluster; good application of one helps the others.
4. **Abstractions enable extension.** Nearly every SOLID principle boils down to: *depend on the right abstraction, at the right level*.
5. **Judgment beats dogma.** SOLID is a toolkit, not a religion. Apply thoughtfully based on the change patterns your system actually faces.
6. **SOLID is the runway to design patterns.** Almost every GoF pattern is a concrete application of one or more SOLID principles (Strategy = OCP + DIP, Adapter = LSP + DIP, etc.).

---

## 13. Self-Assessment Test

*Answer each question in a sentence or two before revealing the answer. This tests conceptual understanding, not recall.*

<details>

**Q1.** A class has 15 methods, all working with the same underlying state and serving one cohesive purpose. Does it violate SRP?

<br>

**Answer:** No. SRP is about reasons to change, not method count. If all methods serve one responsibility (and change for the same reason), the class respects SRP. A `ShoppingCart` with 15 methods for managing cart state is fine.

---

**Q2.** You have an `Animal` class with a method `fly()`. You're adding `Penguin`. What's the correct SOLID response?

<br>

**Answer:** Restructure the hierarchy. Don't override `fly()` in `Penguin` to throw an exception (LSP violation). Instead, split into e.g. `FlyingAnimal` and `FlightlessAnimal`, or move `fly()` out of `Animal` entirely. The base class's contract should only promise things *all* subclasses can deliver.

---

**Q3.** You add a new payment type. You have to modify a central `if/elif` chain in `PaymentProcessor`. Which SOLID principle is this violating?

<br>

**Answer:** Primarily **OCP** — you're modifying existing code to extend behavior. Often also **DIP** — you're depending on concrete types rather than an abstraction. Fix: introduce a `PaymentStrategy` interface with one class per payment type, and let `PaymentProcessor` depend on the interface.

---

**Q4.** A `Printable` interface has `print()`, `scan()`, and `fax()`. Your `BasicPrinter` only prints, and throws `NotImplementedError` on the others. Which principle is this violating? What other principle is it also violating indirectly?

<br>

**Answer:** Directly violates **ISP** (forced to implement methods it doesn't use). Indirectly violates **LSP** (any code using `Printable` polymorphically will crash when given a `BasicPrinter`). Fix: split into `Printer`, `Scanner`, `Fax` — each class implements only what it supports.

---

**Q5.** A class `OrderService` creates a `PostgresDatabase` instance directly in its constructor. Your tests have to run against a real Postgres server. What's the violation and the fix?

<br>

**Answer:** Violates **DIP** — high-level `OrderService` depends directly on low-level `PostgresDatabase`. Fix: extract a `Database` abstraction, have `OrderService` receive it via constructor injection, and provide an in-memory or mock implementation for tests.

---

**Q6.** True or False: If a class has only one method, it automatically respects SRP.

<br>

**Answer:** False. SRP is about reasons to change, not size. A one-method class with 500 lines of tangled logic doing unrelated things still violates SRP. Conversely, a 20-method class can respect SRP if all methods serve one cohesive purpose.

---

**Q7.** Your `Duck` class has a `quack()` method. You subclass `RubberDuck(Duck)` that overrides `quack()` to play a squeaky sound instead of a real quack. Does this violate LSP?

<br>

**Answer:** Generally **no**, as long as the contract is "produce some kind of duck sound." Both real and rubber ducks satisfy that. LSP would only be violated if `quack()` had stronger guarantees the subclass breaks — e.g., "returns a real audio file" when `RubberDuck` returns nothing. LSP is about honoring contracts, not sameness of implementation.

---

**Q8.** Can a design follow SRP but still violate OCP? Give a brief example.

<br>

**Answer:** Yes. A `DiscountCalculator` class with a single responsibility (calculating discounts) can still use a giant `if/elif` chain that forces modification whenever a new discount type appears. SRP addresses class boundaries; OCP addresses extension mechanisms. They're related but distinct.

---

**Q9.** What's the relationship between Dependency Injection and the Dependency Inversion Principle?

<br>

**Answer:** DIP is the *principle* — depend on abstractions. Dependency Injection is the *most common technique* to achieve DIP in practice — pass dependencies in from outside (via constructor, setter, or framework) instead of instantiating them internally. DIP is the "what"; DI is the "how."

---

**Q10.** You're writing a 100-line data-munging script that reads a CSV and produces a summary. Should you carefully apply all five SOLID principles?

<br>

**Answer:** Probably not. SOLID's overhead is justified when code is long-lived and change is expected. For throwaway scripts and prototypes, applying SOLID can over-engineer the solution. Use judgment: abstract where change is likely; stay concrete where it isn't.

</details>

---

## 14. Practice Exercises

### Exercise 1 — SRP Refactor

The following class violates SRP. Identify the responsibilities, split the class, and explain your reasoning.

```python
class Invoice:
    def __init__(self, items):
        self.items = items  # list of (name, price, qty)

    def calculate_total(self):
        return sum(price * qty for _, price, qty in self.items)

    def calculate_tax(self):
        return self.calculate_total() * 0.18

    def save_to_pdf(self, filepath):
        print(f"Writing PDF to {filepath}")

    def send_by_email(self, to):
        print(f"Sending invoice to {to}")
```

**Solution:**

Responsibilities identified:
1. **Data / state** — what's on the invoice (items).
2. **Money calculations** — totals, taxes (Finance domain).
3. **PDF rendering** — output formatting (Presentation domain).
4. **Email delivery** — communication (Infrastructure domain).

Refactored:

```python
class Invoice:
    def __init__(self, items):
        self.items = items


class InvoiceCalculator:
    TAX_RATE = 0.18

    def total(self, invoice):
        return sum(price * qty for _, price, qty in invoice.items)

    def tax(self, invoice):
        return self.total(invoice) * self.TAX_RATE


class InvoicePDFRenderer:
    def render(self, invoice, filepath):
        print(f"Writing PDF of {len(invoice.items)} items to {filepath}")


class InvoiceEmailSender:
    def send(self, invoice, to):
        print(f"Sending invoice with {len(invoice.items)} items to {to}")
```

Each class can now change independently: tax rate update only touches `InvoiceCalculator`; PDF layout change only touches `InvoicePDFRenderer`; SMTP migration only touches `InvoiceEmailSender`.

---

### Exercise 2 — OCP Application

You have:

```python
class AreaCalculator:
    def compute(self, shapes):
        total = 0
        for shape in shapes:
            if shape["type"] == "circle":
                total += 3.14 * shape["radius"] ** 2
            elif shape["type"] == "square":
                total += shape["side"] ** 2
            elif shape["type"] == "rectangle":
                total += shape["width"] * shape["height"]
        return total
```

Adding any new shape requires modifying `AreaCalculator`. Refactor to respect OCP.

**Solution:**

```python
from abc import ABC, abstractmethod
import math

class Shape(ABC):
    @abstractmethod
    def area(self): pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return math.pi * self.radius ** 2

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def area(self):
        return self.width * self.height


class AreaCalculator:
    def compute(self, shapes):
        return sum(shape.area() for shape in shapes)
```

Adding `Triangle` now requires **zero changes** to `AreaCalculator` — just create a new `Triangle(Shape)` class.

---

### Exercise 3 — LSP Check

Examine this code. Does it violate LSP? Why or why not?

```python
class FileReader:
    def read(self, path):
        with open(path) as f:
            return f.read()

class LoggingFileReader(FileReader):
    def read(self, path):
        print(f"Reading {path}")
        return super().read(path)
```

vs.

```python
class StrictFileReader(FileReader):
    def read(self, path):
        if not path.endswith(".txt"):
            raise ValueError("Only .txt supported!")
        return super().read(path)
```

**Solution:**

- **`LoggingFileReader`** — **does NOT** violate LSP. It adds a side effect (logging) but still returns the full file contents for any valid path, honoring the parent's contract.

- **`StrictFileReader`** — **violates LSP**. It strengthens preconditions (only `.txt` files allowed). Code written for `FileReader` that passes a `.json` file would work with the parent but crash with the child. Substitutability is broken.

Key lesson: subclasses may *extend* behavior but should not *restrict* what the parent accepts.

---

### Exercise 4 — ISP Design

Design interfaces for a workshop where:
- A `Carpenter` only needs to `cut_wood`.
- A `Plumber` only needs to `fix_pipe`.
- A `Handyman` can do both.

Avoid forcing either specialist to implement the other's skill.

**Solution:**

```python
from abc import ABC, abstractmethod

class WoodWorker(ABC):
    @abstractmethod
    def cut_wood(self): pass

class PipeWorker(ABC):
    @abstractmethod
    def fix_pipe(self): pass


class Carpenter(WoodWorker):
    def cut_wood(self): print("Cutting wood")

class Plumber(PipeWorker):
    def fix_pipe(self): print("Fixing pipe")

class Handyman(WoodWorker, PipeWorker):
    def cut_wood(self): print("Cutting wood")
    def fix_pipe(self): print("Fixing pipe")
```

Note how **multiple inheritance** of narrow interfaces cleanly captures "handyman has both skills" without bloating a single mega-interface.

---

### Exercise 5 — DIP via Injection

The following code is hard to test because `EmailService` depends on a hardcoded SMTP client. Refactor it to respect DIP.

```python
class SmtpClient:
    def send(self, to, subject, body):
        print(f"SMTP → {to}: {subject}")


class EmailService:
    def __init__(self):
        self.client = SmtpClient()

    def send_welcome(self, user):
        self.client.send(user.email, "Welcome!", f"Hi {user.name}")
```

**Solution:**

```python
from abc import ABC, abstractmethod

class EmailClient(ABC):
    @abstractmethod
    def send(self, to, subject, body): pass


class SmtpClient(EmailClient):
    def send(self, to, subject, body):
        print(f"SMTP → {to}: {subject}")


class FakeEmailClient(EmailClient):    # For tests
    def __init__(self):
        self.sent = []
    def send(self, to, subject, body):
        self.sent.append((to, subject, body))


class EmailService:
    def __init__(self, client: EmailClient):
        self.client = client

    def send_welcome(self, user):
        self.client.send(user.email, "Welcome!", f"Hi {user.name}")


# Usage
prod_service = EmailService(SmtpClient())

# Testing
fake = FakeEmailClient()
test_service = EmailService(fake)
test_service.send_welcome(SomeUser)
assert len(fake.sent) == 1
```

`EmailService` now depends on the abstraction `EmailClient`. Implementations are injected. Testing no longer requires real SMTP.

---

### Exercise 6 — Full SOLID Refactor (Capstone)

Here is a "god class" that violates every SOLID principle. Refactor it completely.

```python
class OrderManager:
    def __init__(self):
        self.orders = []

    def place_order(self, customer_type, items, payment_method):
        # Calculate total
        total = sum(price * qty for _, price, qty in items)

        # Apply discount
        if customer_type == "regular":
            total *= 0.95
        elif customer_type == "premium":
            total *= 0.90
        elif customer_type == "vip":
            total *= 0.80

        # Process payment
        if payment_method == "card":
            print(f"Charging ₹{total} on card")
        elif payment_method == "upi":
            print(f"Processing ₹{total} via UPI")
        elif payment_method == "cash":
            print(f"Collecting ₹{total} cash on delivery")

        # Save to MySQL
        print(f"Saving order to MySQL...")

        # Send email
        print(f"Sending confirmation email...")

        self.orders.append({"items": items, "total": total})
        return total
```

**Solution:**

```python
from abc import ABC, abstractmethod

# --- Discount strategies (OCP, DIP) ---
class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, amount): pass

class RegularDiscount(DiscountStrategy):
    def apply(self, amount): return amount * 0.95

class PremiumDiscount(DiscountStrategy):
    def apply(self, amount): return amount * 0.90

class VIPDiscount(DiscountStrategy):
    def apply(self, amount): return amount * 0.80


# --- Payment processors (OCP, DIP) ---
class PaymentProcessor(ABC):
    @abstractmethod
    def charge(self, amount): pass

class CardProcessor(PaymentProcessor):
    def charge(self, amount): print(f"Card: ₹{amount}")

class UPIProcessor(PaymentProcessor):
    def charge(self, amount): print(f"UPI: ₹{amount}")

class CashProcessor(PaymentProcessor):
    def charge(self, amount): print(f"Cash on delivery: ₹{amount}")


# --- Repository (SRP, DIP) ---
class OrderRepository(ABC):
    @abstractmethod
    def save(self, order): pass

class MySQLOrderRepository(OrderRepository):
    def save(self, order): print(f"MySQL: saved order {order}")

class InMemoryOrderRepository(OrderRepository):
    def __init__(self): self.orders = []
    def save(self, order): self.orders.append(order)


# --- Notification (SRP, DIP) ---
class OrderNotifier(ABC):
    @abstractmethod
    def notify(self, order): pass

class EmailOrderNotifier(OrderNotifier):
    def notify(self, order): print(f"Email: order {order} confirmed")


# --- Pricing (SRP) ---
class PriceCalculator:
    def total(self, items):
        return sum(price * qty for _, price, qty in items)


# --- Orchestrator (SRP — coordinates, doesn't do everything) ---
class OrderService:
    def __init__(self,
                 calculator: PriceCalculator,
                 discount: DiscountStrategy,
                 payment: PaymentProcessor,
                 repository: OrderRepository,
                 notifier: OrderNotifier):
        self.calculator = calculator
        self.discount = discount
        self.payment = payment
        self.repository = repository
        self.notifier = notifier

    def place_order(self, items):
        total = self.calculator.total(items)
        total = self.discount.apply(total)
        self.payment.charge(total)
        order = {"items": items, "total": total}
        self.repository.save(order)
        self.notifier.notify(order)
        return total
```

### Usage

```python
service = OrderService(
    calculator=PriceCalculator(),
    discount=PremiumDiscount(),
    payment=UPIProcessor(),
    repository=MySQLOrderRepository(),
    notifier=EmailOrderNotifier(),
)
service.place_order([("book", 300, 2), ("pen", 50, 5)])
```

### Principle-by-principle check

- **SRP:** each class has one reason to change. `PriceCalculator`, `DiscountStrategy`, `PaymentProcessor`, `OrderRepository`, `OrderNotifier`, `OrderService` all own distinct responsibilities.
- **OCP:** new discount types, payment methods, repositories, or notifiers = new classes. `OrderService` is unchanged.
- **LSP:** any `DiscountStrategy`, `PaymentProcessor`, etc., is substitutable within `OrderService`. Contracts are honored.
- **ISP:** each interface is narrow — `apply`, `charge`, `save`, `notify`. No class is forced to implement irrelevant methods.
- **DIP:** `OrderService` depends entirely on abstractions. Production and test configurations differ only in which implementations are injected.

---

**You now understand SOLID as a system, not five isolated rules.** With OOP (*raw materials*) and SOLID (*arrangement rules*), you're ready for the final layer: **common design patterns** — pre-solved recipes for recurring design problems, each one essentially a distilled application of SOLID principles.

---

*This content is part of **Codeverra** — a platform for learning coding, data science, DSA, and AI from scratch. Explore more: https://codeverra.com*
