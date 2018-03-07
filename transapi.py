import requests
import json

url_text = lambda text: f"http://qa.tmxmall.com/v1/http/mttranslate?text={text}&user_name=1499059470@qq.com&client_id=e0c2ccfde21c5de10af7a72e53bcc273&from=zh-CN&to=en-US&de=trados"

src = "我爱北京天安门100"
r = requests.post(url_text(src))
try:
    tgt = json.loads(r.text)["mt_set"][0]["tgt"]
except Exception as e:
    print(r.text)



