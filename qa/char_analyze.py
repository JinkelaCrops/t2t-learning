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
    print("%20s" % regex, len(filter_sentence))
    return len(filter_sentence)


regex_filter_line("[\\u0020-\\u007e]", lines)
regex_filter_line("[\\u00a0-\\u00ff]", lines)
regex_filter_line("[\\u0100-\\u01ff]", lines)
regex_filter_line("[\\u0251]", lines)
regex_filter_line("[\\u025b]", lines)
regex_filter_line("[\\u0261]", lines)
regex_filter_line("[\\u028a]", lines)
regex_filter_line("[\\u02c6-\\u02cb]", lines)
regex_filter_line("[\\u02d0]", lines)
regex_filter_line("[\\u02d8-\\u02da]", lines)
regex_filter_line("[\\u02dc]", lines)
regex_filter_line("[\\u037a]", lines)
regex_filter_line("[\\u037e]", lines)
regex_filter_line("[\\u038a]", lines)
regex_filter_line("[\\u038c]", lines)
regex_filter_line("[\\u03cb]", lines)
regex_filter_line("[\\u03d6]", lines)
regex_filter_line("[\\u0384-\\u0385]", lines)
regex_filter_line("[\\u0387-\\u0388]", lines)
regex_filter_line("[\\u038e-\\u038f]", lines)
regex_filter_line("[\\u0391-\\u03c9]", lines)
regex_filter_line("[\\u0400-\\u04ff]", lines)
regex_filter_line("[\\u0590-\\u05ff]", lines)
regex_filter_line("[\\u0652]", lines)
regex_filter_line("[\\u11bc]", lines)
regex_filter_line("[\\u1868]", lines)
regex_filter_line("[\\u1d31]", lines)
regex_filter_line("[\\u1d52]", lines)
regex_filter_line("[\\u1d5b]", lines)
regex_filter_line("[\\u1ef7]", lines)
regex_filter_line("[\\u2016-\\u206a]", lines)
regex_filter_line("[\\u2070]", lines)
regex_filter_line("[\\u2074-\\u2075]", lines)
regex_filter_line("[\\u2077-\\u2078]", lines)
regex_filter_line("[\\u2082-\\u2084]", lines)
regex_filter_line("[\\u20ac]", lines)
regex_filter_line("[\\u2103]", lines)
regex_filter_line("[\\u2105]", lines)
regex_filter_line("[\\u2109]", lines)
regex_filter_line("[\\u2116]", lines)
regex_filter_line("[\\u2122]", lines)
regex_filter_line("[\\u212b]", lines)
regex_filter_line("[\\u2160-\\u216b]", lines)
regex_filter_line("[\\u2170-\\u2179]", lines)
regex_filter_line("[\\u21d2]", lines)
regex_filter_line("[\\u2190-\\u2193]", lines)
regex_filter_line("[\\u2206]", lines)
regex_filter_line("[\\u2208]", lines)
regex_filter_line("[\\u2211-\\u2212]", lines)
regex_filter_line("[\\u2217-\\u221a]", lines)
regex_filter_line("[\\u221d-\\u2220]", lines)
regex_filter_line("[\\u2223]", lines)
regex_filter_line("[\\u2225]", lines)
regex_filter_line("[\\u2227-\\u222b]", lines)
regex_filter_line("[\\u222e]", lines)
regex_filter_line("[\\u2234]", lines)
regex_filter_line("[\\u2237]", lines)
regex_filter_line("[\\u223c-\\u223d]", lines)
regex_filter_line("[\\u2245]", lines)
regex_filter_line("[\\u224c]", lines)
regex_filter_line("[\\u2252]", lines)
regex_filter_line("[\\u2260-\\u2261]", lines)
regex_filter_line("[\\u2264-\\u2267]", lines)
regex_filter_line("[\\u226f]", lines)
regex_filter_line("[\\u2295]", lines)
regex_filter_line("[\\u2299]", lines)
regex_filter_line("[\\u22a5]", lines)
regex_filter_line("[\\u22bf]", lines)
regex_filter_line("[\\u2312]", lines)
regex_filter_line("[\\u2395]", lines)
regex_filter_line("[\\u2460-\\u2473]", lines)
regex_filter_line("[\\u2474-\\u2487]", lines)
regex_filter_line("[\\u2488-\\u249b]", lines)
regex_filter_line("[\\u2500-\\u257f]", lines)
regex_filter_line("[\\u25a0-\\u25a1]", lines)
regex_filter_line("[\\u25b2-\\u25b4]", lines)
regex_filter_line("[\\u25c6-\\u25c7]", lines)
regex_filter_line("[\\u25ca-\\u25cb]", lines)
regex_filter_line("[\\u25ce-\\u25cf]", lines)
regex_filter_line("[\\u2605-\\u2606]", lines)
regex_filter_line("[\\u2609]", lines)
regex_filter_line("[\\u2610]", lines)
regex_filter_line("[\\u2640]", lines)
regex_filter_line("[\\u2642]", lines)
regex_filter_line("[\\u2666]", lines)
regex_filter_line("[\\u266a-\\u266b]", lines)
regex_filter_line("[\\u2714]", lines)
regex_filter_line("[\\u2717]", lines)
regex_filter_line("[\\u274f]", lines)
regex_filter_line("[\\u2751]", lines)
regex_filter_line("[\\u279f]", lines)
regex_filter_line("[\\u27a2]", lines)
regex_filter_line("[\\u27a5]", lines)
regex_filter_line("[\\u2a7d]", lines)
regex_filter_line("[\\u2fd4]", lines)
regex_filter_line("[\\u3001-\\u301e]", lines)
regex_filter_line("[\\u3022-\\u3025]", lines)
regex_filter_line("[\\u3105-\\u3107]", lines)
regex_filter_line("[\\u310a]", lines)
regex_filter_line("[\\u3111]", lines)
regex_filter_line("[\\u3113]", lines)
regex_filter_line("[\\u3116-\\u3117]", lines)
regex_filter_line("[\\u311a-\\u311b]", lines)
regex_filter_line("[\\u3122]", lines)
regex_filter_line("[\\u3125]", lines)
regex_filter_line("[\\u3127-\\u3128]", lines)
regex_filter_line("[\\u3220-\\u3229]", lines)
regex_filter_line("[\\u32a3]", lines)
regex_filter_line("[\\u338e-\\u338f]", lines)
regex_filter_line("[\\u339c-\\u339d]", lines)
regex_filter_line("[\\u33a1]", lines)
regex_filter_line("[\\u33a5]", lines)
regex_filter_line("[\\u33d5]", lines)
regex_filter_line("[\\u33d1-\\u33d2]", lines)
regex_filter_line("[\\u359e]", lines)
regex_filter_line("[\\u39d1]", lines)
regex_filter_line("[\\u41f2]", lines)
regex_filter_line("[\\u4341]", lines)
regex_filter_line("[\\u4d13]", lines)
regex_filter_line("[\\u4d15]", lines)
regex_filter_line("[\\u4e00-\\u9fff]", lines)
regex_filter_line("[\\uacf3]", lines)
regex_filter_line("[\\ucd38]", lines)
regex_filter_line("[\\ue20c-\\ue2ff]", lines)
regex_filter_line("[\\uf900-\\ufaff]", lines)
regex_filter_line("[\\ufb03]", lines)
regex_filter_line("[\\ufe30-\\ufe31]", lines)
regex_filter_line("[\\ufe33]", lines)
regex_filter_line("[\\ufe38]", lines)
regex_filter_line("[\\ufe3c-\\ufe3d]", lines)
regex_filter_line("[\\ufe3f-\\ufe41]", lines)
regex_filter_line("[\\ufe4d-\\ufe4e]", lines)
regex_filter_line("[\\ufe55-\\ufe57]", lines)
regex_filter_line("[\\ufe59-\\ufe5c]", lines)
regex_filter_line("[\\ufe5f]", lines)
regex_filter_line("[\\ufe63]", lines)
regex_filter_line("[\\ufe65-\\ufe66]", lines)
regex_filter_line("[\\ufe6a-\\ufe6b]", lines)
regex_filter_line("[\\ufeff]", lines)
regex_filter_line("[\\uff01]", lines)
regex_filter_line("[\\uff08-\\uff09]", lines)
regex_filter_line("[\\uff0c]", lines)
regex_filter_line("[\\uff1a]", lines)
regex_filter_line("[\\uff1f]", lines)
regex_filter_line("[\\uff61]", lines)
regex_filter_line("[\\uff63]", lines)
regex_filter_line("[\\uff65]", lines)
regex_filter_line("[\\uff6c]", lines)
regex_filter_line("[\\uff72]", lines)
regex_filter_line("[\\uff86]", lines)
regex_filter_line("[\\uff89]", lines)
regex_filter_line("[\\uffe0-\\uffe1]", lines)
regex_filter_line("[\\uffe3]", lines)
regex_filter_line("[\\uffe5]", lines)
regex_filter_line("[\\uffed]", lines)
regex_filter_line("[\\ufffc]", lines)

"""
     [\u0020-\u007e] 13056272
     [\u00a0-\u00ff] 258619
     [\u0100-\u01ff] 353
            [\u0251] 302
            [\u025b] 2
            [\u0261] 25
            [\u028a] 1
     [\u02c6-\u02cb] 870
            [\u02d0] 1
     [\u02d8-\u02da] 25
            [\u02dc] 10
            [\u037a] 1
            [\u037e] 4
            [\u038a] 3
            [\u038c] 1
            [\u03cb] 3
            [\u03d6] 2
     [\u0384-\u0385] 8
     [\u0387-\u0388] 2
     [\u038e-\u038f] 2
     [\u0391-\u03c9] 567276
     [\u0400-\u04ff] 2058
     [\u0590-\u05ff] 34
            [\u0652] 1
            [\u11bc] 3
            [\u1868] 1
            [\u1d31] 1
            [\u1d52] 1
            [\u1d5b] 1
            [\u1ef7] 1
     [\u2016-\u206a] 323353
            [\u2070] 4
     [\u2074-\u2075] 9
     [\u2077-\u2078] 11
     [\u2082-\u2084] 13
            [\u20ac] 58
            [\u2103] 132218
            [\u2105] 64
            [\u2109] 45
            [\u2116] 559
            [\u2122] 348
            [\u212b] 5
     [\u2160-\u216b] 235239
     [\u2170-\u2179] 1557
            [\u21d2] 3
     [\u2190-\u2193] 15107
            [\u2206] 5
            [\u2208] 281
     [\u2211-\u2212] 839
     [\u2217-\u221a] 75
     [\u221d-\u2220] 861
            [\u2223] 1
            [\u2225] 80
     [\u2227-\u222b] 226
            [\u222e] 8
            [\u2234] 46
            [\u2237] 333
     [\u223c-\u223d] 29
            [\u2245] 1
            [\u224c] 33
            [\u2252] 4
     [\u2260-\u2261] 555
     [\u2264-\u2267] 31397
            [\u226f] 3
            [\u2295] 4
            [\u2299] 17
            [\u22a5] 41
            [\u22bf] 116
            [\u2312] 5
            [\u2395] 4
     [\u2460-\u2473] 48470
     [\u2474-\u2487] 1267
     [\u2488-\u249b] 107
     [\u2500-\u257f] 566
     [\u25a0-\u25a1] 1052
     [\u25b2-\u25b4] 3695
     [\u25c6-\u25c7] 205
     [\u25ca-\u25cb] 339
     [\u25ce-\u25cf] 767
     [\u2605-\u2606] 196
            [\u2609] 3
            [\u2610] 35
            [\u2640] 1017
            [\u2642] 1108
            [\u2666] 2
     [\u266a-\u266b] 9
            [\u2714] 4
            [\u2717] 1
            [\u274f] 1
            [\u2751] 2
            [\u279f] 1
            [\u27a2] 6
            [\u27a5] 1
            [\u2a7d] 3
            [\u2fd4] 2
     [\u3001-\u301e] 7028921
     [\u3022-\u3025] 8
     [\u3105-\u3107] 8
            [\u310a] 1
            [\u3111] 1
            [\u3113] 2
     [\u3116-\u3117] 6
     [\u311a-\u311b] 2
            [\u3122] 1
            [\u3125] 1
     [\u3127-\u3128] 11
     [\u3220-\u3229] 312
            [\u32a3] 6
     [\u338e-\u338f] 125
     [\u339c-\u339d] 75
            [\u33a1] 59
            [\u33a5] 1
            [\u33d5] 24
     [\u33d1-\u33d2] 9
            [\u359e] 6
            [\u39d1] 3
            [\u41f2] 13
            [\u4341] 2
            [\u4d13] 2
            [\u4d15] 1
     [\u4e00-\u9fff] 13056199
            [\uacf3] 2
            [\ucd38] 1
     [\ue20c-\ue2ff] 1305
     [\uf900-\ufaff] 136
            [\ufb03] 1
     [\ufe30-\ufe31] 941
            [\ufe33] 2
            [\ufe38] 4
     [\ufe3c-\ufe3d] 33
     [\ufe3f-\ufe41] 19
     [\ufe4d-\ufe4e] 7
     [\ufe55-\ufe57] 102
     [\ufe59-\ufe5c] 185
            [\ufe5f] 10
            [\ufe63] 70
     [\ufe65-\ufe66] 551
     [\ufe6a-\ufe6b] 233
            [\ufeff] 4
            [\uff01] 886
     [\uff08-\uff09] 622070
            [\uff0c] 3445520
            [\uff1a] 471609
            [\uff1f] 9822
            [\uff61] 2
            [\uff63] 1
            [\uff65] 8
            [\uff6c] 2
            [\uff72] 1
            [\uff86] 1
            [\uff89] 1
     [\uffe0-\uffe1] 160
            [\uffe3] 7143
            [\uffe5] 57
            [\uffed] 9
            [\ufffc] 1
"""

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
