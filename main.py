from queue import Queue
from threading import Thread
import requests
import json

api = ""
url = ""
threads = 10  # 线程数
librarys = 500  # 媒体库数

base_url = url + "/Library/VirtualFolders/{0}?api_key=" + api


"""
获取媒体库
"""


def query(limit=50):
    url = base_url.format("Query")
    if limit != None:
        url += f"&Limit={limit}"
    request = requests.get(url)

    if request.status_code != 204 and request.status_code != 200:
        return False, "🤕Emby 服务器连接失败!"
    return True, request.json()


"""
删除媒体库
"""


def refreshLibrary(refreshLibrary=True, itemId=None):
    url = base_url.format("")
    url += f"&refreshLibrary={refreshLibrary}&id={itemId}"
    if itemId is None or itemId == "":
        return False, "🤕空的ID"

    request = requests.delete(url)

    # if request.status_code != 204 and request.status_code != 200:
    #     return False, "🤕Emby 服务器连接失败!"
    return True, f"Success >> {request.status_code}"


def work(inQueue):
    while not inQueue.empty():
        item = inQueue.get()
        print(item["Name"], item["ItemId"], refreshLibrary(itemId=item["ItemId"]))
        inQueue.task_done()


if __name__ == "__main__":
    inQueue = Queue()

    #  获取媒体库
    success, query = query(librarys)  # 发包获取
    if not success:
        exit(query)
    # with open("Query.json") as fp:  # 本地获取
    #     query = json.load(fp)

    # 遍历
    for i in query["Items"]:
        if i["Name"] != "相机上传":
            continue
        inQueue.put(i)

    for i in range(threads):
        thread = Thread(target=work, args=(inQueue,))
        thread.daemon = True  # 随主线程退出而退出
        thread.start()

    inQueue.join()
