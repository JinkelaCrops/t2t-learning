from tensor2tensor.utils import registry
from tensor2tensor.models.transformer import transformer_big_single_gpu


@registry.register_hparams
def transformer_big_single_gpu_batch_size_1600():
    """HParams for transfomer big model on WMT."""
    hparams = transformer_big_single_gpu()
    hparams.batch_size = 1600
    # small vocab 30000: 1600 for single gpu
    hparams.symbol_modality_num_shards = 1
    return hparams


@registry.register_hparams
def transformer_big_single_gpu_batch_size():
    """HParams for transfomer big model on WMT."""
    hparams = transformer_big_single_gpu()
    hparams.batch_size = 1600
    # small vocab 30000: 1600 for single gpu
    hparams.symbol_modality_num_shards = 1
    return hparams
