"""
Food delivery app backend -- showing coroutines, tasks and the event loop.

When a user opens the app, the backend must call several other services
(user service, restaurant service, offers service, order history service).
Each call is network I/O: the server just WAITS for a reply. That waiting
is exactly what asyncio lets us overlap.

The services are simulated with asyncio.sleep() so the demo runs anywhere,
but each one stands in for a real HTTP / database call.
"""
import asyncio
import time

START = time.perf_counter()


def log(msg):
    print(f"[{time.perf_counter() - START:4.1f}s] {msg}")


def reset_clock(title):
    global START
    START = time.perf_counter()
    print(f"\n{'=' * 60}\n{title}\n{'=' * 60}")


# ---------------------------------------------------------------------------
# "Microservices" -- each one is a network call that takes some time
# ---------------------------------------------------------------------------

async def fetch_user_profile(user_id):
    log(f"  -> user-service: get profile of user {user_id}")
    await asyncio.sleep(0.5)
    log("  <- user-service: profile received")
    return {"id": user_id, "name": "Asha", "city": "Bengaluru"}


async def fetch_restaurants(city):
    log(f"  -> restaurant-service: restaurants open in {city}")
    await asyncio.sleep(1.5)
    log("  <- restaurant-service: 42 restaurants")
    return ["Meghana Foods", "Truffles", "CTR"]


async def fetch_offers(user_id):
    log("  -> offers-service: offers for user")
    await asyncio.sleep(1.8)
    log("  <- offers-service: 3 offers")
    return ["50% off up to 100", "Free delivery", "20% off on Truffles"]


async def fetch_past_orders(user_id):
    log("  -> order-service: past orders")
    await asyncio.sleep(1.2)
    log("  <- order-service: 7 past orders")
    return ["Biryani", "Burger", "Masala Dosa"]


# ---------------------------------------------------------------------------
# DEMO 1: await one after another -> no concurrency
#   `await coro` runs the coroutine inline, like a normal function call.
#   The event loop has only one task, so nothing overlaps.
# ---------------------------------------------------------------------------

async def home_screen_sequential(user_id):
    profile = await fetch_user_profile(user_id)
    restaurants = await fetch_restaurants(profile["city"])
    offers = await fetch_offers(user_id)
    past_orders = await fetch_past_orders(user_id)
    log(f"HOME SCREEN READY for {profile['name']}")
    return profile, restaurants, offers, past_orders


# ---------------------------------------------------------------------------
# DEMO 2: gather -> concurrency
#   restaurants NEEDS the city from the profile, so the profile call must
#   come first. The other three calls are independent, so gather wraps each
#   one in a Task and the event loop runs them at the same time.
# ---------------------------------------------------------------------------

async def home_screen_gather(user_id):
    profile = await fetch_user_profile(user_id)          # dependency first
    restaurants, offers, past_orders = await asyncio.gather(
        fetch_restaurants(profile["city"]),
        fetch_offers(user_id),
        fetch_past_orders(user_id),
    )
    log(f"HOME SCREEN READY for {profile['name']}")
    return profile, restaurants, offers, past_orders


# ---------------------------------------------------------------------------
# DEMO 3: create_task -> start work EARLY
#   offers and past orders don't need the profile, so we start them as
#   tasks straight away. They begin running as soon as this coroutine
#   yields (at `await fetch_user_profile`) -- NOT when we await the task.
# ---------------------------------------------------------------------------

async def home_screen_tasks(user_id):
    offers_task = asyncio.create_task(fetch_offers(user_id))
    orders_task = asyncio.create_task(fetch_past_orders(user_id))
    log("tasks created (scheduled, not running yet)")

    profile = await fetch_user_profile(user_id)   # yield -> tasks start now
    restaurants = await fetch_restaurants(profile["city"])

    offers = await offers_task        # just collects the result
    past_orders = await orders_task
    log(f"HOME SCREEN READY for {profile['name']}")
    return profile, restaurants, offers, past_orders


# ---------------------------------------------------------------------------
# DEMO 4: fire-and-forget background work
#   After payment succeeds, the user should see "Order placed" straight
#   away. SMS and email confirmations run as background tasks -- nobody
#   awaits them in the request.
# ---------------------------------------------------------------------------

async def charge_payment(amount):
    log(f"  -> payment-gateway: charge Rs {amount}")
    await asyncio.sleep(1.0)
    log("  <- payment-gateway: success")


async def send_sms(phone, text):
    log(f"  -> sms-service: sending to {phone}")
    await asyncio.sleep(2.0)
    log("  <- sms-service: delivered")


async def send_email(email, text):
    log(f"  -> email-service: sending to {email}")
    await asyncio.sleep(1.5)
    log("  <- email-service: delivered")


background_tasks = set()   # keep references so tasks aren't garbage-collected


async def place_order(amount):
    await charge_payment(amount)       # must finish before we confirm

    for coro in (send_sms("98xxxxxx01", "Order placed!"),
                 send_email("asha@example.com", "Order placed!")):
        task = asyncio.create_task(coro)
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)

    log("RESPONSE SENT TO APP: 'Order placed!'  (notifications still going)")


async def order_demo():
    await place_order(450)
    # A real web server keeps running forever. Here we wait for the background
    # tasks, otherwise asyncio.run would cancel them when this function returns.
    await asyncio.gather(*background_tasks)


# ---------------------------------------------------------------------------
# DEMO 5: the classic mistake -- a BLOCKING call inside async code
#   Imagine the offers service is called with a sync library such as
#   `requests`. time.sleep() below stands in for that call. It never yields,
#   so the event loop is frozen and gather can't overlap anything.
#   Fix: run the blocking call in a thread with asyncio.to_thread().
# ---------------------------------------------------------------------------

def fetch_offers_sync_library(user_id):      # e.g. requests.get(...)
    log("  -> offers-service (BLOCKING client)")
    time.sleep(1.8)
    log("  <- offers-service (BLOCKING client)")
    return ["50% off up to 100"]


async def fetch_offers_blocking(user_id):
    return fetch_offers_sync_library(user_id)          # freezes the loop


async def fetch_offers_in_thread(user_id):
    return await asyncio.to_thread(fetch_offers_sync_library, user_id)


async def home_screen_with(offers_fn, user_id):
    profile = await fetch_user_profile(user_id)
    await asyncio.gather(
        fetch_restaurants(profile["city"]),
        offers_fn(user_id),
        fetch_past_orders(user_id),
    )
    log("HOME SCREEN READY")


# ---------------------------------------------------------------------------

async def main():
    reset_clock("DEMO 1: sequential awaits          (expect ~5.0s)")
    await home_screen_sequential(user_id=7)

    reset_clock("DEMO 2: gather independent calls   (expect ~2.3s)")
    await home_screen_gather(user_id=7)

    reset_clock("DEMO 3: create_task to start early (expect ~2.0s)")
    await home_screen_tasks(user_id=7)

    reset_clock("DEMO 4: background notifications after payment")
    await order_demo()

    reset_clock("DEMO 5a: blocking call inside gather (expect ~3.5s)")
    await home_screen_with(fetch_offers_blocking, user_id=7)

    reset_clock("DEMO 5b: blocking call moved to a thread (expect ~2.3s)")
    await home_screen_with(fetch_offers_in_thread, user_id=7)


asyncio.run(main())
