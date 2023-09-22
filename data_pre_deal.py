# -*- coding: UTF-8 -*-
import ast
import json
import os
from langconv import Converter
import argparse
# @Project ：counselor 
# @File    ：data_pre_deal.py
# @IDE     ：PyCharm 
# @Author  ：liguochun0304@163.com
# @Date    ：2023/9/22 9:41


parser = argparse.ArgumentParser(description='传入参数')
parser.add_argument("--input_path",type=str,default="./spirder_data")
parser.add_argument("--output_path",type=str,default="./output_data")
args = parser.parse_args()


def joint_text(contents):
    """
    拼接正文中的字符串
    :param contents:
    :return:
    """
    contents = eval(contents)
    text = ""
    for content in contents:
        text = text + content
    return text
# 读取文件夹中的全部文件名
files= os.listdir(args.input_path)


def convert(text, flag=1):
    """
    text为要转换的文本，flag=0代表简化繁，flag=1代表繁化简
    :param text:
    :param flag:
    :return:
    """
    rule = 'zh-hans' if flag else 'zh-hant'
    return Converter(rule).convert(text)
def txt_to_json(input_path,output_path):
    """
    将从维基百科中爬取下来的词条先进行简单的预处理，删除重复的词条，并且将txt转换成json文件
    :param input_path:
    :param output_path:
    :return:
    """

    fail_files=[]
    for file in files:
        """遍历每一个文件"""
        # 打开文件
        with open(f"{input_path}/{file}", "r", encoding="utf=8") as fs:
            datas = fs.readlines()

        plane_list = []
        for data in datas:
            # 去除换行符
            data = data.strip()
            plane_list.append(data)

        if not os.path.exists(f"{output_path}/{file}.json"):
            # 将数据转换成字典的格式
            try:
                plane = {}
                plane["标题"] = plane_list[1]
                plane["类别"] = plane_list[2].split("：",1)[1]
                plane["原文地址"] = plane_list[3].split("：",1)[1]
                plane["爬取时间"] = plane_list[4].split("：",1)[1]
                plane["全文内容"] = plane_list[6]

                contents=plane["全文内容"]
                contents = eval(contents)
                text = ""
                for content in contents:
                    text = text + content
                text = convert(text)

                plane["全文内容"] = text

                # 数据持久化存储
                with open(f"./{output_path}/{plane['标题']}.jsonl","w",encoding="utf-8") as f:
                    f.write(json.dumps(plane,ensure_ascii=False ,indent =3))
            except IndexError:
                fail_files.append(file)



    count = len(os.listdir(output_path))
    print(f"{fail_files}存储失败。")
    print(f"数据预处理完成，一共爬取到了{count}条维基百科的词条。")


if __name__ == '__main__':
    txt_to_json(args.input_path,args.output_path)