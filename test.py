import psutil
import time
import  platform
# while True:
#     time.sleep(5)
#     a = psutil.disk_io_counters()
# # print(type(a))
#     print(a)
# # b = psutil.disk_partitions()
# # print(b)
#
#     c = psutil.disk_usage('/').percent
#     print(c)
# sdiskusage(total=42273669120, used=17241096192, free=22885195776, percent=40.8)
#!/usr/bin/env python

# import os
# hd={}
# disk = os.statvfs("/")
# hd['available'] = disk.f_bsize * disk.f_bavail
# hd['capacity'] = disk.f_bsize * disk.f_blocks
# hd['used'] = disk.f_bsize * disk.f_bfree
# print(hd)
#     # return hd

# while True:
#     time.sleep(2)
#     process = psutil.virtual_memory().percent
#     cpus = psutil.cpu_percent(interval=None, percpu=True)
#     disk = psutil.disk_partitions()
#     # print(process,cpus)
#     print(disk)
# # def disk_stat():
#     import os
#     hd = {}
#     disk = os.statvfs('/usr')
#     percent = (disk.f_blocks - disk.f_bfree) * 100 / (disk.f_blocks - disk.f_bfree + disk.f_bavail) + 1
#     return percent
#
#
# print (disk_stat())
# disk  = psutil.disk_partitions()
# print(disk)
# disk = psutil.disk_partitions()
# print(disk)
# while True:
#     time.sleep(1)
#     # partition = psutil.disk_usage('/')
#     #
#     # print (partition)
#     a = psutil.disk_partitions(all=False)
#     disk = psutil.disk_usage('h:\\')
#     print(a)
#     print(disk)
# io = psutil.disk_io_counters()
# print (io)
# import subprocess32
# def process(path):
#     # 指定单位 -BK -BM -BG
#     df = subprocess32.Popen(['df', '-BG', path], stdout=subprocess.PIPE)
#     output = df.communicate()[0]
#     print (output)
# process()
#     device, size, used, available, percent, mountpoint = /
#     output.split('/n')[1].split()
#     print 'device: ', device
#     print 'seize: ', size
#     print 'used: ', used
#     print 'available: ', available
#     print 'percent: ', percent
#     print 'mountpoint: ', mountpointdef main():
#     path = '/dev/sda1'
# process(path)if __name__ == '__main__':
# main()
# coding:utf-8
__author__ = 'chenhuachao'
# --------------------------------
# Created by chenhuachao  on 2015/12/23.
# ---------------------------------
import wmi
import time
import platform


def get_network_flow(os):
    '''监控window平台下网卡的实时的流量信息
    通过当前总流量和一秒后的总流量的差值，来统计实时的网卡流量信息;
    返回的流量单位是KB
    '''
    if os == "Windows":
        c = wmi.WMI()
        for interfacePerTcp in c.Win32_PerfRawData_Tcpip_TCPv4():
            sentflow = float(interfacePerTcp.SegmentsSentPersec)  # 已发送的流量
            receivedflow = float(interfacePerTcp.SegmentsReceivedPersec)  # 接收的流量
            present_flow = sentflow + receivedflow  # 算出当前的总流量
        time.sleep(1)
        for interfacePerTcp in c.Win32_PerfRawData_Tcpip_TCPv4():
            sentflow = float(interfacePerTcp.SegmentsSentPersec)  # 已发送的流量
            receivedflow = float(interfacePerTcp.SegmentsReceivedPersec)  # 接收的流量
            per_last_present_flow = sentflow + receivedflow  # 算出1秒后当前的总流量
        present_network_flow = (per_last_present_flow - present_flow) / 1024
        print("当前流量为：{0}KB".format("%.2f" % present_network_flow))
        return "%.2f" % present_network_flow


if __name__ == "__main__":
    os = platform.system()
    while 1:
        flow = get_network_flow(os)
        print("{0}KB".format(flow))