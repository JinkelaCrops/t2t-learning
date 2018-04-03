# 所有的unicode字符
from collections import Counter
from qa.regex_utils import *
import re

resource_path = r"D:\tmxmall-code\report\regex-learning\medicine.sample.txt"

with open(resource_path, "r", encoding="utf8") as f:
    char_stream = f.read()

char_dictionary = Counter(list(char_stream))
med_unicodes = expr_converter("[[%s]]" % "".join(char_dictionary.keys()).replace("\n", "") + "#[[\\u4e00-\\u9fff]]")
format_med_unicodes = re.sub("(?<!-)(?=\\\\u)", "\n", med_unicodes)
print(format_med_unicodes)

lines = char_stream.split("\n")

unknown_char = "[^\\u0020-\\u007e\\u4e00-\\u9fff]"


def regex_filter_line(regex, lines):
    filter_sentence = list(filter(lambda x: re.search(regex, x) is not None, lines))
    print(regex, len(filter_sentence))
    return len(filter_sentence)


regex_filter_line("[\\u00a0-\\u00ff]", lines)

"""
\\u0020-\\u007e Latin
\\u00a0-\\u00ff Latin ++

\\u0100-\\u01ff Latin ++

\\u0251 ɑ
\\u025b ɛ
\\u0261 ɡ
\\u028a ʊ
\\u02c6-\\u02cb ˆˇˈˉˊˋ
\\u02d0 ː
\\u02d8-\\u02da ˘˙˚
\\u02dc ˜

\\u037a ͺ
\\u037e ;
\\u038a Ί
\\u038c Ό
\\u03cb ϋ
\\u03d6 ϖ
\\u0384-\\u0385 ΄΅
\\u0387-\\u0388 ·Έ
\\u038e-\\u038f ΎΏ

\\u0391-\\u03c9 希腊

\\u0400-\\u04ff 西里尔

\\u0590-\\u05ff 希伯来

\\u0652 阿拉伯

\\u11bc 朝鲜

\\u1868 ᡨ 蒙古

\\u1d31 ᴱ
\\u1d52 ᵒ
\\u1d5b ᵛ

\\u1ef7 ỷ Latin ++

\\u2016-\\u206a punc++
\\u2070 ⁰
\\u2074-\\u2075 ⁴⁵
\\u2077-\\u2078 ⁷⁸
\\u2082-\\u2084 ₂₃₄
\\u20ac €

\\u2103 ℃
\\u2105 ℅
\\u2109 ℉
\\u2116 №
\\u2122 ™
\\u212b Å
\\u2160-\\u216b ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ
\\u2170-\\u2179 ⅰⅱⅲⅳⅴⅵⅶⅷⅸ
\\u21d2 ⇒
\\u2190-\\u2193 ←↑→↓

\\u2206 ∆
\\u2208 ∈
\\u2211-\\u2212 ∑−
\\u2217-\\u221a ∗∘∙√
\\u221d-\\u2220 ∝∞∟∠
\\u2223 ∣
\\u2225 ∥
\\u2227-\\u222b ∧∨∩∪∫
\\u222e ∮
\\u2234 ∴
\\u2237 ∷
\\u223c-\\u223d ∼∽
\\u2245 ≅
\\u224c ≌
\\u2252 ≒
\\u2260-\\u2261 ≠≡
\\u2264-\\u2267 ≤≥≦≧
\\u226f ≯
\\u2295 ⊕
\\u2299 ⊙
\\u22a5 ⊥
\\u22bf ⊿

\\u2312 ⌒
\\u2395 ⎕

\\u2460-\\u2473 ①②③④⑤⑥⑦⑧⑨⑩ ⑳
\\u2474-\\u2487 ⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽ ⒇
\\u2488-\\u249b ⒈⒉⒊⒋⒌⒍⒎⒏⒐⒑ ⒛

\\u2500-\\u257f ─━│┃┄┅┆┇┈┉┊
\\u25a0-\\u25a1 ■□
\\u25b2-\\u25b4 ▲△▴
\\u25c6-\\u25c7 ◆◇
\\u25ca-\\u25cb ◊○
\\u25ce-\\u25cf ◎●

\\u2605-\\u2606 ★☆
\\u2609 ☉
\\u2610 ☐
\\u2640 ♀
\\u2642 ♂
\\u2666 ♦
\\u266a-\\u266b ♪♫

\\u2714 ✔
\\u2717 ✗
\\u274f ❏
\\u2751 ❑
\\u279f ➟
\\u27a2 ➢
\\u27a5 ➥

\\u2a7d ⩽

\\u2fd4 ⿔ CJK++

\\u3001-\\u301e CJK punc

\\u3022-\\u3025 〢〣〤〥

\\u3105-\\u3107 ㄅㄆ
\\u310a ㄊ
\\u3111 ㄑ
\\u3113 ㄓ
\\u3116-\\u3117 ㄖㄗ
\\u311a-\\u311b ㄚㄛ
\\u3122 ㄢ
\\u3125 ㄥ
\\u3127-\\u3128 ㄧㄨ

\\u3220-\\u3229 ㈠㈡㈢㈣㈤㈥㈦㈧㈨
\\u32a3 ㊣
\\u338e-\\u338f ㎎㎏
\\u339c-\\u339d ㎜㎝
\\u33a1 ㎡
\\u33a5 ㎥
\\u33d5 ㏕
\\u33d1-\\u33d2 ㏑㏒

\\u359e 㖞

\\u39d1 㧑

\\u41f2 䇲

\\u4341 䍁

\\u4d13 䴓
\\u4d15 䴕

\\u4e00-\\u9fff CJK

\\uacf3 곳 朝鲜++

\\ucd38 촸 朝鲜++

\\ue20c-\\ue2ff ???

\\uf900-\\ufaff CJK ++

\\ufb03 ﬃ

\\ufe30-\\ufe31 ︰︱
\\ufe33 ︳
\\ufe38 ︸
\\ufe3c-\\ufe3d ︼︽
\\ufe3f-\\ufe41 ︿﹀﹁
\\ufe4d-\\ufe4e ﹍﹎
\\ufe55-\\ufe57 ﹕﹖﹗
\\ufe59-\\ufe5c ﹙﹚﹛
\\ufe5f ﹟
\\ufe63 ﹣
\\ufe65-\\ufe66 ﹥﹦
\\ufe6a-\\ufe6b ﹪﹫
\\ufeff arabic ++ # FE70-FEFF

\\uff01 ！
\\uff08-\\uff09 （）
\\uff0c ，
\\uff1a ：
\\uff1f ？
\\uff61 ｡
\\uff63 ｣
\\uff65 ･
\\uff6c ｬ
\\uff72 ｲ
\\uff86 ﾆ
\\uff89 ﾉ
\\uffe0-\\uffe1 ￠￡
\\uffe3 ￣
\\uffe5 ￥
\\uffed ￭
\\ufffc ￼
"""
