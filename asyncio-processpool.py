import asyncio
import os
import time
from concurrent.futures import ProcessPoolExecutor


def count_primes(limit):
    """Pure-Python CPU work: must live at module level so other processes can import it."""
    count = 0
    for n in range(2, limit):
        if all(n % d for d in range(2, int(n ** 0.5) + 1)):
            count += 1
    return count


LIMITS = [300_000, 300_000, 300_000, 300_000]


async def main():
    loop = asyncio.get_running_loop()
    print(f"CPUs available: {os.cpu_count()}")

    start = time.perf_counter()
    results = [count_primes(n) for n in LIMITS]              # blocks the loop throughout
    print(f"In the event loop : {time.perf_counter() - start:.2f}s  {results}")

    start = time.perf_counter()
    results = await asyncio.gather(*(asyncio.to_thread(count_primes, n) for n in LIMITS))
    print(f"asyncio.to_thread : {time.perf_counter() - start:.2f}s  {results}")

    with ProcessPoolExecutor() as pool:                      # one worker per CPU by default
        start = time.perf_counter()
        results = await asyncio.gather(
            *(loop.run_in_executor(pool, count_primes, n) for n in LIMITS)
        )
        print(f"ProcessPoolExecutor: {time.perf_counter() - start:.2f}s  {results}")


if __name__ == "__main__":        # required: worker processes re-import this file
    asyncio.run(main())
# await main()
