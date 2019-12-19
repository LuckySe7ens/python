#just for windows
#auto switch to available wifi
#author: Nickwong
import os
import time
import datetime
import subprocess
import tkinter
from tkinter.messagebox import showwarning

def connect_wifi(wifiProfile):
    cmd = 'netsh wlan connect name="%s"' % wifiProfile;
    return os.system(cmd)

def check_ping(ip, count = 1, timeout = 1000):
    cmd = 'ping -n %d -w %d %s > NUL' % (count,timeout,ip)
    response = os.system(cmd)
    # and then check the response...
    # 0 for ok, no 0 for failed
    return "ok" if response == 0 else "failed"

def get_current_wifi(wifiList):
    cmd = 'netsh wlan show interfaces'
    p = subprocess.Popen(cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
        )
    ret = p.stdout.read()
    for index in range(len(wifiList)):
        if ret.find(wifiList[index]) >=0 :
            return index
    return 0

def show_messagebox():
    tkMessageBox.showwarning("Title", 'Network is unstable')

def auto_switch_wifi(ipTest, wifiList):
    lastMinute = 0
    while(True):
        #sleep to save power
        time.sleep(1)
        now = datetime.datetime.now()
        #ping twice to ignore network fluctuation
        pingStatus = check_ping(ipTest,2)
        if now.minute != lastMinute:
            lastMinute = now.minute
            print(now.strftime("%Y-%m-%d %H:%M:%S"),'',pingStatus)
        if pingStatus != 'ok':
            index = get_current_wifi(wifiList)
            index = 1 - index
            print('---auto switch wifi from "%s" to "%s", waiting for 15s' % (wifiList[1-index],wifiList[index]))
            connect_wifi(wifiList[index])
            show_messagebox()
            #switch need a delay, good coffee need time to cook
            time.sleep(15)

def test():
     while(True):
        print(wifiList[get_current_wifi(wifiList)])

if __name__ == "__main__":
    #baidu.com ip
    ipTest = '61.135.169.121'
    #wifi must match blow name
    wifiList = ['spruce','wifi-58']
    connect_wifi('spruce');
#    auto_switch_wifi(ipTest,wifiList)