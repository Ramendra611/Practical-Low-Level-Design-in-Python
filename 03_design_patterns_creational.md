# Design Patterns — Part 1: Introduction & Creational Patterns

> **Who this is for:** Anyone comfortable with Python OOP and SOLID principles who now wants to recognize and apply the 23 classical design patterns — the shared vocabulary of experienced software designers.

---

## Table of Contents

1. [What Are Design Patterns, Really?](#1-what-are-design-patterns)
2. [Why Learn Patterns?](#2-why-learn-patterns)
3. [The GoF Classification](#3-the-gof-classification)
4. [How to Read the Pattern Chapters](#4-how-to-read-the-pattern-chapters)
5. [Creational Patterns — Overview](#5-creational-patterns-overview)
6. [Singleton](#6-singleton)
7. [Factory Method](#7-factory-method)
8. [Abstract Factory](#8-abstract-factory)
9. [Builder](#9-builder)
10. [Prototype](#10-prototype)
11. [Summary of Creational Patterns](#11-summary-of-creational-patterns)
12. [Practice Exercises with Solutions](#12-practice-exercises)
13. [Self-Assessment Test](#13-self-assessment-test)

---

## 1. What Are Design Patterns?

Imagine you're a new chef in a busy restaurant. Every night, you re-invent how to slice onions, how to simmer sauces, how to plate pasta. You *could* do this — you're smart. But every great chef you've ever met uses a repertoire of **standard techniques** that were perfected by thousands of cooks before them. The techniques have names: *julienne*, *reduction*, *deglazing*. When a head chef says "julienne those carrots," every trained cook knows exactly what to do.

Design patterns are **julienne for software**. They're named, repeatedly-discovered solutions to recurring design problems. They let a designer say "let's use a Strategy here" and a teammate instantly understands the structure, the tradeoffs, and why.

### A More Formal Definition

> "Each pattern describes a problem which occurs over and over again in our environment, and then describes the core of the solution to that problem, in such a way that you can use this solution a million times over, without ever doing it the same way twice."
> — Christopher Alexander (architect, whose ideas inspired software patterns)

Three things to notice:

1. **Pattern ≠ code.** A pattern is a *shape*, a *structure*. You implement it differently each time based on context.
2. **Pattern ≠ library.** You don't `pip install singleton`. You recognize when a situation calls for a pattern and build it into your code.
3. **Pattern = named solution to a named problem.** You can only use a pattern if you can clearly state the problem first.

### The Story of the GoF

In 1994, four authors — **Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides** — published *Design Patterns: Elements of Reusable Object-Oriented Software*. They documented **23 patterns** they'd seen repeatedly in well-designed systems. The authors became known as the **"Gang of Four" (GoF)**, and these 23 are now called the **classical GoF patterns**.

These aren't the only patterns out there — there are dozens more (Repository, MVC, Pub/Sub, etc.) — but the GoF 23 form the universal baseline. Knowing them is table stakes for serious software design.

---

## 2. Why Learn Patterns?

### 1. Shared Vocabulary

Software teams communicate in patterns. Saying *"let's use the Observer pattern here"* in 30 seconds conveys what might take 10 minutes to explain from scratch. Patterns are to code what "city," "highway," "bridge" are to urban planning.

### 2. Proven Solutions

These structures have been battle-tested across decades and across industries. When you use a known pattern, you inherit that experience rather than reinventing (and re-failing).

### 3. Fluency with SOLID

Almost every GoF pattern is essentially a **concrete application of SOLID principles**. Observer obeys OCP (add observers without changing the subject). Strategy embodies DIP (depend on an abstract strategy). Learning patterns makes SOLID go from abstract rules to instinct.

### 4. Reading Other People's Code

A huge fraction of real-world frameworks (Django, SQLAlchemy, Flask, pytest) use these patterns extensively. Recognizing them is like knowing grammar — suddenly you understand unfamiliar codebases much faster.

### A Note of Caution

Patterns are tools, not trophies. Overusing patterns ("pattern fever") is as bad as ignoring them. The experienced designer asks *"what's the simplest structure that solves this?"* first, and only reaches for a pattern when it genuinely clarifies the design.

A famous quote:

> "Design patterns are there to be used *when they help*. Using one 'because you can' is the mark of an amateur."

Keep this in mind as we walk through each one.

---

## 3. The GoF Classification

The 23 patterns are grouped into three families by what they primarily deal with:

| Family | Focus | Patterns (count) |
|---|---|---|
| **Creational** | How objects are *created* | 5 |
| **Structural** | How objects are *composed* into larger structures | 7 |
| **Behavioral** | How objects *communicate* and distribute responsibility | 11 |

We'll cover them in three parts:

- **Part 1 (this document):** Creational — Singleton, Factory Method, Abstract Factory, Builder, Prototype.
- **Part 2:** Structural — Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy.
- **Part 3:** Behavioral — Chain of Responsibility, Command, Interpreter, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor.

---

## 4. How to Read the Pattern Chapters

For each pattern, you'll see the same structure:

1. **The Pain** — what problem does this pattern solve? (No pattern makes sense without a problem.)
2. **The Intent** — the pattern's one-line mission.
3. **The Analogy** — a real-world parallel.
4. **The Structure** — the roles involved.
5. **Python Implementation** — code that you can run.
6. **A Realistic Use Case** — where you'd actually use this.
7. **Tradeoffs** — when the pattern helps and when it hurts.
8. **Related Patterns** — neighbors in the design space.
9. **Python-Specific Notes** — when Python's features make the pattern simpler, unnecessary, or different.

Now let's dive in.

---

## 5. Creational Patterns — Overview

**The core question all creational patterns answer:** *how do we create objects in a way that stays flexible as requirements evolve?*

In naive code, we create objects by direct `ClassName(args)` calls scattered throughout the codebase. This seems simple — and is, for tiny projects. But it tightly couples the caller to the exact class being instantiated. Any change to construction logic (a new required argument, a new subclass, a configuration-driven choice) forces edits everywhere.

Creational patterns give us **knobs to turn** on object creation:

- **Singleton** — controls *how many* instances can exist (exactly one).
- **Factory Method** — lets subclasses decide *which concrete class* to create.
- **Abstract Factory** — creates *families* of related objects together.
- **Builder** — breaks complex construction into *step-by-step* assembly.
- **Prototype** — creates new objects by *cloning* existing ones.

Each one tackles a different creation pain. Let's meet them.

---

## 6. Singleton

### The Pain

Some things genuinely should exist **only once** in an application:

- A **configuration registry** that reads `config.yaml` once and serves everywhere.
- A **logger** that funnels all output to the same log file (so lines don't interleave bizarrely).
- A **connection pool** that manages a fixed set of DB connections — two pools fighting for the same DB is a disaster.

Without deliberate control, anyone can do `Logger()` ten times, creating ten separate loggers, and you end up with a logging mess. You need a guarantee: *no matter how many times the code asks for a Logger, it gets the same one.*

### Intent

> Ensure a class has only one instance, and provide a global point of access to it.

### Analogy

Think of a **country's president at any given moment**. There's exactly one. Anyone asking "who's the current president?" gets the same answer. If two people claimed the office simultaneously, chaos.

Or: the **main power switch** in a house. There's one master switch. Everything else routes through it. You don't have two main switches fighting for control.

### Python Implementation — Classic Approach

```python
class Logger:
    _instance = None   # Class-level slot holding the one-and-only instance

    def __new__(cls, *args, **kwargs):
        # We override __new__ (not __init__) because __new__ is the method that
        # actually ALLOCATES and returns the object. __init__ only *initializes*
        # an object that already exists — by the time __init__ runs, a fresh
        # object has already been created. To prevent a second object from ever
        # being made, we must intercept at the creation step itself.
        if cls._instance is None:
            cls._instance = super().__new__(cls)  # First call: build it once
            cls._instance.log_file = "app.log"
        # Every later Logger() call finds _instance already set and returns the
        # SAME object — so __new__ short-circuits the allocation entirely.
        return cls._instance

    def log(self, message):
        print(f"[{self.log_file}] {message}")


a = Logger()
b = Logger()
print(a is b)   # True — same object
a.log("Hello")  # [app.log] Hello
```

`__new__` is Python's actual object-creation hook (called before `__init__`). By intercepting it, we ensure that asking for a new `Logger` returns the existing one if it exists. A subtle gotcha: because `__init__` still runs on *every* `Logger()` call (Python calls it on whatever `__new__` returns), any initialization logic placed in `__init__` would re-run and could clobber state. That's why we set `log_file` inside the `if` block in `__new__` — it runs exactly once.

### Python Implementation — Decorator Approach

Cleaner and reusable:

```python
def singleton(cls):
    # `instances` lives in the enclosing function's scope. Because get_instance
    # references it, Python keeps it alive as a CLOSURE variable for the life of
    # the decorated class — it becomes a private, per-class cache that outside
    # code can't touch. One dict can serve multiple decorated classes (keyed by
    # the class object), which is why this decorator is reusable.
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            # First call for this class: actually construct and remember it.
            instances[cls] = cls(*args, **kwargs)
        # Subsequent calls hit the cache and return the stored instance, so the
        # name `Logger` now refers to get_instance, and Logger() yields one obj.
        return instances[cls]
    return get_instance


@singleton
class Logger:
    def __init__(self):
        self.log_file = "app.log"
    def log(self, msg):
        print(f"[{self.log_file}] {msg}")


a = Logger()
b = Logger()
print(a is b)   # True
```

### Python Implementation — Module-Level (Most Pythonic)

In Python, **modules themselves are singletons**. Importing a module twice still gives you the same object. This is often the simplest solution:

```python
# logger.py
log_file = "app.log"
def log(msg):
    print(f"[{log_file}] {msg}")
```

```python
# anywhere else
import logger
logger.log("Hello")
```

No decorator, no `__new__` trickery. Just a module. This is idiomatic Python and usually preferable unless you genuinely need a class with methods and mutable state.

### Realistic Use Case

A **database connection pool**:

```python
@singleton
class ConnectionPool:
    def __init__(self):
        self.connections = [f"conn-{i}" for i in range(10)]

    def acquire(self):
        return self.connections.pop()

    def release(self, conn):
        self.connections.append(conn)
```

Every service that needs a DB connection gets the same pool. No two separate pools fighting for the DB.

### Tradeoffs

**Pros:**
- Controlled, single point of access.
- Lazy initialization (created only when first needed).
- Guaranteed consistency — all callers see the same state.

**Cons:**
- **Global state** — notoriously hard to test. Tests may bleed state into each other.
- **Hidden dependencies** — classes using Singleton don't declare their dependency in the constructor, violating DIP.
- **Concurrency traps** — naive Singletons are not thread-safe (two threads may create two instances at once).
- **Overused.** Many "Singletons" in real code could have been simple module-level objects or dependency-injected shared instances.

### Related Patterns

- **Monostate** (Borg pattern) — achieves Singleton-like behavior by making *all instances share state* instead of forcing a single instance. Useful when inheritance is involved.
- **Dependency Injection** — often a better alternative. Instead of `Logger()` anywhere, pass the logger into classes that need it.

### Python-Specific Notes

Python's module-level singletons (and `functools.lru_cache` for one-time construction) often make explicit Singleton patterns unnecessary. Reach for the pattern only when you need a class, need to control instantiation carefully, and can't use DI.

---

## 7. Factory Method

### The Pain

You're writing a notification system. You have this:

```python
class EmailNotifier:
    def send(self, msg): ...

class SMSNotifier:
    def send(self, msg): ...

class PushNotifier:
    def send(self, msg): ...


def notify_user(user, msg):
    if user.prefers == "email":
        notifier = EmailNotifier()
    elif user.prefers == "sms":
        notifier = SMSNotifier()
    elif user.prefers == "push":
        notifier = PushNotifier()
    notifier.send(msg)
```

The `if/elif` chain that picks *which class* to instantiate is scattered everywhere you need a notifier. Add a `SlackNotifier`? Every such chain needs updating. OCP is crying.

### Intent

> Define an interface for creating an object, but let subclasses (or a single method) decide which concrete class to instantiate.

The *what* (needing a notifier) is separated from the *which* (choosing the concrete type).

### Analogy

Think of a **pizza shop chain**. Headquarters defines: "every shop must have a `make_pizza(order)` method that returns a pizza." But the **New York branch** makes NY-style pizza. The **Chicago branch** makes deep-dish. Same operation (`make_pizza`), different concrete product per branch.

A customer walks into any shop and orders — they don't care about the implementation. The shop produces its own style.

### Structure

- **Product** — the abstract interface (`Notifier`).
- **Concrete Products** — `EmailNotifier`, `SMSNotifier`, etc.
- **Creator** — abstract class with a `factory_method()` that returns a Product.
- **Concrete Creators** — subclasses overriding `factory_method()` to return specific Products.

### Python Implementation

```python
from abc import ABC, abstractmethod

# Products
class Notifier(ABC):
    @abstractmethod
    def send(self, msg): pass

class EmailNotifier(Notifier):
    def send(self, msg): print(f"Email: {msg}")

class SMSNotifier(Notifier):
    def send(self, msg): print(f"SMS: {msg}")


# Creators
class NotificationService(ABC):
    @abstractmethod
    def create_notifier(self) -> Notifier: pass   # <-- THE factory method:
    # an abstract "creation hook" the base class declares but refuses to
    # implement. Each subclass decides which concrete Product to return,
    # so the *choice of class to instantiate* is deferred to subclasses.

    def notify(self, msg):
        # The base class owns the high-level workflow and calls the factory
        # method without knowing which concrete Notifier it gets back. This is
        # the whole point: behavior is fixed here, product choice varies below.
        notifier = self.create_notifier()
        notifier.send(msg)


class EmailService(NotificationService):
    def create_notifier(self): return EmailNotifier()   # subclass fills the hook

class SMSService(NotificationService):
    def create_notifier(self): return SMSNotifier()     # different product, same flow


service = EmailService()
service.notify("Welcome!")   # Email: Welcome!
```

The `NotificationService.notify` logic doesn't care which notifier comes out of `create_notifier()`. Subclasses vary the Product without changing the surrounding logic.

### Simpler Variant — Parameterized Factory

Often you don't need multiple Creator subclasses. A single factory function that takes a parameter works:

```python
def notifier_factory(kind) -> Notifier:
    notifiers = {
        "email": EmailNotifier,
        "sms": SMSNotifier,
    }
    return notifiers[kind]()

notifier = notifier_factory("email")
notifier.send("hi")
```

Some purists distinguish between "Factory Method" (the GoF subclass version) and "Simple Factory" (the parameterized function). In practice, both solve the same pain and are often called "factories."

### Realistic Use Case

**Document parsers**:

```python
class Document(ABC):
    @abstractmethod
    def parse(self, raw): pass

class PDFDocument(Document):
    def parse(self, raw): return f"PDF parsed: {raw[:20]}..."

class DocxDocument(Document):
    def parse(self, raw): return f"DOCX parsed: {raw[:20]}..."

def document_factory(file_ext) -> Document:
    return {"pdf": PDFDocument, "docx": DocxDocument}[file_ext]()
```

Callers just say `document_factory("pdf").parse(raw)` — no knowledge of internals.

### Tradeoffs

**Pros:**
- Decouples object creation from usage.
- Obeys OCP: add a new Product → add a new Concrete Creator (or a new line in the mapping).
- Makes testing easier — swap in a fake factory.

**Cons:**
- More classes — can feel heavy for trivial cases.
- Adds a layer of indirection (new readers have to trace through the factory).

### Related Patterns

- **Abstract Factory** — when you need families of related products, not just one.
- **Builder** — when the object itself is complex to construct step by step.
- **Strategy** — structurally similar but about *swappable behaviors*, not object creation.

### Python-Specific Notes

Python's first-class functions and dicts-of-callables (`{"email": EmailNotifier, ...}`) make factories extremely lightweight. You rarely need the full GoF hierarchy of Creators — a dict-based registry or a function usually suffices.

---

## 8. Abstract Factory

### The Pain

Imagine you're building a UI framework that must work on **Windows, Mac, and Linux**. Each OS has its own look for buttons, checkboxes, menus, etc.

With Factory Method, you could have a factory for buttons, another for checkboxes, another for menus. But nothing guarantees they're *consistent* — someone might accidentally mix a Mac button with a Windows checkbox. The UI looks like Frankenstein.

You need a way to say: *"give me the entire Mac family of UI components, all consistent with each other,"* or *"give me the Windows family."*

### Intent

> Provide an interface for creating families of related or dependent objects without specifying their concrete classes.

### Analogy

Think of a **themed meal combo** at a restaurant.

A "Mexican combo" = tacos + salsa + horchata. A "Italian combo" = pasta + garlic bread + Chianti. A "Japanese combo" = sushi + miso + green tea.

You order "Italian combo," and the kitchen knows the entire consistent set to prepare. You don't mix sushi with garlic bread (unless you have very specific tastes).

The restaurant is the **Abstract Factory**. Each combo is a **Concrete Factory**. The individual items are **Products**.

### Structure

- **Abstract Products** — `Button`, `Checkbox`, `Menu` (interfaces).
- **Concrete Products** — `MacButton`, `MacCheckbox`; `WinButton`, `WinCheckbox`; etc.
- **Abstract Factory** — interface declaring creators: `create_button()`, `create_checkbox()`.
- **Concrete Factories** — `MacFactory`, `WinFactory`, each producing their own consistent family.

### Python Implementation

```python
from abc import ABC, abstractmethod

# Abstract Products
class Button(ABC):
    @abstractmethod
    def render(self): pass

class Checkbox(ABC):
    @abstractmethod
    def render(self): pass


# Concrete Products — Mac family
class MacButton(Button):
    def render(self): print("Rendering Mac button")

class MacCheckbox(Checkbox):
    def render(self): print("Rendering Mac checkbox")


# Concrete Products — Windows family
class WinButton(Button):
    def render(self): print("Rendering Windows button")

class WinCheckbox(Checkbox):
    def render(self): print("Rendering Windows checkbox")


# Abstract Factory
class UIFactory(ABC):
    # Unlike Factory Method (which has ONE creation hook), an Abstract Factory
    # declares a *set* of related creation methods. Each one below is a factory
    # method; together they define a whole product family the client builds.
    @abstractmethod
    def create_button(self) -> Button: pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox: pass


# Concrete Factories — each implements the ENTIRE family for one platform, which
# is what guarantees the products it returns belong together (all Mac, all Win).
class MacFactory(UIFactory):
    def create_button(self): return MacButton()
    def create_checkbox(self): return MacCheckbox()

class WinFactory(UIFactory):
    def create_button(self): return WinButton()
    def create_checkbox(self): return WinCheckbox()


# Client code — doesn't know or care which concrete family it's using
def build_ui(factory: UIFactory):
    button = factory.create_button()
    checkbox = factory.create_checkbox()
    button.render()
    checkbox.render()


build_ui(MacFactory())
# Rendering Mac button
# Rendering Mac checkbox

build_ui(WinFactory())
# Rendering Windows button
# Rendering Windows checkbox
```

Key property: within one factory, all products are **guaranteed consistent**. No one can accidentally mix Mac buttons with Windows checkboxes — the factory enforces the family.

### Realistic Use Cases

- **Cross-platform UI toolkits** (classic example).
- **Multi-database support** — one factory produces a `Connection`, `QueryBuilder`, and `Transaction` for MySQL; another for Postgres. The factory ensures you never mix Postgres-specific SQL with a MySQL connection.
- **Theming systems** — light theme factory vs dark theme factory, each producing matching colors, fonts, icons.

### Factory Method vs Abstract Factory

| Factory Method | Abstract Factory |
|---|---|
| Creates **one** product | Creates a **family** of related products |
| Variation through subclassing or parameter | Variation through swapping the whole factory |
| Simpler | More setup, more classes |
| Use when you need "which kind of X?" | Use when you need "which family of related things?" |

### Tradeoffs

**Pros:**
- Guarantees internal consistency among related products.
- Strongly supports OCP — new families add new factories without touching client code.
- Decouples client from concrete classes entirely.

**Cons:**
- Significant class proliferation. A dozen products × a dozen families = lots of classes.
- Adding a *new kind of product* to the family (e.g., add `Slider` to the UIFactory) forces every existing factory to implement it — a pain.

### Related Patterns

- **Factory Method** — the single-product cousin.
- **Builder** — when constructing each individual product is complex.
- **Prototype** — sometimes used inside Abstract Factories to create products by cloning templates.

---

## 9. Builder

### The Pain

Consider a `Pizza` class with many configuration options: size, crust, cheese, sauce, toppings, extra cheese, gluten-free, etc. Naively:

```python
pizza = Pizza("large", "thin", "mozzarella", "tomato",
              ["olives", "mushrooms"], extra_cheese=True,
              gluten_free=False, spicy=True, ...)
```

Problems:

1. **Telescoping constructor** — what does argument 7 mean? Unreadable.
2. **Many combinations** — some args only make sense with others (`gluten_free=True` with `crust="regular"`?).
3. **Optional parameters** — constructors become unwieldy.
4. **Immutability tension** — if you want the final Pizza to be immutable, how do you configure it step-by-step?

### Intent

> Separate the construction of a complex object from its representation, so the same construction process can create different representations.

Essentially: *build the object in **steps**, with a clean API, and only produce the final object once all configuration is done.*

### Analogy

Think of **ordering a custom burger at Subway** or **building a PC**.

At Subway: you start empty, then *step by step* pick your bread, protein, veggies, sauces. At the end, you get a finished sandwich. You don't have to specify all 20 ingredients in one confusing line.

At a PC builder website: you pick CPU, then motherboard, then RAM, then GPU. The site guides you; only at "Checkout" is the final PC configured.

### Python Implementation

```python
class Pizza:
    def __init__(self):
        self.size = None
        self.crust = None
        self.cheese = None
        self.toppings = []
        self.extra_cheese = False

    def __repr__(self):
        return (f"Pizza(size={self.size}, crust={self.crust}, "
                f"cheese={self.cheese}, toppings={self.toppings}, "
                f"extra_cheese={self.extra_cheese})")


class PizzaBuilder:
    def __init__(self):
        self.pizza = Pizza()

    def set_size(self, size):
        self.pizza.size = size
        # Returning `self` is what makes the fluent interface work: each setter
        # hands back the SAME builder, so the next method can be called directly
        # on the result — `.set_size(...).set_crust(...)`. Without this return,
        # each call would yield None and chaining would break on the second dot.
        return self

    def set_crust(self, crust):
        self.pizza.crust = crust
        return self

    def set_cheese(self, cheese):
        self.pizza.cheese = cheese
        return self

    def add_topping(self, topping):
        self.pizza.toppings.append(topping)
        return self

    def with_extra_cheese(self):
        self.pizza.extra_cheese = True
        return self

    def build(self) -> Pizza:
        return self.pizza


# Usage — fluent, readable
pizza = (PizzaBuilder()
         .set_size("large")
         .set_crust("thin")
         .set_cheese("mozzarella")
         .add_topping("olives")
         .add_topping("mushrooms")
         .with_extra_cheese()
         .build())

print(pizza)
```

Each step is named. Each is optional (you can skip steps). Chainable (each method returns `self`). The final `build()` produces the object.

### The "Director" Variant

In the classical GoF Builder, there's also a **Director** — a class that knows common sequences.

```python
class PizzaDirector:
    def make_margherita(self, builder):
        return (builder.set_size("medium")
                       .set_crust("thin")
                       .set_cheese("mozzarella")
                       .add_topping("basil")
                       .build())

    def make_pepperoni(self, builder):
        return (builder.set_size("large")
                       .set_crust("regular")
                       .set_cheese("mozzarella")
                       .add_topping("pepperoni")
                       .with_extra_cheese()
                       .build())


director = PizzaDirector()
m = director.make_margherita(PizzaBuilder())
p = director.make_pepperoni(PizzaBuilder())
```

The Director holds recipes. Same builder, different recipes, different pizzas.

### Realistic Use Cases

- **SQL query builders** (SQLAlchemy's `select().where().order_by()...`).
- **HTTP request builders** (`requests`-style fluent APIs, or `urllib3` Pool configuration).
- **Configuration objects** with many optional fields.
- **Test data builders** — create a complex test fixture step by step.

### Tradeoffs

**Pros:**
- Hides complex construction behind a clean, step-by-step API.
- Supports multiple representations — different builders can produce pizzas differently (e.g., a `PizzaXMLBuilder` that builds XML instead).
- Makes optional/variable construction elegant.
- Can enforce construction order or validation in `build()`.

**Cons:**
- Duplication — you're essentially mirroring the Product's fields with builder methods.
- Overkill for simple objects with 2-3 fields.

### Related Patterns

- **Abstract Factory** — Builder constructs one complex object; Abstract Factory creates families. They sometimes work together (a factory may return a builder).
- **Fluent Interface** — a more general style; Builder is a common application of it.

### Python-Specific Notes

Python's keyword arguments and `@dataclass` often obviate the need for a Builder for simple cases:

```python
@dataclass
class Pizza:
    size: str
    crust: str = "thin"
    cheese: str = "mozzarella"
    toppings: list = field(default_factory=list)
    extra_cheese: bool = False

pizza = Pizza(size="large", toppings=["olives"], extra_cheese=True)
```

Reach for Builder when:
- Construction has **validation rules** across multiple fields.
- You want a **fluent/chainable API** for readability.
- The object has **many optional fields** and keyword arguments would be too many.
- You need **multiple representations** of the same "build plan."

---

## 10. Prototype

### The Pain

Suppose you have an elaborate object — say, a pre-configured game character with specific stats, equipment, abilities, and a name. You want to spawn 100 similar enemies that differ only slightly. Recreating the object from scratch every time is:

1. **Slow** — if construction involves expensive computation or DB queries.
2. **Redundant** — if 95% of the new object is identical to the original.
3. **Losing context** — the original might have state accumulated over time that you'd like to preserve.

### Intent

> Specify the kinds of objects to create using a prototypical instance, and create new objects by **cloning** this prototype.

### Analogy

Think of **photocopying a document** instead of retyping it.

You have a filled-out form with your name, address, and signature. You need 50 copies. You don't re-fill the form 50 times — you photocopy it. Then you edit specific fields on each copy if needed.

Or: **Ctrl+C, Ctrl+V** followed by small tweaks.

### Python Implementation

Python makes this pattern almost trivial thanks to the `copy` module:

```python
import copy

class Enemy:
    def __init__(self, name, hp, weapon, abilities):
        self.name = name
        self.hp = hp
        self.weapon = weapon
        self.abilities = abilities

    def clone(self):
        return copy.deepcopy(self)

    def __repr__(self):
        return f"Enemy({self.name}, HP={self.hp}, weapon={self.weapon}, abilities={self.abilities})"


# Prototype: an elite guard
guard_prototype = Enemy("Guard", 100, "sword", ["block", "slash"])

# Spawn similar enemies cheaply
guard1 = guard_prototype.clone()
guard1.name = "Guard-1"

guard2 = guard_prototype.clone()
guard2.name = "Guard-2"
guard2.abilities.append("shield_bash")   # Mutating this copy doesn't affect others

print(guard_prototype)
print(guard1)
print(guard2)
```

### Shallow vs Deep Copy — A Crucial Detail

Python offers two kinds of copying:

- **`copy.copy(obj)`** — shallow copy. Copies the outer object, but nested mutable objects are still shared.
- **`copy.deepcopy(obj)`** — deep copy. Recursively copies everything. Fully independent.

This matters!

```python
import copy

original = {"scores": [1, 2, 3]}
shallow = copy.copy(original)
deep = copy.deepcopy(original)

shallow["scores"].append(4)
print(original["scores"])   # [1, 2, 3, 4]  ← modified!
print(deep["scores"])       # [1, 2, 3]    ← independent
```

For Prototype, **deep copy** is usually the correct choice unless you explicitly want shared references (e.g., a shared textures dictionary in a game).

### Realistic Use Cases

- **Game development** — spawn many similar enemies, items, or particles from a template.
- **Graphics / UI** — replicate configured components.
- **Test fixtures** — build a complex "base" state once, then clone and modify for each test.
- **Configuration templates** — start from a default config, clone, and override specific fields per environment.
- **Undo/redo systems** — sometimes cloning the state is cheaper than re-running actions.

### Tradeoffs

**Pros:**
- Faster than reconstructing expensive objects.
- Hides complex construction behind `.clone()`.
- Preserves state at the moment of cloning.
- Works well with dynamic configurations (prototype is configured at runtime, then cloned).

**Cons:**
- Deep-copying objects with cyclic references, file handles, or sockets gets tricky.
- Shallow vs deep copy mistakes are a common bug source.
- Many modern languages and frameworks handle "object templates" differently (e.g., factories, dataclasses).

### Related Patterns

- **Abstract Factory** — sometimes uses Prototype internally (factory holds prototypical instances, clones them on demand).
- **Singleton** — the philosophical opposite. Singleton restricts to one; Prototype encourages many clones.

### Python-Specific Notes

Python's `copy.deepcopy` gives you Prototype almost for free. You can override `__deepcopy__` on a class to customize cloning (e.g., reset certain fields to defaults, exclude certain fields).

```python
def __deepcopy__(self, memo):
    # __deepcopy__ is the hook copy.deepcopy() calls if a class defines it. We
    # override it precisely when "copy everything verbatim" is WRONG for some
    # fields. The `memo` dict is deepcopy's bookkeeping — it tracks objects
    # already copied so shared/cyclic references aren't duplicated or looped
    # infinitely. We must thread it through any nested deepcopy calls.
    new = Enemy(self.name, self.hp, self.weapon,
                copy.deepcopy(self.abilities, memo))  # abilities: truly independent per clone
    # Some fields should NOT be carried over identically — they must be unique
    # to each clone. A timestamp is the classic case: the clone was created now,
    # not when the prototype was. So we reset it instead of copying it.
    new.last_cloned_at = datetime.now()
    return new
```

---

## 11. Summary of Creational Patterns

All five creational patterns tackle the same overarching question — **how do we create objects flexibly?** — but each addresses a different axis of variation:

| Pattern | The Question It Answers | Varies What? |
|---|---|---|
| **Singleton** | "How do I ensure only one of this exists?" | Count (exactly one) |
| **Factory Method** | "How do I let the right concrete class be chosen without the client knowing?" | Which concrete class |
| **Abstract Factory** | "How do I create a whole family of consistent related objects?" | Which family of related classes |
| **Builder** | "How do I assemble a complex object step-by-step with clarity?" | Construction process |
| **Prototype** | "How do I create a new object from an existing one efficiently?" | How the object is originated (clone vs build) |

### Decision Flow

A practical way to choose:

1. **Need exactly one?** → Singleton (but strongly prefer module-level or DI first).
2. **Need to pick among a few types, based on input?** → Factory Method (or simple factory function).
3. **Need consistent families of related types?** → Abstract Factory.
4. **Object has many optional fields, or complex construction?** → Builder.
5. **Need to rapidly create objects similar to an existing one?** → Prototype.

### Key Takeaways

1. **Creational patterns are about *isolating* the knowledge of *what* gets created from the code that *uses* what gets created.** This decoupling is the entire point.
2. **Python often simplifies these patterns.** Module-level singletons, keyword arguments + dataclasses, and `copy.deepcopy` mean you reach for the full GoF hierarchy less often than in Java/C++. Recognize the *pattern*, then ask "what's the Pythonic way?"
3. **Patterns are not free.** Every factory, builder, or prototype adds classes and indirection. Apply when the flexibility is actually needed.
4. **SOLID lives inside these patterns.** Notice how OCP and DIP quietly show up in every single creational pattern — clients depend on interfaces, not concrete classes, so new types can be added without modification.

---

## 12. Practice Exercises

### Exercise 1 — Singleton

Implement a `ConfigManager` class that reads configuration from a dictionary once at startup and is accessible as a singleton. Ensure that calling `ConfigManager()` multiple times returns the same instance, and that modifications to config via one reference are visible from all others.

**Solution:**

```python
class ConfigManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = {}
        return cls._instance

    def load(self, config_dict):
        self._config = config_dict

    def get(self, key, default=None):
        return self._config.get(key, default)

    def set(self, key, value):
        self._config[key] = value


a = ConfigManager()
a.load({"db_host": "localhost", "port": 5432})

b = ConfigManager()
print(b.get("db_host"))   # localhost

b.set("port", 6000)
print(a.get("port"))      # 6000 — shared state
print(a is b)             # True
```

**Pythonic alternative:** use a module-level config dict in a `config.py` file — simpler, no `__new__` trickery, and just as singleton-ish.

---

### Exercise 2 — Factory Method

You're building a **shape-drawing tool**. Given a string (`"circle"`, `"square"`, `"triangle"`), return the appropriate shape object with a `draw()` method. Design this using Factory Method so that adding `"hexagon"` later requires no modification to the client code.

**Solution:**

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def draw(self): pass

class Circle(Shape):
    def draw(self): print("Drawing circle")

class Square(Shape):
    def draw(self): print("Drawing square")

class Triangle(Shape):
    def draw(self): print("Drawing triangle")


# Registry-based factory — easy to extend
_shape_registry = {
    "circle": Circle,
    "square": Square,
    "triangle": Triangle,
}

def shape_factory(kind) -> Shape:
    if kind not in _shape_registry:
        raise ValueError(f"Unknown shape: {kind}")
    return _shape_registry[kind]()


# Client code
for s in ["circle", "square", "triangle"]:
    shape_factory(s).draw()


# Adding Hexagon later — no change to client
class Hexagon(Shape):
    def draw(self): print("Drawing hexagon")

_shape_registry["hexagon"] = Hexagon
shape_factory("hexagon").draw()
```

The client `shape_factory(...).draw()` never changes. New shapes plug in through the registry.

---

### Exercise 3 — Abstract Factory

Design an Abstract Factory for a **cross-platform form UI** with two products: `TextInput` and `SubmitButton`. Support `MaterialDesign` and `iOSStyle` families. Write a `build_form` function that uses whichever factory it's given and renders a consistent form.

**Solution:**

```python
from abc import ABC, abstractmethod

# Abstract Products
class TextInput(ABC):
    @abstractmethod
    def render(self): pass

class SubmitButton(ABC):
    @abstractmethod
    def render(self): pass


# Material family
class MaterialTextInput(TextInput):
    def render(self): print("[Material TextInput with floating label]")

class MaterialSubmitButton(SubmitButton):
    def render(self): print("[Material raised button]")


# iOS family
class iOSTextInput(TextInput):
    def render(self): print("(iOS rounded TextInput)")

class iOSSubmitButton(SubmitButton):
    def render(self): print("(iOS styled button)")


# Abstract Factory
class FormUIFactory(ABC):
    @abstractmethod
    def create_text_input(self) -> TextInput: pass
    @abstractmethod
    def create_submit_button(self) -> SubmitButton: pass


class MaterialFactory(FormUIFactory):
    def create_text_input(self): return MaterialTextInput()
    def create_submit_button(self): return MaterialSubmitButton()


class iOSFactory(FormUIFactory):
    def create_text_input(self): return iOSTextInput()
    def create_submit_button(self): return iOSSubmitButton()


# Client code
def build_form(factory: FormUIFactory):
    factory.create_text_input().render()
    factory.create_submit_button().render()


print("-- Material --")
build_form(MaterialFactory())

print("-- iOS --")
build_form(iOSFactory())
```

No mixing is possible — the factory guarantees consistency within each family.

---

### Exercise 4 — Builder

Design a Builder for a `HttpRequest` object with optional method, URL, headers (dict), query params (dict), body, and timeout. Support a fluent API. Make `build()` validate that at minimum URL is provided.

**Solution:**

```python
class HttpRequest:
    def __init__(self):
        self.method = "GET"
        self.url = None
        self.headers = {}
        self.query = {}
        self.body = None
        self.timeout = 30

    def __repr__(self):
        return (f"HttpRequest({self.method} {self.url} "
                f"headers={self.headers} query={self.query} "
                f"body={self.body} timeout={self.timeout})")


class HttpRequestBuilder:
    def __init__(self):
        self.req = HttpRequest()

    def method(self, m):
        self.req.method = m
        return self

    def url(self, u):
        self.req.url = u
        return self

    def header(self, key, value):
        self.req.headers[key] = value
        return self

    def query_param(self, key, value):
        self.req.query[key] = value
        return self

    def body(self, b):
        self.req.body = b
        return self

    def timeout(self, t):
        self.req.timeout = t
        return self

    def build(self) -> HttpRequest:
        if self.req.url is None:
            raise ValueError("URL is required")
        return self.req


req = (HttpRequestBuilder()
       .method("POST")
       .url("https://api.example.com/users")
       .header("Authorization", "Bearer xyz")
       .header("Content-Type", "application/json")
       .query_param("active", "true")
       .body('{"name": "Amit"}')
       .timeout(60)
       .build())

print(req)
```

Note how the `build()` step enforces the invariant (URL required). Doing this in a plain constructor would be ugly with so many optional args.

---

### Exercise 5 — Prototype

Create a `Document` class representing a text document with a title, body, tags (list), and metadata (dict). Implement `clone()` such that modifying a clone's tags or metadata does NOT affect the prototype. Demonstrate the difference by showing what happens with shallow vs deep copy.

**Solution:**

```python
import copy

class Document:
    def __init__(self, title, body, tags=None, metadata=None):
        self.title = title
        self.body = body
        self.tags = tags or []
        self.metadata = metadata or {}

    def clone(self):
        return copy.deepcopy(self)

    def shallow_clone(self):
        return copy.copy(self)

    def __repr__(self):
        return f"Document({self.title!r}, tags={self.tags}, metadata={self.metadata})"


prototype = Document("Blog Template", "Introduction...",
                     tags=["draft"], metadata={"author": "Amit"})

# Deep clone — independent
deep = prototype.clone()
deep.tags.append("published")
deep.metadata["reviewed"] = True
print("Original after deep clone mutation:", prototype)
# Original is unchanged: tags=['draft'], metadata={'author': 'Amit'}
print("Deep clone:", deep)

# Shallow clone — dangerous!
shallow = prototype.shallow_clone()
shallow.tags.append("shared!")
print("Original after shallow clone mutation:", prototype)
# Original.tags is now ['draft', 'shared!'] — mutation leaked
```

**Takeaway:** with mutable nested fields (lists, dicts), always use `deepcopy` for true Prototype behavior.

---

### Exercise 6 — Full Capstone (Combining Patterns)

Design a system for creating **database connections** that uses multiple patterns together:

- **Singleton** — one `ConnectionPool` per application.
- **Factory Method** — pool produces different kinds of connections (`ReadOnlyConnection`, `WriteConnection`, `AdminConnection`) based on the requested role.
- **Abstract Factory** (optional) — support multiple database backends (MySQL family vs Postgres family).
- **Builder** (optional) — complex connection config constructed step-by-step.

Outline the class structure and provide a working code example.

**Solution (one possible design):**

```python
from abc import ABC, abstractmethod
import copy

# --- Products: Connections ---
class Connection(ABC):
    @abstractmethod
    def execute(self, query): pass

class MySQLReadConnection(Connection):
    def execute(self, query): print(f"[MySQL-READ] {query}")
class MySQLWriteConnection(Connection):
    def execute(self, query): print(f"[MySQL-WRITE] {query}")
class PostgresReadConnection(Connection):
    def execute(self, query): print(f"[PG-READ] {query}")
class PostgresWriteConnection(Connection):
    def execute(self, query): print(f"[PG-WRITE] {query}")


# --- Abstract Factory: per-backend connection family ---
class ConnectionFactory(ABC):
    @abstractmethod
    def create_read(self) -> Connection: pass
    @abstractmethod
    def create_write(self) -> Connection: pass


class MySQLFactory(ConnectionFactory):
    def create_read(self): return MySQLReadConnection()
    def create_write(self): return MySQLWriteConnection()

class PostgresFactory(ConnectionFactory):
    def create_read(self): return PostgresReadConnection()
    def create_write(self): return PostgresWriteConnection()


# --- Singleton Pool ---
class ConnectionPool:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._factory = None
        return cls._instance

    def configure(self, factory: ConnectionFactory):
        self._factory = factory

    def get_connection(self, role: str) -> Connection:
        if self._factory is None:
            raise RuntimeError("Pool not configured")
        if role == "read":
            return self._factory.create_read()
        elif role == "write":
            return self._factory.create_write()
        else:
            raise ValueError(f"Unknown role: {role}")


# --- Usage ---
pool = ConnectionPool()
pool.configure(PostgresFactory())

# Same pool instance everywhere
same_pool = ConnectionPool()
assert pool is same_pool

pool.get_connection("read").execute("SELECT * FROM users")
pool.get_connection("write").execute("INSERT INTO users ...")

# Switch backends at runtime
pool.configure(MySQLFactory())
pool.get_connection("read").execute("SELECT * FROM orders")
```

**Patterns identified:**
- `ConnectionPool` — Singleton.
- `get_connection(role)` — Factory Method (picks which connection class based on the role argument).
- `ConnectionFactory` + `MySQLFactory` / `PostgresFactory` — Abstract Factory (families of related products).

Each pattern solves a distinct problem; together they create a flexible system.

---

## 13. Self-Assessment Test

*Answer each question before revealing the answer. Tests conceptual understanding.*

<details>

**Q1.** Why is a module-level variable in Python often a better choice than an explicit Singleton class?

<br>

**Answer:** Because Python modules are themselves singletons (import caches them). A module gives you global state without the complexity of `__new__`, thread-safety issues, or hidden dependency problems. Use the Singleton pattern only when you need a class with mutable state and methods, and can't use dependency injection.

---

**Q2.** What's the key difference between Factory Method and Abstract Factory?

<br>

**Answer:** Factory Method creates **one** product type (the method decides which concrete class). Abstract Factory creates a **family of related products** together, ensuring they are consistent with each other. Rule of thumb: "Which concrete X?" → Factory Method. "Which consistent family of Xs and Ys?" → Abstract Factory.

---

**Q3.** When would you use Builder instead of just passing keyword arguments to a constructor?

<br>

**Answer:** When (a) the object has many optional fields and keyword-argument lists become unreadable, (b) construction has multi-field validation rules best checked at the end, (c) you want a fluent/chainable API for readability, or (d) the same builder steps should produce multiple representations (e.g., a builder that builds JSON vs XML from the same configuration).

---

**Q4.** Why is `copy.deepcopy` usually the right choice for Prototype instead of `copy.copy`?

<br>

**Answer:** Because most real-world objects contain nested mutable fields (lists, dicts, custom objects). `copy.copy` only copies the top level — nested objects remain shared between original and clone. Mutations to the clone then leak back to the prototype. Deep copy recursively duplicates everything, giving true independence.

---

**Q5.** Identify the pattern: "A class that ensures only one instance and offers global access."

<br>

**Answer:** Singleton.

---

**Q6.** Identify the pattern: "A class that builds a complex object in steps, with each step returning `self` for chaining."

<br>

**Answer:** Builder.

---

**Q7.** Which SOLID principles does Factory Method primarily support, and why?

<br>

**Answer:** Primarily **OCP** (adding a new product type requires adding a new factory case, not modifying existing ones) and **DIP** (clients depend on the abstract Product interface, not concrete classes). Also weakly **SRP** — creation logic is separated from usage logic.

---

**Q8.** What's a major downside of Abstract Factory?

<br>

**Answer:** Adding a new *kind of product* to the family (e.g., a new `Slider` interface to a UI factory) forces **every existing concrete factory** to implement it. Families extend easily, but products within families do not. This rigidity is the classic Abstract Factory pain.

---

**Q9.** You have a class with 15 optional fields. Your constructor is becoming unreadable. Which creational pattern is most appropriate?

<br>

**Answer:** **Builder**. Alternatively, in Python, `@dataclass` with keyword arguments can handle simpler cases without a full Builder. If validation across multiple fields is needed at construction time, or a fluent interface is desired, Builder is the clearer choice.

---

**Q10.** You want to create 1,000 slightly-different enemy game objects, all variations of the same "boss" template. Which pattern fits best?

<br>

**Answer:** **Prototype**. Create the fully-configured boss once, then clone it 1,000 times, tweaking only the differences. Cheaper than invoking a complex factory 1,000 times.

---

**Q11.** Why might overusing Singleton be a code smell?

<br>

**Answer:** Singletons introduce **global, mutable state**, which makes unit testing hard (tests bleed into each other), creates **hidden dependencies** (classes using them don't declare the dependency), and tightly couples the codebase. Many Singletons are better replaced with dependency injection — the "one instance" is created at startup and passed explicitly to those who need it.

---

**Q12.** A colleague wraps every class in a factory. Is this a good idea?

<br>

**Answer:** No — this is *pattern fever*. Factories are valuable when (a) the concrete class choice varies, (b) construction logic is complex, or (c) you need to decouple callers from concrete types. For classes whose instantiation is trivial and stable, a direct `ClassName()` call is clearer. Patterns are tools, not decorations.

</details>

---

**You've now mastered the Creational patterns.** Each one is a different answer to "how do we create objects flexibly?" — and each embodies SOLID principles in a specific, reusable shape.

**Next up: Structural Patterns** — how to combine objects into larger structures (Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy). These focus on **how objects fit together** rather than how they're created.

---

*This content is part of **Codeverra** — a platform for learning coding, data science, DSA, and AI from scratch. Explore more: https://codeverra.com*
