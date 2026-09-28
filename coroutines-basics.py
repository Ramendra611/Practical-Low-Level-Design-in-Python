import time
import asyncio

async def call_api(url): # coroutine 
    print(f"calling api for image -- {url}")
    await asyncio.sleep(3)
    print(f"received api response for  ---{url} !!!")


async def download_image(name: str) -> None: # coroutine 
    print(f"starting download - {name}")
    api_coroutine = call_api(f"images.com/download/{name}")
    # print(type(api_coroutine))
    await api_coroutine
    print(f"done downloading ---{name}")


async def main():
    start = time.time()

    coro1 = download_image("image-1.jpg") # coroutine object 
    coro2 = download_image("image-2.jpg")  # coroutine object

    # await coro1
    # await coro2

    task1 = asyncio.create_task(coro1) # created a task -- > creating the coroutine and scheduling it
    task2 = asyncio.create_task(coro2)

    await task1
    await task2

    print("Total time taken: ", time.time() - start)

## run the main coroutine
asyncio.run(main())


