import os

# split file and manual check
file_dir = "../t2t_med/t2t_datagen/medicine"
file_name = "medicine.sample.big.txt"
split_dir = file_dir + "/medicine_split"

with open(file_dir + "/" + file_name, "r", encoding="utf8") as f:
    data = f.readlines()

if not os.path.exists(split_dir):
    os.mkdir(split_dir)
for i in range(0, len(data), 100):
    split_file_name = file_name + "." + f"0000{i//100 + 1}"[-4:]
    with open(split_dir + "/" + split_file_name, "w", encoding="utf8") as f:
        f.writelines(data[i:i + 100])

# file 0001

# src tgt都存在，可校验
# 百分比 [0-9 ]+\.[0-9 ]+%  必须要有一个数字
# 小数   [0-9 ]+\.[0-9 ]    必须要有一个数字
# 数字   [0-9 ]+
# 年代   在数字前
# 单位   case******
# 专有名词 以中文分割且在英文中出现(或只差空格)，位置相似
# # 只有英文大写(专有术语)
# # 英文大小写(化学元素或专有术语), CamelCase
# # 英文大小写加数字(化合物或代号)，这个要在# 数字之前
# # # 化合物前缀 3,5-，这个要在# 数字之前 无依赖
# # 其他化合物，在上面之前
# # 人名，在上面之前
# # 论文引用（这个要在最前，一般是()包括，英到中其实不需要翻译这个）


# 术语，需要特殊整理，可以设置backup，要在前面之前，或者未来使用char-word hybird model直接拼写术语？
# 还是提取术语以后专门使用网络训练去翻译术语？化合物什么的应该不是大问题，翻译固定
# 特殊术语 et al. 等人 e.g.(eg如) 罗马数字，同义替换
# 中英文对应的符号 ? ! () [] {} : ; "" ''，同义替换
# 列举术语，取出列举case，人工锁定（加特殊符号$$），需要总结规则。泡菜汁中含有多种泡菜乳酸菌，如明串珠菌属乳酸菌、乳球属乳酸菌、乳杆菌属乳酸菌、双歧杆菌属乳酸菌之一 ||| the sauerkraut juice comprise various sauerkraut lactobacillus such as lactobacillus of Leuconostoc, lactobacillus of lactococcus, lactic acid bacteria of Lactobacillus, and lactobacillus of Bifidobacterium
# 日期，这个要整理出最常见的日期翻译方式，在年代前

# 不匹配
# 开头为括号或数字序号或符号但是没有对应(开头是特殊格式)
# 整句英文都大写，句子中大部分都开头大写
# ...
# 第一个大类部分满足的，即QA不通过，事实上有些QA可以为我所用：括号不匹配啥的，中文有术语但是英文没有（反过来也是）