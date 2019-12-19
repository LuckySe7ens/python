#-*- encoding: utf-8 -*-
import logging
import wmi
import os
import win32api
import time
import socket

ProgramPath = 'C:\Program Files (x86)\Spruce-Infocube\云杉准入.exe'
ProcessName = '云杉准入.exe'
#读取配置文件中的进程名和系统路径，这2个参数都可以在配置文件中修改
ProList = []
#定义一个列表
c = wmi.WMI()

def isNetOK(testserver):
  s=socket.socket()
  s.settimeout(3)
  try:
    status = s.connect_ex(testserver)
    if status == 0:
      s.close()
      return True
    else:
      return False
  except Exception as e:
    return False
	
def connect_wifi(wifiProfile):
    cmd = 'netsh wlan connect name="%s"' % wifiProfile;
    return os.system(cmd)
 
def isNetChainOK(testserver=('www.baidu.com',443)):
  isOK = isNetOK(testserver)
  return isOK
  
def main():
    for process in c.Win32_Process():
        ProList.append(str(process.Name))
#把所有任务管理器中的进程名添加到列表
 
#    if ProcessName not in ProList:
    if isNetChainOK() is False:
        connect_wifi('spruce')
#判断进程名是否在列表中，如果是True，则所监控的服务正在 运行状态，
#打印服务正常运行
#         print('')
#        print("Server is running...")
#        print('')
#   else:
#如果进程名不在列表中，即监控的服务挂了，则在log文件下记录日志
#日志文件名是以年月日为文件名
 
        f=open('.\\log\\'+time.strftime("%Y%m%d", time.localtime())+'-exception.txt','a')
        print('net is not ok,Begining to Restart Server...')
#打印服务状态
        f.write('\n'+'net is not ok,Begining to Restart Server...'+'\n')
        f.write(time.strftime('%Y-%m-%d %H:%M:%S --%A--%c', time.localtime()) +'\n')
 #写入时间和服务状态到日志文件中
        if ProcessName in ProList:
            os.system('taskkill /IM 云杉准入.exe /F')
#            win32api.ShellExecute(0,'close','C:\Program Files (x86)\Spruce-Infocube\云杉准入.exe', '','',1)
        os.startfile(ProgramPath)
#        pid=win32api.ShellExecute(0,'open',ProgramPath, '','',1)
#		win32api.ShellExecute(0,'open',ProgramPath,	'','',1)
		#调用服务重启
        f.write('Restart Server Success...'+'\n')
        f.write(time.strftime('%Y-%m-%d %H:%M:%S --%A--%c', time.localtime()))
        f.close()
#关闭文件
        print('Restart Server Success...')
        print(time.strftime('%Y-%m-%d %H:%M:%S --%A--%c', time.localtime()))
    del ProList[:] 
#清空列表，否则列表会不停的添加进程名，会占用系统资源
     
if __name__=="__main__" : 
    while True: 
        main() 
        time.sleep(10)