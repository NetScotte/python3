import asyncio


async def crawl_page(url):
    print(f"crawling {url}")
    sleep_time = int(url.split('_')[-1])
    # 等待事件
    await asyncio.sleep(sleep_time)
    print(f'OK {url}')


async def main(urls):
    # 通过asyncio.create_task()创建任务，任务创建后很快就会被调度执行
    tasks = [asyncio.create_task(crawl_page(url)) for url in urls]
    # 取消任务
    tasks[1].cancel()
    # 等待所有任务结束，捕获异常
    await asyncio.gather(*tasks, return_exceptions=True)


# 程序进入main()函数，事件循环开启，事件循环会检测所有任务，当任务完成时会通知事件循环，事件循环会在合适的时候调度任务从await处继续执行
asyncio.run(main(["url_1", "url_2", "url_3"]))
