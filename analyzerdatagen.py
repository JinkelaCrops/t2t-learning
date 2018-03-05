import re
import json
import random


def unpack(line, id_sep="###", sep=" ||| "):
    id, line = line.split(id_sep)
    zh, en = line.strip().split(sep)
    # id = int(re.sub("^0+", "", id))
    return zh, en


def train_valid_split(data, size=10000, shuffle=True):
    if shuffle:
        random.seed(0)
        data = random.sample(data, len(data))
    train = data[:-size]
    valid = data[-size:]
    return train, valid


if __name__ == '__main__':
    file_path = "../t2t_med/t2t_datagen/medicine"
    filename_list = [file_path + "/medicine.sample.big.txt.term_nonempty",
                     file_path + "/medicine.sample.big.txt.term_empty", ]
    data = []
    data_dict = []
    for filename in filename_list:
        with open(filename, "r", encoding="utf8") as f:
            data += f.readlines()
        with open(filename + ".dict", "r", encoding="utf8") as fd:
            data_dict += json.load(fd)

    zhs = []
    ens = []
    for line in data:
        zh, en = unpack(line, id_sep="###", sep=" ||| ")
        zhs.append(zh)
        ens.append(en)

    train_zh, valid_zh = train_valid_split(zhs, 1000, True)
    train_en, valid_en = train_valid_split(ens, 1000, True)
    train_zh_dict, valid_zh_dict = train_valid_split(data_dict, 1000, True)

    with open(file_path + "/new_medicine/train.en", "w", encoding="utf8") as f:
        f.writelines([x + "\n" for x in train_en])
    with open(file_path + "/new_medicine/train.zh", "w", encoding="utf8") as f:
        f.writelines([x + "\n" for x in train_zh])
    with open(file_path + "/new_medicine/valid.en", "w", encoding="utf8") as f:
        f.writelines([x + "\n" for x in valid_en])
    with open(file_path + "/new_medicine/valid.zh", "w", encoding="utf8") as f:
        f.writelines([x + "\n" for x in valid_zh])
    # todo: train_zh_dict or train_en_dict ?
    with open(file_path + "/new_medicine/train.zh.dict", "w", encoding="utf8") as f:
        json.dump(train_zh_dict, f, ensure_ascii=False)
    with open(file_path + "/new_medicine/valid.zh.dict", "w", encoding="utf8") as f:
        json.dump(valid_zh_dict, f, ensure_ascii=False)
