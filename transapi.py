import requests
import json
import urllib
import argparse

parser = argparse.ArgumentParser(description="transapi.py")
parser.add_argument('-f', "--file_path")
parser.add_argument("--truncate", default=1E10, type=int)

args = parser.parse_args()


class TranslateAPI(object):
    url_text = lambda \
            text: f"http://qa.tmxmall.com/v1/http/mttranslate?text={text}&user_name=1499059470@qq.com&client_id=e0c2ccfde21c5de10af7a72e53bcc273&from=zh-CN&to=en-US&de=trados"


def trans(src):
    post_url = TranslateAPI.url_text(urllib.parse.quote(src))
    r = requests.post(post_url)
    try:
        outcome = json.loads(r.text)
        tgt = outcome["mt_set"][0]["tgt"]
        print("from:", outcome["mt_set"][0]["provider"], "content:", tgt[:10], "...")
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
