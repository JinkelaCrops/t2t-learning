import tensorflow as tf
from tensorflow import saved_model


HOMEPATH = "D:/Projects/t2t_med"

data_dir = f"{HOMEPATH}/t2t_data/new_medicine_new"
problems = "translate_zhen_new_med_small_vocab"
model = "transformer"
hparams_set = "transformer_big_single_gpu_batch_size"
output_dir = f"{HOMEPATH}/t2t_train/new_medicine_new/{problems}/{model}-{hparams_set}"

export_dir = f"{output_dir}/export/Servo/1523011017"


sess = tf.Session(graph=tf.Graph())
# saved_model.tag_constants: TRAINING, SERVING, GPU, TPU
tf.saved_model.loader.load(sess, [saved_model.tag_constants.SERVING], export_dir)
graph = sess.graph
y1 = graph.get_tensor_by_name("transformer/strided_slice_10:0")
x0 = graph.get_tensor_by_name("serialized_example:0")
t1 = sess.run(y1, feed_dict={x0: ["我 是 一个 人"]})

x1 = graph.get_tensor_by_name("transformer/ExpandDims:0")
y1 = graph.get_tensor_by_name("transformer/strided_slice_10:0")
y2 = graph.get_tensor_by_name("transformer/Select_1:0")
sess.run(x1)
sess.close()

sess2 = tf.Session(graph=graph)
preds_evaluated = sess2.run(x1, feed_dict={x0: ["我 是 一个 人"]})
sess2.close()

aa = input_fn()


