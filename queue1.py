import numpy as np
import os

planes = [
    "战斗机",
    "轰炸机",
    "歼击轰炸机",
    "侦察机",
    "运输机",
    "预警机",
    "反潜机",
    "空中加油机",
    "无人机",
    "武装直升机",
    "反潜直升机",
    "运输直升机",
    "电子干扰飞机",
    "教练机",
]

ships = [
    "航空母舰",
    "驱逐舰",
    "巡洋舰",
    "护卫舰",
    "潜艇",
    "两栖攻击舰",
    "濒海战斗舰",
    "两栖指挥舰",
    "补给舰",
    "船坞登陆舰",
    "导弹艇",
    "调查船",
    "水文测量船",
    "远征机动基地",
    "辅助舰艇",
    "猎雷舰",
    "登陆舰/艇",
    "巡逻艇",
    "运输舰",
    "巡防舰",
    "快艇",
    "无人舰船",
    "巡护舰",
    "搜救艇",
    "无人潜航器",
    "载人潜航器",
    "实验型舰艇",

]


class Queue():
    # def __int__(self):

    # candidates = ["https://zh.wikipedia.org/wiki/Category:%E5%86%9B%E7%94%A8%E8%88%AA%E7%A9%BA%E5%99%A8"]
    candidates = []  # 保存候选的请求列表

    # 拼接字符串
    for ship in ships:
        url = f"https://zh.wikipedia.org/wiki/Category:{ship}"
        candidates.append(url)
    for plane in planes:
        url= f"https://zh.wikipedia.org/wiki/Category:{plane}"
        candidates.append(url)

    has_viewd = []  # 保存已经被处理过的请求
    # self.max_num = max_num # 保存最多可
    save_every = 100  # has_viewd每100次执行一次保存以记录
    # 初始化时需要添加若干个入口请求
    candidates.append('https://zh.wikipedia.org/wiki/Category:%E6%88%98%E6%96%97%E6%9C%BA')

    def load_npy(self):
        if os.path.exists('../orgin_page/has_viewd.npy'):
            self.has_viewd = np.load('../orgin_page/has_viewd.npy').tolist()

    def save_has_viewd(self):
        np.save('./orgin_page/has_viewd.npy', self.has_viewd)

    def add_candidate(self, url):
        # 注意，执行该函数说明获得了一个新的请求，需要待处理（从分类或内容页面解析得到的链接）
        if url not in self.candidates and url not in self.has_viewd:
            self.candidates.append(url)

    def add_candidates(self, url_list):
        # 批量添加注意，执行该函数说明获得了一个新的请求，需要待处理（从分类或内容页面解析得到的链接）
        for url in url_list:
            self.add_candidate(url)

    def delete_candidate(self, url):
        # 注意，执行该函数时，说明有进程已经收到该请求，在处理前需要将候选列表中该请求删除，表示已有进程已经拿到该请求
        if url in self.candidates:
            self.candidates.remove(url)

    def add_has_viewd(self, url):
        # 注意，执行该函数时，说明有进程已经收到请求，并进行了相关处理，现需要更新队列状态
        if url not in self.candidates and url not in self.has_viewd:
            # 如果当前请求既不在候选列表，也不在已爬列表，则加入
            self.has_viewd.append(url)
        elif url in self.candidates and url not in self.has_viewd:
            # 如果当前请求在候选列表中，且不在已爬列表，则说明有进程提前读取该页面，但候选列表还没更新，则加入
            # 并将候选列表对应的请求删除
            self.has_viewd.append(url)
            self.delete_candidate(url)
        elif url in self.candidates and url in self.has_viewd:
            # 如果当前请求在候选列表中，也在已爬列表中，则说明有进程已经完成了爬取，但候选列表没更新，则直接
            # 删掉候选列表中指定的请求
            self.delete_candidate(url)
            # 最后一种情况是当前请求不在候选列表，但在已爬列表，而还能遇到该请求，说明该请求属于滞后请求，无视即可
