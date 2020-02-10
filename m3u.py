# -*- coding: UTF-8 -*-

import os
f = open('4hu.csv', 'r', encoding='utf-8')
w = open('4hu.m3u', 'a', encoding='utf-8')
w.write('#EXTM3U\n')
line = f.readline()
line = line[:-1]
while line:
    content = line.split(',')
    w.write('#EXTINF:-1 tvg-id="" tvg-name="" tvg-logo="' + content[3] + '" group-title="'
            + content[1] + '",' + content[2] + "\n")
    w.write(content[4] + '\n')
    line = f.readline()
    line = line[:-1]
    content = line.split(',')
w.close()
f.close()
