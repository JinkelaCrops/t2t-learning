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

Example usage to mydecode.sh from dataset:

  t2t-decoder \
      --data_dir ~/data \
      --problems=algorithmic_identity_binary40 \
      --model=transformer
      --hparams_set=transformer_base

Set FLAGS.decode_interactive or FLAGS.decode_from_file for alternative mydecode.sh
sources.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

# Dependency imports

from tensor2tensor.bin import t2t_trainer
from tensor2tensor.utils import decoding
from tensor2tensor.utils import trainer_lib
from tensor2tensor.utils import usr_dir

import tensorflow as tf

flags = tf.flags
FLAGS = flags.FLAGS

# Additional flags in bin/t2t_trainer.py and utils/flags.py
flags.DEFINE_string("decode_from_file", None,
                    "Path to the source file for decoding")
flags.DEFINE_string("decode_to_file", None,
                    "Path to the decoded (output) file")
flags.DEFINE_bool("decode_interactive", False,
                  "Interactive local inference mode.")
flags.DEFINE_integer("decode_shards", 1, "Number of decoding replicas.")

# ---------------------------------------------------------------
# flags.DEFINE_string("gpuid", None, "limit used gpu")
if FLAGS.gpuid:
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"  # see issue #152
    os.environ["CUDA_VISIBLE_DEVICES"] = FLAGS.gpuid
# ---------------------------------------------------------------

def create_estimator(run_config, hparams):
    return trainer_lib.create_estimator(
        FLAGS.model,
        hparams,
        run_config,
        decode_hparams=decoding.decode_hparams(FLAGS.decode_hparams))

def create_hparams():
    return trainer_lib.create_hparams(
        FLAGS.hparams_set,
        FLAGS.hparams,
        data_dir=os.path.expanduser(FLAGS.data_dir),
        problem_name=FLAGS.problems)


def create_decode_hparams():
    decode_hp = decoding.decode_hparams(FLAGS.decode_hparams)
    decode_hp.add_hparam("shards", FLAGS.decode_shards)
    decode_hp.add_hparam("shard_id", FLAGS.worker_id)
    return decode_hp


def decode(estimator, hparams, decode_hp):
    if FLAGS.decode_interactive:
        decoding.decode_interactively(estimator, hparams, decode_hp)
    elif FLAGS.decode_from_file:
        decoding.decode_from_file(estimator, FLAGS.decode_from_file, hparams,
                                  decode_hp, FLAGS.decode_to_file)
    else:
        decoding.decode_from_dataset(
            estimator,
            FLAGS.problems.split("-"),
            hparams,
            decode_hp,
            decode_to_file=FLAGS.decode_to_file,
            dataset_split="test" if FLAGS.eval_use_test_set else None)


def main(_):
    HOMEPATH = "D:/Projects/t2t_med"

    FLAGS.data_dir = f"{HOMEPATH}/t2t_data/new_medicine_new"
    FLAGS.problems = "translate_zhen_new_med_small_vocab"
    FLAGS.model = "transformer"
    FLAGS.hparams_set = "transformer_big_single_gpu_batch_size"
    FLAGS.output_dir = f"{HOMEPATH}/t2t_train/new_medicine_new/{FLAGS.problems}/{FLAGS.model}-{FLAGS.hparams_set}"


    tf.logging.set_verbosity(tf.logging.INFO)
    trainer_lib.set_random_seed(FLAGS.random_seed)
    usr_dir.import_usr_dir(FLAGS.t2t_usr_dir)

    ckpt_dir = os.path.expanduser(FLAGS.output_dir)

    hparams = create_hparams()
    hparams.no_data_parallelism = True  # To clear the devices
    run_config = t2t_trainer.create_run_config(hparams)

    estimator = create_estimator(run_config, hparams)

    ############################################
    from tensorflow.python.estimator.estimator import random_seed
    from tensorflow.contrib.learn.python.learn.utils.saved_model_export_utils import make_export_strategy
    from tensorflow.python.framework import ops
    ############################################
    g = ops.get_default_graph()
    with ops.Graph().as_default() as g:
        estimator._create_and_assert_global_step(g)
        random_seed.set_random_seed(estimator._config.tf_random_seed)
        serving_input_receiver = make_export_strategy

        # Call the model_fn and collect the export_outputs.
        estimator_spec = self._call_model_fn(
            features=serving_input_receiver.features,
            labels=None,
            mode=model_fn_lib.ModeKeys.PREDICT,
            config=self.config)

        # Build the SignatureDefs from receivers and all outputs
        signature_def_map = build_all_signature_defs(
            serving_input_receiver.receiver_tensors,
            estimator_spec.export_outputs,
            serving_input_receiver.receiver_tensors_alternatives)

        if not checkpoint_path:
            # Locate the latest checkpoint
            checkpoint_path = saver.latest_checkpoint(self._model_dir)
        if not checkpoint_path:
            raise ValueError("Couldn't find trained model at %s." % self._model_dir)

        export_dir = get_timestamped_export_dir(export_dir_base)
        temp_export_dir = get_temp_export_dir(export_dir)

        # TODO(soergel): Consider whether MonitoredSession makes sense here
        with tf_session.Session(config=self._session_config) as session:

            saver_for_restore = estimator_spec.scaffold.saver or saver.Saver(
                sharded=True)
            saver_for_restore.restore(session, checkpoint_path)

            # TODO(b/36111876): replace legacy_init_op with main_op mechanism
            # pylint: disable=protected-access
            local_init_op = (
                    estimator_spec.scaffold.local_init_op or
                    monitored_session.Scaffold._default_local_init_op())
            # pylint: enable=protected-access

            # Perform the export
            builder = saved_model_builder.SavedModelBuilder(temp_export_dir)
            builder.add_meta_graph_and_variables(
                session, [tag_constants.SERVING],
                signature_def_map=signature_def_map,
                assets_collection=ops.get_collection(
                    ops.GraphKeys.ASSET_FILEPATHS),
                legacy_init_op=local_init_op)
            builder.save(as_text)

        # Add the extra assets
        if assets_extra:
            assets_extra_path = os.path.join(compat.as_bytes(temp_export_dir),
                                             compat.as_bytes('assets.extra'))
            for dest_relative, source in assets_extra.items():
                dest_absolute = os.path.join(compat.as_bytes(assets_extra_path),
                                             compat.as_bytes(dest_relative))
                dest_path = os.path.dirname(dest_absolute)
                gfile.MakeDirs(dest_path)
                gfile.Copy(source, dest_absolute)

        gfile.Rename(temp_export_dir, export_dir)




    from google.protobuf import text_format as pbtf

    gdef = tf.GraphDef()

    with open(GRAPH_NAME + "/saved_model.pbtxt", 'r') as f:
        graph_str = f.read()

    pbtf.Merge(graph_str, gdef)

    tf.import_graph_def(gdef)

    tf.GraphDef()

    # Access saved Variables directly
    print(sess.run('bias:0'))
    # This will print 2, which is the value of bias that we saved
    # Now, let's access and create placeholders variables and
    # create feed-dict to feed new data
    graph = tf.get_default_graph()
    w1 = graph.get_tensor_by_name("w1:0")
    w2 = graph.get_tensor_by_name("w2:0")
    feed_dict = {w1: 13.0, w2: 17.0}
    # Now, access the op that you want to run.
    op_to_restore = graph.get_tensor_by_name("op_to_restore:0")
    print(sess.run(op_to_restore, feed_dict))
    # This will print 60 which is calculated
    sess.close()

    ###################################################################################
    from tensor2tensor.utils.decoding import _get_sorted_inputs
    from tensor2tensor.utils.decoding import _decode_batch_input_fn
    from tensor2tensor.utils.decoding import make_input_fn_from_generator
    from tensor2tensor.utils.decoding import _decode_input_tensor_to_features_dict
    from tensor2tensor.utils.decoding import log_decode_results
    ###################################################################################
    filename = FLAGS.decode_from_file
    hparams = hp
    decode_to_file = FLAGS.decode_to_file
    """Compute predictions on entries in filename and write them out."""
    if not decode_hp.batch_size:
        decode_hp.batch_size = 32
    tf.logging.info(
        "decode_hp.batch_size not specified; default=%d" % decode_hp.batch_size)

    problem_id = decode_hp.problem_idx
    # Inputs vocabulary is set to targets if there are no inputs in the problem,
    # e.g., for language models where the inputs are just a prefix of targets.
    has_input = "inputs" in hparams.problems[problem_id].vocabulary
    inputs_vocab_key = "inputs" if has_input else "targets"
    inputs_vocab = hparams.problems[problem_id].vocabulary[inputs_vocab_key]
    targets_vocab = hparams.problems[problem_id].vocabulary["targets"]
    problem_name = FLAGS.problems.split("-")[problem_id]
    tf.logging.info("Performing decoding from a file.")
    sorted_inputs, sorted_keys = _get_sorted_inputs(filename, decode_hp.shards,
                                                    decode_hp.delimiter)
    num_decode_batches = (len(sorted_inputs) - 1) // decode_hp.batch_size + 1

    def input_fn():

        input_gen = _decode_batch_input_fn(
            problem_id, num_decode_batches, sorted_inputs, inputs_vocab,
            decode_hp.batch_size, decode_hp.max_input_size)

        gen_fn = make_input_fn_from_generator(input_gen)
        example = gen_fn()
        return _decode_input_tensor_to_features_dict(example, hparams)

    decodes = []
    # result_iter = estimator.predict(input_fn)
    # ------------------------------------------------------------------------
    #########################
    from tensorflow.python.training import saver
    from tensorflow.python.training import training
    from tensorflow.python.framework import random_seed
    from tensorflow.python.estimator import model_fn as model_fn_lib
    import six
    #########################
    hooks = []
    checkpoint_path = None
    # Check that model has been trained.
    if not checkpoint_path:
        checkpoint_path = saver.latest_checkpoint(estimator._model_dir)
    if not checkpoint_path:
        raise ValueError('Could not find trained model in model_dir: {}.'.format(
            estimator._model_dir))

    random_seed.set_random_seed(estimator._config.tf_random_seed)
    # estimator._create_and_assert_global_step(g)
    features, input_hooks = estimator._get_features_from_input_fn(
        input_fn, model_fn_lib.ModeKeys.PREDICT)

    def _get_features_from_input_fn(input_fn, mode):
        """Extracts the `features` from return values of `input_fn`."""
        result = self._call_input_fn(input_fn, mode)
        input_hooks = []
        if isinstance(result, dataset_ops.Dataset):
            iterator = result.make_initializable_iterator()
            input_hooks.append(_DatasetInitializerHook(iterator))
            result = iterator.get_next()
        if isinstance(result, (list, tuple)):
            # Unconditionally drop the label (the second element of result).
            result = result[0]

        if not _has_dataset_or_queue_runner(result):
            logging.warning('Input graph does not use tf.data.Dataset or contain a '
                            'QueueRunner. That means predict yields forever. '
                            'This is probably a mistake.')
        return result, input_hooks

    estimator_spec = estimator._call_model_fn(
        features, None, model_fn_lib.ModeKeys.PREDICT, estimator.config)
    predictions = estimator._extract_keys(estimator_spec.predictions, None)  # predict_keys is None

    mon_sess = training.MonitoredSession(
        session_creator=training.ChiefSessionCreator(
            checkpoint_filename_with_path=checkpoint_path,
            scaffold=estimator_spec.scaffold,
            config=estimator._session_config),
        hooks=input_hooks + hooks)

    preds_evaluated = mon_sess.run(predictions)

    preds = []
    for i in range(estimator._extract_batch_length(preds_evaluated)):
        pred_dict_tmp = {
            key: value[i]
            for key, value in six.iteritems(preds_evaluated)
        }
        preds.append(pred_dict_tmp)

        mon_sess.close()

    # ------------------------------------------------------------------------
    result_iter = preds

    for result in result_iter:
        if decode_hp.return_beams:
            beam_decodes = []
            beam_scores = []
            output_beams = np.split(result["outputs"], decode_hp.beam_size, axis=0)
            scores = None
            if "scores" in result:
                scores = np.split(result["scores"], decode_hp.beam_size, axis=0)
            for k, beam in enumerate(output_beams):
                tf.logging.info("BEAM %d:" % k)
                score = scores and scores[k]
                decoded_outputs, _ = log_decode_results(result["inputs"], beam,
                                                        problem_name, None,
                                                        inputs_vocab, targets_vocab)
                beam_decodes.append(decoded_outputs)
                if decode_hp.write_beam_scores:
                    beam_scores.append(score)
            if decode_hp.write_beam_scores:
                decodes.append("\t".join(
                    ["\t".join([d, "%.2f" % s]) for d, s
                     in zip(beam_decodes, beam_scores)]))
            else:
                decodes.append("\t".join(beam_decodes))
        else:
            decoded_outputs, _ = log_decode_results(result["inputs"],
                                                    result["outputs"], problem_name,
                                                    None, inputs_vocab, targets_vocab)
            decodes.append(decoded_outputs)
    print(decodes)


if __name__ == "__main__":
    tf.app.run()
