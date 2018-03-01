# coding=utf-8
# Copyright 2017 Yan Pan.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Data generators for translation data-sets."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

# Dependency imports

from tensor2tensor.data_generators import generator_utils
from tensor2tensor.data_generators import problem
from tensor2tensor.data_generators import text_encoder
from tensor2tensor.data_generators import translate
from tensor2tensor.utils import registry

import tensorflow as tf

FLAGS = tf.flags.FLAGS

# End-of-sentence marker.
EOS = text_encoder.EOS_ID

# End-of-sentence marker.
EOS = text_encoder.EOS_ID

# This is far from being the real WMT17 task - only toyset here
# you need to register to get UN data and CWT data. Also, by convention,
# this is EN to ZH - use translate_enzh_wmt8k_rev for ZH to EN task
#
# News Commentary, around 220k lines
# This dataset is only a small fraction of full WMT17 task
_MED_TRAIN_DATASETS = [[
    "medicine.tar.gz",
    ["medicine/train.en",
     "medicine/train.zh"]]]

_MED_TEST_DATASETS = [[
    "medicine.tar.gz",
    ["medicine/valid.en",
     "medicine/valid.zh"]]]


def get_filename(dataset):
    return dataset[0][0].split("/")[-1]


@registry.register_problem
class TranslateEnzhMed(translate.TranslateProblem):
    """Problem spec for WMT En-Zh translation.
    Attempts to use full training dataset, which needs website
    registration and downloaded manually from official sources:
    CWMT:
      - http://nlp.nju.edu.cn/cwmt-wmt/
      - Website contrains instructions for FTP server access.
      - You'll need to download CASIA, CASICT, DATUM2015, DATUM2017,
          NEU datasets
    UN Parallel Corpus:
      - https://conferences.unite.un.org/UNCorpus
      - You'll need to register your to download the dataset.
    NOTE: place into tmp directory e.g. /tmp/t2t_datagen/dataset.tgz
    """
    @property
    def num_shards(self):
        return 10

    @property
    def targeted_vocab_size(self):
        return 50000

    @property
    def source_vocab_name(self):
        return "med.vocab.enzh-en.%d" % self.targeted_vocab_size

    @property
    def target_vocab_name(self):
        return "med.vocab.enzh-zh.%d" % self.targeted_vocab_size

    def get_training_dataset(self, tmp_dir):
        """UN Parallel Corpus and CWMT Corpus need to be downloaded manually.
        Append to training dataset if available
        Args:
          tmp_dir: path to temporary dir with the data in it.
        Returns:
          paths
        """
        full_dataset = _MED_TRAIN_DATASETS
        return full_dataset

    def generator(self, data_dir, tmp_dir, train):
        train_dataset = self.get_training_dataset(tmp_dir)
        datasets = train_dataset if train else _MED_TEST_DATASETS
        source_datasets = [[item[0], [item[1][0]]] for item in train_dataset]
        target_datasets = [[item[0], [item[1][1]]] for item in train_dataset]
        source_vocab = generator_utils.get_or_generate_vocab(
            data_dir, tmp_dir, self.source_vocab_name, self.targeted_vocab_size,
            source_datasets, file_byte_budget=1e8)
        target_vocab = generator_utils.get_or_generate_vocab(
            data_dir, tmp_dir, self.target_vocab_name, self.targeted_vocab_size,
            target_datasets, file_byte_budget=1e8)
        tag = "train" if train else "dev"
        filename_base = "med_enzh_%sk_tok_%s" % (self.targeted_vocab_size, tag)
        data_path = translate.compile_data(tmp_dir, datasets, filename_base)
        return translate.bi_vocabs_token_generator(data_path + ".lang1",
                                                   data_path + ".lang2",
                                                   source_vocab, target_vocab, EOS)

    @property
    def input_space_id(self):
        return problem.SpaceID.EN_TOK

    @property
    def target_space_id(self):
        return problem.SpaceID.ZH_TOK

    def feature_encoders(self, data_dir):
        source_vocab_filename = os.path.join(data_dir, self.source_vocab_name)
        target_vocab_filename = os.path.join(data_dir, self.target_vocab_name)
        source_token = text_encoder.SubwordTextEncoder(source_vocab_filename)
        target_token = text_encoder.SubwordTextEncoder(target_vocab_filename)
        return {
            "inputs": source_token,
            "targets": target_token,
        }

@registry.register_problem
class TranslateEnzhMedSimple(TranslateEnzhMed):
    @property
    def targeted_vocab_size(self):
        return 8000
