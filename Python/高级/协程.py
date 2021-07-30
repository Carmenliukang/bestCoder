#!/usr/bin/env python
# -*- coding: utf-8 -*-


import asyncio


async def request(url):
    print(url)
    sleep_time = int(url.split("_")[-1])
    await asyncio.sleep(sleep_time)
    print(f"OK {url}")


async def main(urls):
    for url in urls:
        await request(url)


async def main_method(urls):
    tasks = [asyncio.create_task(request(url)) for url in urls]
    for task in tasks:
        await task


async def main_method_2(urls):
    # 进一步优化代码
    tasks = [asyncio.create_task(request(url)) for url in urls]
    await asyncio.gather(*tasks)


asyncio.run(main(['url_1', 'url_2', 'url_3', 'url_4']))

asyncio.run(main_method(['url_1', 'url_2', 'url_3', 'url_4']))
asyncio.run(main_method_2(['url_1', 'url_2', 'url_3', 'url_4']))
