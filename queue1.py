import numpy as np
import os


class Queue():
    # def __int__(self):

    # candidates = ["https://zh.wikipedia.org/wiki/Category:%E5%86%9B%E7%94%A8%E8%88%AA%E7%A9%BA%E5%99%A8"]

    candidates = ["https://zh.wikipedia.org/wiki/Category:%E6%88%98%E6%96%97%E6%9C%BA",
                  "https://zh.wikipedia.org/wiki/Category:%E7%9B%B4%E5%8D%87%E6%9C%BA",
                  "https://zh.wikipedia.org/wiki/Category:%E8%BF%90%E8%BE%93%E6%9C%BA",
                  "https://zh.wikipedia.org/wiki/Category:%E5%86%9B%E7%94%A8%E8%BF%90%E8%BE%93%E6%9C%BA",
                  "https://zh.wikipedia.org/wiki/Category:%E8%BD%B0%E7%82%B8%E6%9C%BA",
                  "https://zh.wikipedia.org/wiki/Category:%E5%86%9B%E7%94%A8%E9%A3%9E%E6%9C%BA",
                  "https://zh.wikipedia.org/wiki/Category:%E6%97%A0%E4%BA%BA%E6%9C%BA",
                  "https://zh.wikipedia.org/wiki/Category:%E7%A9%BA%E4%B8%AD%E5%8A%A0%E6%B2%B9%E6%A9%9F",
                  "https://zh.wikipedia.org/wiki/Category:%E6%B0%B4%E4%B8%8A%E9%A3%9B%E6%A9%9F"
                  "https://zh.wikipedia.org/wiki/Category:%E5%81%B5%E5%AF%9F%E6%A9%9F",
                  "https://zh.wikipedia.org/wiki/Category:%E5%86%9B%E7%94%A8%E8%88%AA%E7%A9%BA%E5%99%A8%E7%B1%BB%E5%9E%8B",
                  "https://zh.wikipedia.org/wiki/Category:%E5%86%9B%E7%94%A8%E8%88%AA%E7%A9%BA%E5%99%A8",
                  ] # 保存候选的请求列表

    has_viewd = [] # 保存已经被处理过的请求
    # self.max_num = max_num # 保存最多可
    save_every = 100 # has_viewd每100次执行一次保存以记录
    # 初始化时需要添加若干个入口请求
    candidates.append('https://zh.wikipedia.org/wiki/Category:%E6%88%98%E6%96%97%E6%9C%BA')

    def load_npy(self):
        if os.path.exists('../orgin_page/has_viewd.npy'):
            self.has_viewd = np.load('../orgin_page/has_viewd.npy').tolist()

    def save_has_viewd(self):
        np.save('./orgin_page/has_viewd.npy',self.has_viewd)

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

