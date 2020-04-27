#!/usr/bin/env python

import nmap
import pymongo
import csv
import time
scan_range = '192.168.1.1/24'  #扫描目标
scan_ports = '22,23,53,80,443,445,3306'  #端口多个端口逗号隔开，范围用‘-’分隔

nm = nmap.PortScanner()
nm.scan(scan_range, scan_ports)


# print result as CSV
f = nm.csv()
print(f)

#写入csv文件
#引入时间命名文件
fr = f.replace(";",",")    #转为csv的格式    用‘，’替换‘;’

now = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
fname = now+r"report.csv"

st = open(fname, "w")
st.write(fr)
st.close()

#csv文件转字典格式数据存入数据库
with open(fname,'r',encoding='utf-8')as csvfile:
    reader=csv.DictReader(csvfile)
    counts=0
    for each in reader:
        each['host']=(each['host'])
        each['hostname']=str(each['hostname'])
        each['hostname_type']=str(each['hostname_type'])
        each['protocol']=str(each['protocol'])
        each['port']=str(each['port'])
        each['name']=str(each['name'])
        each['state']=str(each['state'])
        each['product'] = str(each['product'])
        each['extrainfo'] = str(each['extrainfo'])
        each['reason'] = str(each['reason'])
        each['version'] = str(each['conf'])
        each['conf'] = str(each['conf'])
        each['cpe'] = str(each['cpe'] )
# 连接数据库写入数据
        client = pymongo.MongoClient(host='localhost', port=27017)  
        db = client.nmapy 
        set = db.scanre  
        set.insert_one(each)

        counts+=1
    print('成功添加了'+str(counts)+'条数据 ')



