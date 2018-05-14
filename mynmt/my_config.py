PROBLEM_NAME = "translate_zhen_new_med_small_vocab"
MODEL_NAME = "transformer"
HPARAMS_SET = "transformer_big_single_gpu_batch_size"
DECODE_HPARAMS = "beam_size=4,alpha=0.6"

# HOME_PATH = "/media/tmxmall/a36811aa-0e87-4ba1-b14f-370134452449/t2t_med"
HOME_PATH = "/media/yanpan/7D4CF1590195F939/Projects/t2t_med"
VOCAB_DIR = f"{HOME_PATH}/t2t_data/new_medicine_new"
MODEL_DIR = f"{HOME_PATH}/t2t_train/new_medicine_new/{PROBLEM_NAME}/{MODEL_NAME}-{HPARAMS_SET}"
USR_DIR = "my_t2t"

BATCH_SIZE = 32
GPU_DEVICE = "0"
GPU_MEM_FRAC = 0.95
