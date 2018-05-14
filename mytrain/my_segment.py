from processutils.segment import SegmentNLTK
from processutils.segment import SegmentJieba
from processutils.segment import segment_afterprocess
import argparse

parser = argparse.ArgumentParser(description="my_segment.py")
parser.add_argument('-f', "--file_prefix")
parser.add_argument('--lan', default="lan1")
args = parser.parse_args([
    "-f", "../test/medicine.sample.data.filter/data.data.tgt.encode.valid",
    "--lan", "en"
])

segment_dict = {"en": SegmentNLTK, "zh": SegmentJieba}

args.seg_path = args.file_prefix + ".seg"

if __name__ == '__main__':
    with open(args.file_prefix, "r", encoding="utf8") as f:
        data = f.readlines()

    process_class = segment_dict[args.lan]
    seg_data = []
    for sentence in data:
        sentence = sentence.strip()
        sentence_seg = process_class.process(sentence)
        sentence_seg_line = segment_afterprocess(" ".join(sentence_seg))
        seg_data.append(sentence_seg_line + "\n")

    with open(args.seg_path, "w", encoding="utf8") as f:
        f.writelines(seg_data)
