from urllib.request import urlopen, Request
import requests
import base64
import time
import json

huobi_url = 'https://api.hbdm.com/linear-swap-ex/market/detail/batch_merged'
github_url='https://api.github.com/repos/sunaidream/sunaidream.github.io/contents/json_file2.json'
github_token1 = '2ba5efdd67cc6633'
github_token2 = '091e0f2b696b6e205018a2a2'
github_token = github_token1+github_token2
headers = {'Authorization': 'token ' + github_token,'Accept': 'application/vnd.github.v3+json'}

login_pre = requests.get(github_url, headers=headers)
github_sha = login_pre.json()['sha']

while True:
    try:
        time_begain = time.perf_counter()
        huobi_content = urlopen(url=huobi_url, timeout=15).read()
        huobi_eos = huobi_content.decode('utf-8')
        huobi_eos = json.loads(huobi_eos)
        i=0
        while i<len(huobi_eos['ticks']):
            if huobi_eos['ticks'][i]["contract_code"]=="EOS-USDT":
                eos_value=i
            i=i+1
        huobi_content = base64.b64encode(huobi_content)
        github_content = huobi_content.decode('utf-8')
        json_send= {"message": "message","sha": github_sha,"content":github_content}
        login = requests.put(github_url, headers=headers,json=json_send)
        github_sha = login.json()['content']['sha']
        time_end = time.perf_counter()
        time_run =time_end-time_begain    
        time_db = time.perf_counter()
        if time_run<2:
            time.sleep(2-time_run)
        time_de = time.perf_counter()
        time_wait=time_de-time_db
        print("\rEOS价格 %s 运行时长 %f  等待时长 %f" % (huobi_eos['ticks'][eos_value]["close"],time_run,time_wait),end="")
    except:
        continue
