# 所有的unicode字符
from collections import Counter
from qa.regex_utils import *
import re

resource_path = r"D:\tmxmall-code\report\regex-learning\medicine.sample.txt"

with open(resource_path, "r", encoding="utf8") as f:
    char_stream = f.read()

char_dictionary = Counter(list(char_stream))
med_interval_exprs = list(char_dictionary.keys()) + ["\\u4e00-\\u9fff"]
med_unicodes = interval_expr_to_unicode(med_interval_exprs)
format_med_unicodes = re.sub("(?<!-)(?=\\\\u)", "\n", med_unicodes)
print(format_med_unicodes)
"""
\\u0020-\\u002c 
\\u002e-\\u005d
\\u005f-\\u007e
\\u00b0-\\u00b1

\\u0391-\\u03c9 希腊

\\u2018-\\u2019 ‘’
\\u201c-\\u201d “”
\\u2030 ‰
\\u2032 ′
\\u2103 ℃

\\u2160-\\u216b ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ
\\u2460-\\u2461 ①②
\\u3001-\\u3002 、。
\\u3009-\\u300b 〈〉《》
\\u4e00-\\u9fff CJK
\\uff01-\\uff52 全角

"""
