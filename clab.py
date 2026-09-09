"""
clab.py : Concurrency Lab toolkit for the Codeverra Concurrency Workbook.

Everything in this file is deliberately dependency-free so the workbook runs
on a plain CPython 3.9+ installation. It lives in a real module file (rather
than inside a notebook cell) for one important reason: on macOS and Windows,
multiprocessing starts worker processes with the "spawn" method, and a spawned
worker can only run functions it can *import*. Functions defined in a notebook
cell are not importable, so process pools would fail. Functions defined here
are importable everywhere.
"""

from __future__ import annotations

import asyncio
import threading
import time
import zlib
from contextlib import contextmanager

# --------------------------------------------------------------------------
# Timing
# --------------------------------------------------------------------------

@contextmanager
def timed(label: str):
    """Print how long the enclosed block took. Used for every measurement."""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{label:<44} {elapsed:6.2f}s")


# --------------------------------------------------------------------------
# Simulated I/O-bound work: "downloading" an image
# --------------------------------------------------------------------------

NETWORK_LATENCY = 0.30  # seconds per simulated request


def synthetic_image(seed: int, size: int = 96) -> list:
    """
    Produce a deterministic size x size greyscale image as a flat list of ints.
    A tiny linear congruential generator keeps this fast and reproducible.
    """
    pixels = []
    state = seed or 1
    for _ in range(size * size):
        state = (1103515245 * state + 12345) & 0x7FFFFFFF
        pixels.append(state % 256)
    return pixels


def fetch_image(url: str, latency: float = NETWORK_LATENCY) -> list:
    """
    A blocking 'download'.

    time.sleep() releases the GIL while it waits, which is exactly what a real
    socket read does. The timing behaviour of this function under threads,
    processes and asyncio therefore matches a real HTTP call closely enough
    for every lesson in this workbook.
    """
    time.sleep(latency)
    return synthetic_image(zlib.crc32(url.encode()))


async def fetch_image_async(url: str, latency: float = NETWORK_LATENCY) -> list:
    """The asyncio-native counterpart of fetch_image."""
    await asyncio.sleep(latency)
    return synthetic_image(zlib.crc32(url.encode()))


# --------------------------------------------------------------------------
# CPU-bound work: turning an image into a thumbnail
# --------------------------------------------------------------------------

def blur(pixels: list, size: int = 96, passes: int = 6) -> list:
    """
    A 3x3 box blur written in pure Python.

    Pure Python arithmetic holds the GIL for its entire duration, which makes
    this a faithful stand-in for any CPU-bound step: image filtering, parsing,
    compression, hashing in a loop, model scoring.
    """
    current = pixels
    for _ in range(passes):
        out = [0] * (size * size)
        for y in range(size):
            for x in range(size):
                total = 0
                count = 0
                for dy in (-1, 0, 1):
                    ny = y + dy
                    if ny < 0 or ny >= size:
                        continue
                    row = ny * size
                    for dx in (-1, 0, 1):
                        nx = x + dx
                        if 0 <= nx < size:
                            total += current[row + nx]
                            count += 1
                out[y * size + x] = total // count
        current = out
    return current


def make_thumbnail(pixels: list, size: int = 96, factor: int = 4) -> list:
    """Blur, then downsample by averaging each factor x factor block."""
    smoothed = blur(pixels, size=size)
    small = size // factor
    out = []
    for y in range(small):
        for x in range(small):
            total = 0
            for dy in range(factor):
                row = (y * factor + dy) * size
                for dx in range(factor):
                    total += smoothed[row + x * factor + dx]
            out.append(total // (factor * factor))
    return out


def download_and_thumbnail(url: str) -> list:
    """One complete unit of work: I/O-bound fetch followed by CPU-bound processing."""
    return make_thumbnail(fetch_image(url))


# --------------------------------------------------------------------------
# Running asyncio code from a notebook
# --------------------------------------------------------------------------

def run_async(coro):
    """
    Run a coroutine to completion and return its result.

    asyncio.run() creates a fresh event loop, runs the coroutine, and closes
    the loop. It refuses to start if a loop is already running in the current
    thread, which is precisely the situation inside a Jupyter kernel. When a
    loop is already running we execute the coroutine on a dedicated thread
    that owns its own private loop, so the same call works in a notebook, in
    a plain script, and inside another framework's loop.
    """
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    box = {}

    def runner():
        try:
            box["value"] = asyncio.run(coro)
        except BaseException as exc:  # noqa: BLE001 - re-raised on the caller's thread
            box["error"] = exc

    thread = threading.Thread(target=runner)
    thread.start()
    thread.join()
    if "error" in box:
        raise box["error"]
    return box["value"]


IMAGE_URLS = [f"https://images.example.com/photo_{i:02d}.jpg" for i in range(8)]
