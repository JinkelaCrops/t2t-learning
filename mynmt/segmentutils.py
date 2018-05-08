import nltk
import jieba
import sys


class SegmentNLTK(object):
    def __init__(self):
        pass

    @staticmethod
    def process(en_sentence):
        tokens = nltk.word_tokenize(en_sentence)
        return tokens


class SegmentJieba(object):
    def __init__(self):
        pass

    @staticmethod
    def process(zh_sentence):
        tokens = list(jieba.cut(zh_sentence, HMM=False))
        return tokens

