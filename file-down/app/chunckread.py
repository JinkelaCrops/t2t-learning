import io
import sys
from concurrent.futures import ProcessPoolExecutor
import time
import os


class ShardedTextCorpusIterator(object):
    """
    This is the iterator for text corpus, used for sharding large text
    corpus into small shards, to avoid hogging memory.

    Inside this iterator, it automatically divides the corpus file into
    shards of size `shard_size`. Then, for each shard, it processes
    into (example_dict, n_features) tuples when iterates.
    """

    def __init__(self, corpus_path, shard_size):
        """
        Args:
            corpus_path: the corpus file path.
            line_truncate: the maximum length of a line to read.
                            0 for unlimited.
            side: "src" or "tgt".
            shard_size: the shard size, 0 means not sharding the file.
            assoc_iter: if not None, it is the associate iterator that
                        this iterator should align its step with.
        """
        try:
            # The codecs module seems to have bugs with seek()/tell(),
            # so we use io.open().
            self.corpus = io.open(corpus_path, "r", encoding="utf-8")
        except IOError:
            sys.stderr.write("Failed to open corpus file: %s" % corpus_path)
            sys.exit(1)

        self.shard_size = shard_size
        self.last_pos = 0
        self.line_index = 0
        self.eof = False

    def __iter__(self):
        """
        Iterator of (example_dict, nfeats).
        On each call, it iterates over as many (example_dict, nfeats) tuples
        until this shard's size equals to or approximates `self.shard_size`.
        """
        # Yield tuples util this shard's size reaches the threshold.
        self.corpus.seek(self.last_pos)
        while True:
            if self.shard_size != 0 and self.line_index % self.shard_size == 0:
                # This part of check is time consuming on Py2 (but
                # it is quite fast on Py3, weird!). So we don't bother
                # to check for very line. Instead we chekc every 64
                # lines. Thus we are not dividing exactly per
                # `shard_size`, but it is not too much difference.
                cur_pos = self.corpus.tell()
                if cur_pos >= self.last_pos + self.shard_size:
                    self.last_pos = cur_pos
                    raise StopIteration

            line = self.corpus.readline()
            if line == '':
                self.eof = True
                self.corpus.close()
                raise StopIteration

            self.line_index += 1
            yield self._example_dict_iter(line)

    def hit_end(self):
        return self.eof

    def _example_dict_iter(self, line):
        return line


def data_generator(corpus_path, shard_size):
    data_iter = ShardedTextCorpusIterator(corpus_path, shard_size)
    while not data_iter.hit_end():
        dataset = []
        for d in data_iter:
            dataset.append(d)
        yield dataset


def submit(x):
    time.sleep(20)
    return 0


if __name__ == '__main__':

    myexecutor = ProcessPoolExecutor(max_workers=10)

    for f_name in ["../file-down.log", "../service.py"]:
        for x in data_generator(f_name, 500):
            myexecutor.submit(submit, x)
