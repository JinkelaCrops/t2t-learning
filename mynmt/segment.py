# -*- coding: utf-8 -*-
"""
使用nltk和hanlp
"""
import re
import nltk
import jieba
from jpype import *
import sys
import argparse

parser = argparse.ArgumentParser(description="segment.py")
parser.add_argument('-f', "--file_path")
parser.add_argument('-l', "--language")
parser.add_argument('-p', "--report", default=10000, type=int)
parser.add_argument("--to_file_name", default=None)
parser.add_argument("--zh_seg_tool", default="jieba")
parser.add_argument("--hanlp_path", default="/media/yanpan/7D4CF1590195F939/Softwares/hanlp")
parser.add_argument("--hanlp_class_path_sep", default=":")

args = parser.parse_args()

"""
>>> import nltk
>>> sentence = "At eight o'clock on Thursday morning Arthur didn't feel very good."
>>> tokens = nltk.word_tokenize(sentence)
>>> tokens
['At', 'eight', "o'clock", 'on', 'Thursday', 'morning',
'Arthur', 'did', "n't", 'feel', 'very', 'good', '.']
>>> tagged = nltk.pos_tag(tokens)
>>> tagged[0:6]
[('At', 'IN'), ('eight', 'CD'), ("o'clock", 'JJ'), ('on', 'IN'),
('Thursday', 'NNP'), ('morning', 'NN')]
"""

"""
from jpype import *

hanlp_path = "D:/Softwares/hanlp"

startJVM(getDefaultJVMPath(), f"-Djava.class.path={hanlp_path}/hanlp-1.5.4.jar;{hanlp_path}", "-Xms1g",
         "-Xmx1g")  # 启动JVM，Linux需替换分号;为冒号:
HanLP = JClass('com.hankcs.hanlp.HanLP')
# 中文分词
print(HanLP.segment('你好，欢迎在Python中调用HanLP的API'))
print([a.word for a in HanLP.segment('你好，欢迎在Python中调用HanLP的API')])
testCases = [
    "商品和服务",
    "结婚的和尚未结婚的确实在干扰分词啊",
    "买水果然后来世博园最后去世博会",
    "中国的首都是北京",
    "欢迎新老师生前来就餐",
    "工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作",
    "随着页游兴起到现在的页游繁盛，依赖于存档进行逻辑判断的设计减少了，但这块也不能完全忽略掉。"]
for sentence in testCases: print(HanLP.segment(sentence))
# 命名实体识别与词性标注
NLPTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
print(NLPTokenizer.segment('中国科学院计算技术研究所的宗成庆教授正在教授自然语言处理课程'))
# 关键词提取
document = "水利部水资源司司长陈明忠9月29日在国务院新闻办举行的新闻发布会上透露，" \
           "根据刚刚完成了水资源管理制度的考核，有部分省接近了红线的指标，" \
           "有部分省超过红线的指标。对一些超过红线的地方，陈明忠表示，对一些取用水项目进行区域的限批，" \
           "严格地进行水资源论证和取水许可的批准。"
print(HanLP.extractKeyword(document, 2))
# 自动摘要
print(HanLP.extractSummary(document, 3))
# 依存句法分析
print(HanLP.parseDependency("徐先生还具体帮助他确定了把画雄鹰、松鼠和麻雀作为主攻目标。"))
shutdownJVM()
"""


class SegmentNLTK(object):
    def __init__(self):
        pass

    @staticmethod
    def process(en_sentence):
        tokens = nltk.word_tokenize(en_sentence)
        return tokens


class SegmentHanLP(object):
    def __init__(self):
        pass

    @staticmethod
    def process(zh_sentence):
        HanLP = JClass('com.hankcs.hanlp.HanLP')
        tokens = [a.word for a in HanLP.segment(zh_sentence)]
        return tokens


class SegmentJieba(object):
    def __init__(self):
        pass

    @staticmethod
    def process(zh_sentence):
        tokens = list(jieba.cut(zh_sentence, HMM=False))
        return tokens


def segment_process(file_path, process_class):
    seg_lines = []
    with open(file_path, "r", encoding="utf8") as f:
        for k, line in enumerate(f):
            seg_line = process_class.process(line.strip())
            seg_lines.append(" ".join(seg_line))
            if k % args.report == args.report - 1:
                print(f"segment info: segment step {k+1}")
    return seg_lines


def afterprocess(line):
    line = re.sub(" +", " ", line).strip()
    return line


if __name__ == '__main__':
    file_path = args.file_path
    file_name = file_path.replace("\\", "/").split("/")[-1]
    file_father_dir = "/".join(file_path.replace("\\", "/").split("/")[:-1])

    if args.language == "zh":
        if args.zh_seg_tool not in ["hanlp", "jieba"]:
            sys.exit(1)

        if args.zh_seg_tool == "hanlp":

            startJVM(getDefaultJVMPath(),
                     f"-Djava.class.path={args.hanlp_path}/hanlp-1.5.4.jar{args.hanlp_class_path_sep}{args.hanlp_path}",
                     "-Xms1g", "-Xmx1g")  # 启动JVM，Linux需替换分号;为冒号:
            seg_lines = segment_process(file_path, SegmentHanLP)
            shutdownJVM()

        elif args.zh_seg_tool == "jieba":
            seg_lines = segment_process(file_path, SegmentJieba)

    if args.language == "en":
        seg_lines = segment_process(file_path, SegmentNLTK)

    to_file_name = f"seg.{file_name}" if args.to_file_name is None else args.to_file_name

    with open(f"{file_father_dir}/{to_file_name}", "w", encoding="utf8") as f:
        f.writelines(["%s\n" % afterprocess(line) for line in seg_lines])
