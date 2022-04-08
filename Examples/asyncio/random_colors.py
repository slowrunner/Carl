#!/usr/bin/env python3
# random_colors.py

"""
REF: https://realpython.com/async-io-python/#the-rules-of-async-io

This program uses one main coroutine, makerandom(), and runs it concurrently across 3 different inputs.

Most programs will contain small, modular coroutines and one wrapper function
that serves to chain each of the smaller coroutines together.
main() is then used to gather tasks (futures) by mapping the central coroutine across some iterable or pool.

In this miniature example, the pool is range(3).

While “making random integers” (which is CPU-bound more than anything) is maybe not the greatest choice as a candidate for asyncio,
it’s the presence of asyncio.sleep() in the example that is designed to mimic an IO-bound process
where there is uncertain wait time involved.

For example, the asyncio.sleep() call might represent sending and receiving not-so-random integers between two clients in a message application.
"""
import asyncio
import random

# ANSI colors
c = (
    "\033[0m",   # End of color
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
)

async def makerandom(idx: int, threshold: int = 6) -> int:
    print(c[idx + 1] + f"Initiated makerandom({idx}).")
    i = random.randint(0, 10)
    while i <= threshold:
        print(c[idx + 1] + f"makerandom({idx}) == {i} too low; retrying.")
        await asyncio.sleep(idx + 1)
        i = random.randint(0, 10)
    print(c[idx + 1] + f"---> Finished: makerandom({idx}) == {i}" + c[0])
    return i

async def main():
    res = await asyncio.gather(*(makerandom(i, 10 - i - 1) for i in range(3)))
    return res

if __name__ == "__main__":
    random.seed(444)
    r1, r2, r3 = asyncio.run(main())
    print()
    print(f"r1: {r1}, r2: {r2}, r3: {r3}")

