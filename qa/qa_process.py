import re

sep = "\t"


def set_intersection(s1, s2):
    return list(set(s1) - (set(s1) - set(s2)))


def compare(src, tgt):
    bi_1 = src + sep + tgt
    bi_2 = tgt + sep + src
    fd_1 = re.findall("(.+)(?=.*%s.*\\1)" % sep, bi_1)
    fd_2 = re.findall("(.+)(?=.*%s.*\\1)" % sep, bi_2)
    fd = set_intersection(fd_1, fd_2)

    output_src = src
    output_tgt = tgt

    if len(fd) > 0:
        fd_regex = "(" + "|".join([re.escape(x) for x in fd]) + ")"
        output_src = re.sub(fd_regex, "<tag>\\1</tag>", output_src)
        output_tgt = re.sub(fd_regex, "<tag>\\1</tag>", output_tgt)

    return output_src, output_tgt


def compare_get_words(src, tgt):
    bi_1 = src + sep + tgt
    bi_2 = tgt + sep + src
    fd_1 = re.findall("(.+)(?=.*%s.*\\1)" % sep, bi_1)
    fd_2 = re.findall("(.+)(?=.*%s.*\\1)" % sep, bi_2)
    fd = set_intersection(fd_1, fd_2)
    return fd


# prefix = '/media/tmxmall/a36811aa-0e87-4ba1-b14f-370134452449'
# with open(f"{prefix}/t2t_med/mynmt/data/medicine.sample.txt/medicine.sample.txt.zh", "r", encoding="utf8") as f:
#     src_lines = [x.strip() for x in f.readlines()]
#
# with open(f"{prefix}/t2t_med/mynmt/data/medicine.sample.txt/medicine.sample.txt.en", "r", encoding="utf8") as f:
#     tgt_lines = [x.strip() for x in f.readlines()]
#
# output_src_lines = []
# output_tgt_lines = []
# for k, (src, tgt) in enumerate(zip(src_lines, tgt_lines)):
#     output_src, output_tgt = compare(src, tgt)
#     output_src_lines.append(output_src + "\n")
#     output_tgt_lines.append(output_tgt + "\n")
#     if k % 10 == 10 - 1:
#         print("processing %s" % (k + 1))
#
# with open(f"{prefix}/t2t_med/mynmt/data/medicine.sample.txt/medicine.sample.txt.zh.tag", "w", encoding="utf8") as f:
#     f.writelines(output_src_lines)
#
# with open(f"{prefix}/t2t_med/mynmt/data/medicine.sample.txt/medicine.sample.txt.en.tag", "w", encoding="utf8") as f:
#     f.writelines(output_tgt_lines)


prefix = '/media/tmxmall/a36811aa-0e87-4ba1-b14f-370134452449'
with open(f"{prefix}/t2t_med/mynmt/data/medicine.sample.txt/medicine.sample.txt.zh", "r", encoding="utf8") as f:
    src_lines = [x.strip() for x in f.readlines()]

with open(f"{prefix}/t2t_med/mynmt/data/medicine.sample.txt/medicine.sample.txt.en", "r", encoding="utf8") as f:
    tgt_lines = [x.strip() for x in f.readlines()]

output_words = []
for k, (src, tgt) in enumerate(zip(src_lines, tgt_lines)):
    words = compare_get_words(src, tgt)
    output_words += words
    if k % 10 == 10 - 1:
        print("processing %s" % (k + 1))

print(sorted(list(set(output_words))))
