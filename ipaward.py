import threading
import time
import requests
#设置最大线程数
threadmax = threading.BoundedSemaphore(200)
#你要验证的网站
Verification_url = 'https://www.baidu.com/'
# main_url 用于你在其他网站买的ip的Api
main_url = ""
def get_proxy_online():
    proxys = requests.get(main_url).text
    proxy_list = proxys.strip().split("\r\n")
    print("本次获取到代理%d个开始去重..." % len(proxy_list))
    proxy_list = list(set(proxy_list))
    print("去重后获取到代理%d个开始过滤..." % len(proxy_list))
    return proxy_list


def test_ip(proxies):
    proxies = {
        "http": f"http://{proxies}",
        "https": f"http://{proxies}",
    }
    try:
        #可以将
        r = requests.get(Verification_url, proxies=proxies, timeout=4)
        if r.status_code == 200:
            print('%s验证成功' % proxies['https'].split('/')[-1])
            live_proxy_list.append(proxies)
        threadmax.release()
    except:
        print('%s验证失败' % proxies['https'].split('/')[-1])
        threadmax.release()
        pass


def check_proxy_live():
    proxy_list = get_proxy_online()
    start = time.time()
    threads = []
    for i in range(len(proxy_list)):
        thread = threading.Thread(target=test_ip, args=[proxy_list[i]])
        threads.append(thread)
        threadmax.acquire()
        thread.start()
    for thread in threads:
        thread.join()
    print('%d个过滤请求用时%f.2' % (len(proxy_list),time.time() - start))


while True:
    try:
        live_proxy_list = []
        # sleep_time 为休眠时间间隔
        sleep_time = 50
        check_proxy_live()
        with open('ip.txt', 'w+') as f:
            print('获取到可用ip %d 个' % len(live_proxy_list))
            for each in live_proxy_list:
                f.write(each['https'].split('/')[-1])
                f.write('\n')
            f.close()

        print("休息%d秒后继续运行" % sleep_time)
        time.sleep(sleep_time)
    except Exception as e:
        print(e)
        time.sleep(10)
        pass
