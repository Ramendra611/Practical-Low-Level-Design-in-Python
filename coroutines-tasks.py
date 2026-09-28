import asyncio
import time


async def get_user(user_id):
    if user_id == 2:
        raise IndexError
    print(f"[{time.perf_counter() - START:.1f}s] start  user {user_id}")
    await asyncio.sleep(1)
    print(f"[{time.perf_counter() - START:.1f}s] finish user {user_id}")
    return {"id": user_id, "name": f"User {user_id}"}

# fetch the data for 10 user


async def main():

    # await get_user(1)
    # await get_user(2)

    # task_list = [asyncio.create_task(get_user(i)) for i in range(15)]

    # results = []
    # for task in task_list:
    #     result = await task
    #     results.append(result)
    # print(results)

    list_of_coroutines = [get_user(i) for i in range(4)]
    results = await asyncio.gather(*list_of_coroutines, return_exceptions=False)
    print(results)


START = time.perf_counter()
asyncio.run(main())
print(f"Took {time.perf_counter() - START:.1f}s")
