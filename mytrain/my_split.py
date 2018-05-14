from processutils.textfilter import DataSplit
import argparse

parser = argparse.ArgumentParser(description="my_split.py")
parser.add_argument('-f', "--file_prefix")
parser.add_argument('--train_name', default="train")
parser.add_argument('--valid_name', default="valid")
parser.add_argument("--valid_size", default=10000, type=int)
parser.add_argument("--shuffle", default=True, type=bool)
args = parser.parse_args([
    "-f", "../test/medicine.sample.data.filter/data.data.src.encode.dict",
    "--train_name", "train",
    "--valid_name", "valid",
    "--valid_size", "100"
])

args.train_path = args.file_prefix + "." + args.train_name
args.valid_path = args.file_prefix + "." + args.valid_name

if __name__ == '__main__':
    with open(args.file_prefix, "r", encoding="utf8") as f:
        data = f.readlines()

    data_split = DataSplit()
    train, valid = data_split.train_valid_split(data, size=args.valid_size, shuffle=args.shuffle)

    with open(args.train_path, "w", encoding="utf8") as f:
        f.writelines(train)
    with open(args.valid_path, "w", encoding="utf8") as f:
        f.writelines(valid)
