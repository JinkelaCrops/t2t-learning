# coding=utf-8
# Copyright 2017 The Tensor2Tensor Authors.
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

r"""Decode from trained T2T models.

This binary performs inference using the Estimator API.

Example usage to decode from dataset:

  t2t-decoder \
      --data_dir ~/data \
      --problems=algorithmic_identity_binary40 \
      --model=transformer
      --hparams_set=transformer_base

Set FLAGS.decode_interactive or FLAGS.decode_from_file for alternative decode
sources.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import re
import time

try:
    file_name = __file__.split("/")[-1].replace(".py", "")
except:
    file_name = "my_t2t_decoder"

# Dependency imports

from tensor2tensor.bin import t2t_trainer
from tensor2tensor.utils import decoding
from tensor2tensor.utils import trainer_lib
from tensor2tensor.utils import usr_dir
from tensor2tensor.utils import registry
from tensor2tensor.data_generators import text_encoder
from tensor2tensor.utils.decoding import log_decode_results
import tensorflow as tf

flags = tf.flags
FLAGS = flags.FLAGS
tf.logging.set_verbosity(tf.logging.INFO)


def create_hparams():
    return trainer_lib.create_hparams(
        FLAGS.hparams_set,
        FLAGS.hparams,
        data_dir=os.path.expanduser(FLAGS.data_dir),
        problem_name=FLAGS.problems)


class SessFieldPredict(object):

    def __init__(self, config):
        os.environ["CUDA_VISIBLE_DEVICES"] = config.GPU_DEVICE
        FLAGS.data_dir = config.VOCAB_DIR
        FLAGS.problems = config.PROBLEM_NAME
        FLAGS.model = config.MODEL_NAME
        FLAGS.hparams_set = config.HPARAMS_SET
        FLAGS.output_dir = config.MODEL_DIR
        FLAGS.decode_hparams = config.DECODE_HPARAMS
        batch_size = config.BATCH_SIZE

        self.hparams = create_hparams()
        self.encoders = registry.problem(FLAGS.problems).feature_encoders(FLAGS.data_dir)
        self.ckpt = tf.train.get_checkpoint_state(FLAGS.output_dir).model_checkpoint_path

        self.inputs_ph = tf.placeholder(shape=(batch_size, None), dtype=tf.int32)  # Just length dimension.
        self.batch_inputs = tf.reshape(self.inputs_ph, [batch_size, -1, 1, 1])  # Make it 4D.
        self.features = {"inputs": self.batch_inputs}
        # Prepare the model and the graph when model runs on features.
        tf.logging.info(f"[{file_name}] SessFieldPredict: register T2TModel")
        self.model = registry.model(FLAGS.model)(self.hparams, tf.estimator.ModeKeys.PREDICT)
        self.model_spec = self.model.estimator_spec_predict(self.features)
        self.prediction = self.model_spec.predictions

        self.inputs_vocab = self.hparams.problems[0].vocabulary["inputs"]
        self.targets_vocab = self.hparams.problems[0].vocabulary["targets"]
        self.problem_name = FLAGS.problems

        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=config.GPU_MEM_FRAC)
        self.sess_config = tf.ConfigProto(gpu_options=gpu_options)

        self.batch_size = batch_size
        tf.logging.info(f"[{file_name}] SessFieldPredict: registered")

        self.sess = tf.Session(config=self.sess_config)
        saver = tf.train.Saver()
        tf.logging.info(f"[{file_name}] Decode: model loading ... ")
        saver.restore(self.sess, self.ckpt)
        tf.logging.info(f"[{file_name}] Decode: model loaded.")


def batch_pad(nd):
    max_length = max(map(len, nd))
    pad_nd = [i + [text_encoder.PAD_ID] * (max_length - len(i)) for i in nd]
    return pad_nd


def end_strip(sent):
    return re.sub("(?:<EOS>)*(?:<pad>)*$", "", sent)


def decode(inputs: list, sess_field: SessFieldPredict):
    tf.logging.info(f"[{file_name}] Decode: source: " + str(inputs))
    st_time = time.time()
    inputs_numpy = [sess_field.encoders["inputs"].encode(i) + [text_encoder.EOS_ID] for i in inputs]
    num_decode_batches = (len(inputs_numpy) - 1) // sess_field.batch_size + 1
    results = []
    for i in range(num_decode_batches):
        input_numpy = inputs_numpy[i * sess_field.batch_size:(i + 1) * sess_field.batch_size]
        inputs_numpy_batch = input_numpy + [[text_encoder.EOS_ID]] * (
                sess_field.batch_size - len(input_numpy))
        inputs_numpy_batch = batch_pad(inputs_numpy_batch)  # pad using 0
        # print("[biz] Decode: " + str(inputs_numpy_batch))
        feed = {sess_field.inputs_ph: inputs_numpy_batch}
        result = sess_field.sess.run(sess_field.prediction, feed)
        decoded_outputs = [end_strip(sess_field.encoders["targets"].decode(i)) for i
                           in result["outputs"][:len(input_numpy)]]
        results += decoded_outputs
    tf.logging.info(f"[{file_name}] Decode: target: " + str(results))
    tf.logging.info(f"[{file_name}] Decode: using %10.2f s" % (time.time() - st_time))

    return results
