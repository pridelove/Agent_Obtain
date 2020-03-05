import threading
import time
import re
import requests
#你要验证的网站
Verification_url = 'https://www.baidu.com/'
# http://www.xiladaili.com   可用数量百位数
def xiladaili_ip():
    ipList = []
    for page_num in range(1, 50):
        url = "http://www.xiladaili.com/gaoni/%d/" % page_num
        response = requests.get(url)
        r = response.text
        patter = re.compile(
            r'(?:(?:[0-1]{0,1}\d{0,1}\d|[2][0-4]\d|[2][5][0-5])\.){3}(?:[0-1]{0,1}\d{0,1}\d|[2][0-4]\d|[2][5][0-5]):(?:\d){1,5}')
        temp_ip = patter.findall(r)
        # 把每页的ip压入列表ipList
        for ip in temp_ip:
            print(ip)
            ipList.append(ip)
        time.sleep(0.2)
        # 去重
    # ipList = list(set(ipList))
    return ipList


# http://www.89ip.cn/index_1.html  可用数量十位数
def ip89():
    ip89List = []
    for page_num in range(1, 20):
        url = "http://www.89ip.cn/index_" + str(page_num) + ".html"
        response = requests.get(url)
        r = response.text
        patter = re.compile(
            r'((?:(?:[0-1]{0,1}\d{0,1}\d|[2][0-4]\d|[2][5][0-5])\.){3}(?:[0-1]{0,1}\d{0,1}\d|[2][0-4]\d|[2][5][0-5]))\s+</td>\s+<td>\s+((?:\d){1,5})')
        temp_ip = patter.findall(r)
        # 把每页的ip压入列表ipList
        for ip in temp_ip:
            print(ip[0] + ':' + ip[1])
            ip89List.append(ip[0] + ':' + ip[1])
        time.sleep(0.2)
    return ip89List


# http://www.ip3366.net/?stype=1&page=1  可用数量个位数
def ip3366():
    ip3366List = []
    for page_num in range(1, 11):
        url = "http://www.ip3366.net/?stype=1&page=" + str(page_num)
        response = requests.get(url)
        r = response.text
        patter = re.compile(
            r'((?:(?:[0-1]{0,1}\d{0,1}\d|[2][0-4]\d|[2][5][0-5])\.){3}(?:[0-1]{0,1}\d{0,1}\d|[2][0-4]\d|[2][5][0-5]))</td>\s+<td>((?:\d){1,5})')
        temp_ip = patter.findall(r)
        # 把每页的ip压入列表ipList
        for ip in temp_ip:
            print(ip[0] + ':' + ip[1])
            ip3366List.append(ip[0] + ':' + ip[1])
        time.sleep(0.2)
    return ip3366List


# https://www.kuaidaili.com/free/    可用数量个位数
def kuaidaili():
    kuaidaili_List = []
    for page_num in range(1, 10):
        url = "https://www.kuaidaili.com/free/inha/" + str(page_num) + "/"
        response = requests.get(url)
        r = response.text
        patter = re.compile(
            r'((?:(?:[0-1]{0,1}\d{0,1}\d|[2][0-4]\d|[2][5][0-5])\.){3}(?:[0-1]{0,1}\d{0,1}\d|[2][0-4]\d|[2][5][0-5]))</td>\s+<td data-title="PORT">((?:\d){1,5})')
        temp_ip = patter.findall(r)
        # 把每页的ip压入列表ipList
        for ip in temp_ip:
            print(ip[0] + ':' + ip[1])
            kuaidaili_List.append(ip[0] + ':' + ip[1])
        time.sleep(0.2)
    return kuaidaili_List


# http://www.nimadaili.com/gaoni/
def nimadaili_ip():
    ipList = []
    for page_num in range(1, 40):
        url = "http://www.nimadaili.com/gaoni/%d/" % page_num
        response = requests.get(url)
        r = response.text
        patter = re.compile(
            r'(?:(?:[0-1]{0,1}\d{0,1}\d|[2][0-4]\d|[2][5][0-5])\.){3}(?:[0-1]{0,1}\d{0,1}\d|[2][0-4]\d|[2][5][0-5]):(?:\d){1,5}')
        temp_ip = patter.findall(r)
        # 把每页的ip压入列表ipList
        for ip in temp_ip:
            print(ip)
            ipList.append(ip)
        time.sleep(0.2)
        # 去重
    # ipList = list(set(ipList))
    return ipList


# 收集和提取ip
def collect_ip():
    SumipList = []
    tempipList = xiladaili_ip()
    for ip in tempipList:
        SumipList.append(ip)
    tempipList = ip89()
    for ip in tempipList:
        SumipList.append(ip)
    tempipList = ip3366()
    for ip in tempipList:
        SumipList.append(ip)
    tempipList = kuaidaili()
    for ip in tempipList:
        SumipList.append(ip)
    tempipList = nimadaili_ip()
    for ip in tempipList:
        SumipList.append(ip)
    return SumipList


# 代理验证
def test_ip(proxies):
    proxies = {
        "http": f"http://{proxies}",
        "https": f"http://{proxies}",
    }
    try:
        r = requests.get(Verification_url, proxies=proxies, timeout=8)
        if r.status_code == 200:
            print('%s验证成功' % proxies['https'].split('/')[-1])
            live_proxy_list.append(proxies)
    except:
        print('%s验证失败' % proxies['https'].split('/')[-1])
        pass


# 主函数
if __name__ == "__main__":
    while True:
        try:
            print("开始获取代理ip列表...")
            live_proxy_list = []
            proxy_list = collect_ip()
            print("一共获取到%d个ip,开始去重..." % len(proxy_list))
            # proxy代理去重
            proxy_list = list(set(proxy_list))
            print("去重后还剩%d个ip,开始验证..." % len(proxy_list))
            time.sleep(3)
            threads = []
            for i in range(len(proxy_list)):
                thread = threading.Thread(target=test_ip, args=[proxy_list[i]])
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()
            print('本次获取到的ip %d 个,可用ip %d 个' % (len(proxy_list), len(live_proxy_list)))
            with open('ip.txt', 'w+') as f:
                for each in live_proxy_list:
                    f.write(each['https'].split('/')[-1])
                    f.write('\n')
                    f.flush()
            time.sleep(600)
        except Exception as e:
            print("异常了:", e)
