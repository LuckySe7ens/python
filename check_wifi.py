# -*- coding: UTF-8 -*-
import os
import sys
import importlib,sys

importlib.reload(sys)
 
# 定义一个函数checkWIFI，获取电脑连接过的所有wifi名称和密码，结果以列表形式返回
def checkWIFI():
    # 定义一个空列表，用来存放查询结果
    list = []
 
    # 查询所有的wifi名称
    message = os.popen('netsh wlan show profiles').readlines()
    # print(message)
 
    # 获取的结果是一个列表list，需要进行遍历
    for i in message:
        # 遍历结果含有中文会乱码，需要进行gbk编码
        result = i.strip()
        # print(result)
        # print(result+"的长度为"+str(len(result))+"，数据类型为"+str(type(result)))
 
        # 检查每一个结果中是否含有指定关键字
        if result.find(u"所有用户配置文件 : ") != -1:
            # print("位置："+str(result.find(u": ")))
            # 从位置11开始截取
            # print("wifi名称:"+result[11:])
 
            # netsh wlan show profiles name="Xiaomi_216E" key=clear
            # 如果找到关键字，就截取指定位置的字符串，即wifi名称，再拼接成cmd命令
            command = 'netsh wlan show profiles name="' + result[11:] + '" key=clear'
            # print(command)
 
            # 执行拼接好的命令，获取含有密码的结果
            per_wifi = os.popen(command).readlines()
 
            # 获取的结果是一个列表list，需要进行遍历
            for j in per_wifi:
                # 遍历结果含有中文会乱码，需要进行gbk编码
                passwd = j.strip()
                # print(passwd)
 
                # 检查每一个结果中是否含有指定关键字
                if passwd.find(u"关键内容            :") != -1:
                    # 获取字符串指定位置的内容并判断是否为空
                    if passwd[18:] != '':
                        # 定义一个临时列表list_temp存放每一个wifi信息，即wifi名称和密码
                        list_temp = []
 
                        # 将wifi名称追加到列表list_temp
                        list_temp.append(result[11:])
 
                        # 将密码追加到列表list_temp
                        list_temp.append(passwd[18:])
 
                        # 将每个wifi信息作为一个整体追加到列表list
                        list.append(list_temp)
 
                        # print("wifi名称:" + result[11:])
                        # print("wifi密码:"+passwd[18:])
                        # print("")
    # 将所有的wifi信息列表list返回给调用者
    return list
 
 
print("正在查询......")
# 定义一个变量，存放调用checkWIFI的执行结果
list = checkWIFI()
print("返回结果如下：")
i = 0
# 将查询结果遍历输出
for n in list:
    i = i + 1
    print(str(i) + "、wifi名称：" + n[0] + "，密码：" + n[1])