# encoding:utf-8
import asyncio
from aiohttp import ClientSession
from ip import ip_main
from ip import getheaders

# 可根据自己电脑更改位置
link_path = ".\\momo_link.txt"


# 读取文件获取文件内容
def readfile():
    with open('ip.txt', 'r', encoding='utf-8') as file:
        ips = file.readlines()
    return ips


# 读取文件获取momo链接
def share_Link():
    import sys
    import os

    # 判断文件是否存在，不存在则创建
    if os.path.isfile(link_path):
        fileopen = open(link_path, 'r', encoding='utf-8')
        momo_share_link = fileopen.readline()
        # 判断是否有链接 无则终止程序
        if momo_share_link == '':
            fileopen.close()
            sys.exit()
        fileopen.close()
        return momo_share_link.strip()
    else:
        os.close(os.open(link_path, os.O_CREAT))  # 创建文件
        sys.exit()  # 终止程序


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# 实例化请求对象
async def create_aiohttp(url, proxy_list):
    header = await getheaders()  # 设置请求头
    global n
    n = 0
    async with ClientSession() as session:  # 实例化一个请求对象
        sem = asyncio.Semaphore(80)  # 设置限制并发次数
        # 生成任务列表
        task = [web_request(url=url, header=header, proxy=proxy, sem=sem, session=session) for proxy in proxy_list]
        await asyncio.wait(task)


# 网页访问
async def web_request(url, header, proxy, sem, session):
    async with sem:  # 限制并发次数
        # await asyncio.sleep(1)
        try:
            async with await session.get(url=url, headers=header, proxy=proxy,
                                         timeout=10) as response:  # 异步请求
                page_source = await response.text()  # 返回字符串形式的相应数据
                await page(page_source)
                # 请求 和 响应时要加上阻塞 await
        except Exception as e:
            print("网页请求失败! ", e)


global n  # 记录访问成功次数


# 判断访问是否成功
async def page(page_source):
    global n
    if "墨墨" in page_source:
        n += 1
        print('访问成功!!!')
    else:
        print('访问失败! 页面无此元素。')


def main():
    link = share_Link()  # 读取文件里的墨墨分享链接
    print("访问链接:", link)
    ip_main()  # 抓取代理
    proxies = [i.strip() for i in readfile()]  # 生成代理列表
    asyncio.run(create_aiohttp(link, proxies))  # 异步访问
    print("任务完成!!!")

    # 呈现程序运行结果。可根据自己电脑更改位置
    reminder_path = f'.\\访问成功{n}次.txt'
    # 创建运行结果提示文件
    with open(reminder_path, 'w', encoding='utf-8') as f:
        f.close()


if __name__ == '__main__':
    main()
