import requests
import warnings
import random
import string
import time
import json
import os

# 忽略 InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning # type: ignore
warnings.simplefilter('ignore', InsecureRequestWarning)

# 假设投票请求的 URL
vote_url = "https://pelian.univsport.com/tp/doings/lightUp"
# 设置参数
max_votes_per_phone = 5
total_votes = 80
rest_time_between_votes = (3, 10)  # 10-20秒
# rest_time_between_votes = (10, 20)  # 10-20秒
rest_time_after_20_votes = 60  # 10分钟
ip_change_after_votes = 5
open_id_file = 'open_ids.json'

# proxies_json = {
#     "data": [
#         { "ip": "176.105.220.74","port": "3129"},
#         { "ip": "193.138.178.6","port": "8282"},
#         { "ip": "49.51.244.112", "port": "8888" },
#     ]
# }


# available proxy list
available_proxies = [
    # '27.79.210.192:16000',#❤
    # '27.79.183.137:16000',#❤❤❤
    # '3.70.176.179:8090',#❤❤❤
    # '37.187.109.70:10111',#❤❤❤
    # '103.175.238.174:8080'#❤❤❤
]

init_proxies = available_proxies

# 读取代理列表
def random_proxy():
    global init_proxies  # 声明使用全局变量
    # init_proxies is empty
    if not init_proxies:
        # read proxy_list.json
        with open('http.txt', 'r') as file:
            init_proxies = file.read().splitlines()  # 按行读取并去除换行符
            # data = json.load(f)
            # init_proxies = data.get('data', [])  # 获取 'data' 字段中的代理列表

    proxies = init_proxies
    if not proxies:
        return None

    # proxies list filter speed min 1000
    # proxies = [proxy for proxy in proxies if proxy.get('speed', 0) < 1000]

    # if not proxies:  # 检查过滤后的代理列表是否为空
    #     return None

    proxy = random.choice(proxies)  # 随机选择一个代理
    return {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
        # 'http': f'http://{proxy.get("ip")}:{proxy.get("port")}',
        # 'https': f'http://{proxy.get("ip")}:{proxy.get("port")}'
    }

# 读取 openId
def load_open_ids():
    if os.path.exists(open_id_file):
        with open(open_id_file, 'r') as f:
            return json.load(f)
    return []

# 保存 openId
def save_open_ids(open_ids):
    with open(open_id_file, 'w') as f:
        json.dump(open_ids, f)

def cast_votes(open_id, request_id, votes):
    headers = {
        "Content-Type": "application/json",
        "requestId": request_id
    }

    proxies = {
        # 'http': 'http://brd-customer-hl_3d4f1c60-zone-residential_proxy1:o2isnte3s1h3@brd.superproxy.io:33335',
        # 'https': 'https://brd-customer-hl_3d4f1c60-zone-residential_proxy1:o2isnte3s1h3@brd.superproxy.io:33335'
    }
    # proxies = random_proxy()
    try:
        print("使用代理:", proxies)
        # response = requests.get('https://geo.brdtest.com/welcome.txt?product=resi&method=native', proxies=proxies,verify=False)
        # response = requests.get('http://cip.cc', proxies=proxies, verify=False)
        # print("响应内容:", response.text)
    except Exception as e:
        print("发生错误:", e)

    for i in range(votes):
        try:
            response = requests.post(vote_url, json={"openId": open_id,"doingsUc": "D1059561989368750080",
  "trainingPartnerUc": "1061320645223424000"}, headers=headers, proxies=proxies, verify=False, timeout=20)
            # 打印响应状态码和内容
            print(f"Vote {i + 1} response for {open_id}: {response.status_code} - {response.text}")
            if response.status_code == 200:
                # {"code":10007,"data":null,"msg":"每天最多投5票"}
                # {"code":0,"data":"成功","msg":"success"}
                code = response.json().get('code', 0)
                if code == 0:
                    print(f"Vote {i + 1} cast successfully for {open_id}")
                elif code == 10007:
                    break
            else:
                print(f"Error casting vote {i + 1} for {open_id}: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error casting vote {i + 1} for {open_id}: {e}")
#             response = requests.post(vote_url, json={"openId": open_id,"doingsUc": "D1059561989368750080",
#   "trainingPartnerUc": "1061320645223424000"}, headers=headers, verify=False)

def generate_open_id(length=28):
    # 定义可用字符，包括数字和字母
    characters = string.ascii_letters + string.digits
    # 随机选择字符并生成 openId
    open_id = ''.join(random.choice(characters) for _ in range(length))
    return open_id

def generate_request_id(prefix="03"):
    # 生成 10 位随机数字
    random_digits = ''.join(random.choices('0123456789', k=10))
    # 拼接前缀和随机数字
    return prefix + random_digits

# 模拟更换 IP 地址的函数
def change_ip():
    # 这里可以添加更换 IP 的代码
    print("更换 IP 地址！")
    #!/usr/bin/env python
    import sys
    if sys.version_info[0]==2:
        import six
        from six.moves.urllib import request
        opener = request.build_opener(
            request.ProxyHandler(
                {'http': 'http://brd-customer-hl_3d4f1c60-zone-residential_proxy1:o2isnte3s1h3@brd.superproxy.io:33335',
                'https': 'http://brd-customer-hl_3d4f1c60-zone-residential_proxy1:o2isnte3s1h3@brd.superproxy.io:33335'}))
        print(opener.open('https://geo.brdtest.com/welcome.txt?product=resi&method=native').read())
    if sys.version_info[0]==3:
        import urllib.request
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler(
                {'http': 'http://brd-customer-hl_3d4f1c60-zone-residential_proxy1:o2isnte3s1h3@brd.superproxy.io:33335',
                'https': 'http://brd-customer-hl_3d4f1c60-zone-residential_proxy1:o2isnte3s1h3@brd.superproxy.io:33335'}))
        print(opener.open('https://geo.brdtest.com/welcome.txt?product=resi&method=native').read())


def simulate_voting():
    total_cast_votes = 0
    rest_count = 0
    # 读取已有的 openId
    open_ids = load_open_ids()
    current_open_id_index = 0

    while total_cast_votes < total_votes:
        for _ in range(max_votes_per_phone):
            if total_cast_votes >= total_votes:
                break
            # 检查是否需要生成新的 openId
            if current_open_id_index >= len(open_ids):
                new_open_id = generate_open_id()
                open_ids.append(new_open_id)
                save_open_ids(open_ids)  # 保存新的 openId
                current_open_id_index = len(open_ids) - 1  # 使用新生成的 openId
            
            open_id = open_ids[current_open_id_index]
            request_id = generate_request_id()
            cast_votes(open_id, request_id, max_votes_per_phone)
            total_cast_votes += 1

            # 更新 openId 索引
            current_open_id_index += 1
            # 随机休息时间
            rest_time = random.randint(*rest_time_between_votes)
            print(f"休息 {rest_time} 秒...")
            time.sleep(rest_time)

        # 更换 IP 地址
        # change_ip()
        rest_count += 1
        if rest_count >= (20 // ip_change_after_votes):
            print("完成 10 次投票，休息 10 分钟...")
            time.sleep(rest_time_after_20_votes)
            rest_count = 0  # 重置休息计数
    print("投票结束，达到设置的上限！")

if __name__ == "__main__":
    # main()
    simulate_voting()
