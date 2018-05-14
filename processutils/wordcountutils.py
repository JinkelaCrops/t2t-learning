import re

space_symbol = "\\u0020\\u00a0\\u202f\\u205f\\u3000\\u303f\\ufeff\\u2000-\\u200b"
control_symbol = "\\u0001-\\u001f"


def word_count(sentence):
    zh = "[\\u4e00-\\u9fff]"
    zh_sp = zh.replace("]", space_symbol + control_symbol + "]")
    non_zh_sp = zh_sp.replace("[", "[^")
    en_regex = "(?<=%s)%s+(?=%s|$)|^%s+(?=%s|$)" % (zh_sp, non_zh_sp, zh_sp, non_zh_sp, zh_sp)
    zh_regex = zh
    words = re.findall(en_regex, sentence) + re.findall(zh_regex, sentence)
    return len(words)
