import requests
import json
import urllib
import argparse

import hashlib
import random

parser = argparse.ArgumentParser(description="transapi4youdao.py")
parser.add_argument('-f', "--file_path")
parser.add_argument("--truncate", default=1E10, type=int)

args = parser.parse_args()


def MD5Gen(something):
    hl = hashlib.md5()
    hl.update(something.encode(encoding='utf-8'))
    return hl.hexdigest().upper()


class TranslateAPI(object):
    appKey = "53dcd3a4513360b0"
    appPassword = "pmb6OCmWH3CqUkwBunh68V357jxm2wPk"
    salt = str(random.randint(1, 65536))
    url_text = lambda \
            text: f"http://openapi.youdao.com/api?q={text}&from=zh_CHS&to=EN&appKey={appKey}&salt={salt}&sign={MD5Gen(appKey+text+salt+appPassword)}"


def trans(src):
    post_url = TranslateAPI.url_text(src)
    r = requests.post(post_url)
    print(r.text)
    try:
        outcome = re.findall("'translation': \['(.*)'\]", r.text)
        tgt = outcome["translation"]
        print("from:", "youdao", "content:", tgt[:10], "...")
        return tgt
    except Exception as e:
        print(r.text)
        return "ERROR"


if __name__ == '__main__':

    trans_result = []
    with open(args.file_path, "r", encoding="utf8") as f:
        for k, line in enumerate(f):
            if k < args.truncate:
                tgt = trans(line[:-1])
                trans_result.append(tgt)

    with open(args.file_path + ".fromapi", "w", encoding="utf8") as f:
        f.writelines(["%s\n" % x for x in trans_result])

# src = re.sub("%", "", "采用C30-HPLC-PDA-ELSD系统，参照已公布全反式异构体的吸光系数（A1%1cm=3400），根据其光谱峰面积与质量峰面积之比，估算出9，9’-顺式异构体、11，11’-顺式异构体和13，13’-顺式异构体的吸光系数分别为：2100、1819和1134。")
#