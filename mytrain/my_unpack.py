from processutils.textfilter import Unpack
from utils.simplelog import Logger

import argparse

parser = argparse.ArgumentParser(description="my_unpack")
parser.add_argument('-f', "--file_prefix", required=True)
parser.add_argument('-sep', "--separator", required=True)

args = parser.parse_args([
    "-f", "../test/medicine.sample.data/data.test",
    "-sep", ' ||| '
])
# args = parser.parse_args()
args.output_src = args.file_prefix + ".src"
args.output_tgt = args.file_prefix + ".tgt"
log = Logger("my_filter", "my_filter.log").log()


def main(data):
    unpack = Unpack(args.separator)
    src_lines = []
    tgt_lines = []
    for k, line in enumerate(data):
        try:
            src, tgt, change_order = unpack.unpack(line)
        except Exception as e:
            log.error(f"unpack error: {e.__class__}, {e.__context__}, ### {line.strip()}")
            continue
        src_lines.append(src + "\n")
        tgt_lines.append(tgt + "\n")
    return src_lines, tgt_lines


if __name__ == '__main__':
    with open(args.file_prefix, "r", encoding="utf8") as f:
        data = f.readlines()

    src_lines, tgt_lines = main(data)

    with open(args.output_src, "w", encoding="utf8") as f:
        f.writelines(src_lines)
    with open(args.output_tgt, "w", encoding="utf8") as f:
        f.writelines(tgt_lines)
