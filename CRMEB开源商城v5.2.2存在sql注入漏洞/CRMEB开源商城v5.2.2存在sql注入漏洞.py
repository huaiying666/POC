import requests

def check_vulnerability(url):
    # 如果URL以斜杠结尾，则去掉末尾的斜杠
    if url.endswith('/'):
        url = url[:-1]
    
    # 构造需要检测的URL，使用特定的API端点
    test_url = f"{url}/api/products?limit=20&priceOrder=&salesOrder=&selectId=)"
    
    try:
        # 发送GET请求获取响应
        response = requests.get(test_url)
        
        # 检查响应内容是否包含指示漏洞的特定字符串
        if 'PDOConnection.php' in response.text:
            print(f"\033[31m[HIGH RISK]\033[0m Vulnerability found in: {url}")
        else:
            print(f"\033[32m[SAFE]\033[0m No vulnerability found in: {url}")
    
    except requests.RequestException as e:
        # 处理请求异常，无法连接到URL
        print(f"\033[33m[ERROR]\033[0m Could not connect to {url}. Error: {e}")

def main():
    # 从url.txt文件中读取URL列表
    with open('url.txt', 'r') as file:
        urls = file.readlines()

    # 遍历每个URL并检测漏洞
    for url in urls:
        url = url.strip()  # 去除URL中的前导和尾随空白字符
        if not url.startswith('http'):
            url = 'http://' + url  # 如果URL缺少HTTP协议前缀，则添加

        check_vulnerability(url)

if __name__ == "__main__":
    main()
