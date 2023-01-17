import argparse

import module.process
import module.thread


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-mode', help='[process, thread]', type=str, required=True)
    parser.add_argument('-url', help='ex) http://google.com', type=str, required=True)
    parser.add_argument('-method', help='수행할 공격 선택 [ex) GET, POST]',
                        type=str, default='GET', required=False)
    parser.add_argument('-time', help='공격 수행할 시간', default=60, type=int, required=False)
    parser.add_argument('-data', help='POST 공격을 수행할 때 사용할 데이터 파일 경로 입력', type=str, required=False)
    parser.add_argument('-pCount', help='공격에 사용할 프로세스 개수 -mode process 와 같이 사용 (기본 50개)',
                        type=int, default=50, required=False)
    parser.add_argument('-tCount', help='공격에 사용할 스레드 개수 -mode thread 와 같이 사용 (기본 500개)',
                        type=int, default=500, required=False)

    args = parser.parse_args()

    mode = args.mode.lower()
    url = args.url
    method = args.method.lower()
    attack_time = args.time

    if (not mode == 'process') and (not mode == 'thread'):
        raise Exception('[process, thread] 중 선택해 주세요!')

    if mode == 'process':
        if method == 'get':
            module.process.run(url, method, args.pCount, attack_time)
        elif method == 'post':
            module.process.run(url, method, args.pCount, attack_time)
    else:
        if method == 'get':
            module.thread.run(url, method, args.tCount, attack_time)
        elif method == 'post':
            module.thread.run(url, method, args.pCount, attack_time)


if __name__ == '__main__':
    main()
