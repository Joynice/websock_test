# encoding:utf-8
# !/usr/bin/env python
import psutil
import time
from liuliang import main
import datetime
from threading import Lock
from flask import Flask, render_template
from flask_socketio import SocketIO


async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

#网络
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

def xx(keys,old_recv,old_sent,now_recv,now_sent):
    net_in = {}
    net_out = {}
    for key in keys:
        net_in.setdefault(key, (now_recv.get(key) - old_recv.get(key)) / 1024)
        net_out.setdefault(key, (now_sent.get(key) - old_sent.get(key)) / 1024)
    sxll = 0
    xxll = 0
    for key in keys:
        # print('{0}:上行流量为{1}kb/s，下行流量为{2}kb/s，总流量为{3}kb/s'.format(key,net_out.get(key),net_in.get(key),(net_in.get(key)+net_out.get(key))))
        sxll += net_out.get(key)
        xxll += net_in.get(key)
    print('5s上行流量总和：{0}kb/s,5s下行流量总和：{1}kb/s,5s总流量：{2}kb/s'.format(sxll, xxll, (sxll + xxll)))
    return sxll, xxll, (sxll + xxll)
# 后台线程 产生数据，即刻推送至前端
def background_thread():
    count = 0
    while True:
        keys, old_recv, old_sent = get_key()
        socketio.sleep(5)
        keys, now_recv, now_sent = get_key()
        net_in, net_out, net_all = xx( keys, old_recv, old_sent,now_recv, now_sent)
        print(net_in, net_out, net_all)

        count += 1
        t = time.strftime('%Y-%m-%d %H:%M:%S')
        # 获取系统时间（只取分:秒）
        cpus = psutil.cpu_percent(interval=None, percpu=True)
        process = psutil.virtual_memory().percent
        # 获取系统cpu使用率 non-blocking

        socketio.emit('server_response',
                      {'data': [t, cpus, process, net_in/5, net_out/5, net_all/5], 'count': count},
                      namespace='/test')
        # 注意：这里不需要客户端连接的上下文，默认 broadcast = True


@app.route('/')
def index():
    return render_template('test.html', async_mode=socketio.async_mode)


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


if __name__ == '__main__':
    socketio.run(app, debug=True)
