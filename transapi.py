import requests
import json
import urllib


class TranslateAPI(object):
    url_text = lambda \
        text: f"http://qa.tmxmall.com/v1/http/mttranslate?text={text}&user_name=1499059470@qq.com&client_id=e0c2ccfde21c5de10af7a72e53bcc273&from=zh-CN&to=en-US&de=trados"


def trans(src):
    post_url = TranslateAPI.url_text(urllib.parse.quote(src))
    r = requests.post(post_url)
    try:
        outcome = json.loads(r.text)
        tgt = outcome["mt_set"][0]["tgt"]
        print(outcome["mt_set"][0]["provider"])
        return tgt
    except Exception as e:
        print(r.text)

if __name__ == '__main__':
    trans("动物在注入LPS后 (2 0 5± 1 0 5 )h ,氧合指数 (PaO2 /FIO2 )≤ 30 0。 此时为ALI,肺组织学可见肺泡水肿 ,肺泡壁淤血 ,肺泡内可见中性粒细胞浸润。")
