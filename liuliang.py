import psutil
import time
def get_key():
    keys = psutil.net_io_counters(pernic=True).keys()
    # print(keys)
    # print(keys)
    recv = {}
    sent = {}
    for key in keys:
        recv.setdefault(key,psutil.net_io_counters(pernic=True).get(key).bytes_recv)
        sent.setdefault(key,psutil.net_io_counters(pernic=True).get(key).bytes_sent)
    # print(keys)
    # print(recv)
    # print(sent)
    return keys,recv,sent

def get_rate(func):
    keys, old_recv, old_sent = func()
    time.sleep(5)
    keys, now_recv, now_sent = func()
    # print('111')
    net_in = {}
    net_out = {}
    for key in keys:
        net_in.setdefault(key,(now_recv.get(key) - old_recv.get(key))/1024)
        net_out.setdefault(key,(now_sent.get(key) - old_sent.get(key))/1024)
    # print(keys)
    # print(net_in)
    # print(net_out)
    return keys,net_in,net_out

def main():

    while True:
        try:
            keys,net_in,net_out  = get_rate(get_key)
            sxll = 0
            xxll = 0
            for key in keys:
                # print('{0}:上行流量为{1}kb/s，下行流量为{2}kb/s，总流量为{3}kb/s'.format(key,net_out.get(key),net_in.get(key),(net_in.get(key)+net_out.get(key))))
                sxll += net_out.get(key)
                xxll += net_in.get(key)
            print('5s上行流量总和：{0}kb/s,5s下行流量总和：{1}kb/s,5s总流量：{2}kb/s'.format(sxll,xxll,(sxll+xxll)))
            return sxll,xxll,(sxll+xxll)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
