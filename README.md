# 医学机器翻译开发

医学领域机器翻译模块主要功能是机器翻译模型的训练，以及机器翻译模型的预测。使用的开发语言为`python`，
依赖的模块及主要功能为
* `tensorflow-gpu`: 注意要使用GPU版本的`tensorflow`
* `tornado`: 进行数据读写及解码器服务搭建
* `requests`: 发送请求
* `pandas`: 数据处理
* `numpy`: 数据处理
* `nltk`: 英文分词及`BLEU`计算
* `jieba`: 中文分词
* `tensor2tensor`: `transformer`模型实现及词典数据处理，版本`1.5.5`，安装其全部依赖以后，直接将主文件夹`tensor2tensor`
放在代码路径下，并不安装为模块。原因是方便管理、定制和debug。原本计划在训练中指定`t2t_usr_dir`，从而避免直接修改
`tensor2tensor`代码，但是发现还是直接修改来的清晰快捷。

具体来说有三个任务
1. 机器翻译模型训练
2. 机器翻译模型预测
3. 机器翻译服务


## 机器翻译模型训练

训练程序所在的文件夹为`mytrain`，训练代码没有统一的`.py`文件入口，取而代之的是
`train_data_prepare.sh`和`train_t2t_training.sh`两个`.sh`脚本。

### 数据预处理
采用了http服务进行数据读写，因此在数据处理前，应该首先开启`file-down/service.py`文件读写服务

全部代码存放在`mytrain/train_data_prepare.sh`文件中

以代码根目录下的`test/medicine.sample`数据文件为例，数据预处理分为以下几个步骤：

1. 使用`mytrain/my_merge.py`合并`test/medicine.sample`全部的数据文件，保存为单一的数据文件`test/medicine.sample.data/data`，
使用`RemoteIO`读写数据

2. 使用`mytrain/my_split.py`从数据`test/medicine.sample.data/data`中拆分测试集和训练数据，分别保存为如下两个文件
    * `test/medicine.sample.data/data.test`，双语测试集
    * `test/medicine.sample.data/data.data`，双语训练数据
    
3. 从训练数据中过滤出有效的训练数据。这里使用术语过滤，其中，术语的定义及生成可以在`processutils/analyze.py`中找到，
具体有以下几类术语：
    1. `PercentDecimal`: 小数百分比
    2. `PercentInteger`: 整数百分比
    3. `NumericDecimal`: 小数
    4. `NumericInteger`: 整数
    5. `NumericYear`: 年份
    6. `TermUpperCase`: 大写缩略词
    7. `TermCamelCase`: 驼峰拼写
    8. `TermEnCharWithNum`: 数字与英文混杂的术语
    9. `TermChemicalPrefix`: 化合物前缀
   
    术语包含但是不局限于这几种，由于不同的术语在句子中的含义不同，因此需要使用不同的记号将其分开。这里采用的就是术语对应的英文名字。
    术语和术语之间可能存在重叠，因此要解决冲突，这里使用`processutils.analyze.max_length_subpiece`实现。在生成每个原文译文句对的术语后，
    还需要根据一些条件进行过滤，过滤条件可以在`mytrain.my_filter.AnalyzeFilter`中找到，包含以下几个过滤条件
    1. `sub_order_dict_equal`: 原文和译文的术语完全对应
    2. `all_term_filter`: 原文和译文的术语个数不超过一句字数的50%
    3. `raw_filter`: 原文和译文中不以`...`结尾，且原文和译文中只能一边有中文汉字
    
    使用`mytrain/my_filter.py`从双语训练数据`test/medicine.sample.data/data.data`中生成术语信息并进行过滤，保存到
    `test/medicine.sample.data.filter`:
    * `data.data.src.encode`，原文术语encode结果
    * `data.data.tgt.encode`，译文术语encode结果
    * `data.data.src.encode.dict`，原文术语列表
    * `data.data.tgt.encode.dict`，译文术语列表
    * `data.data.origin`，原始训练数据
    
    使用http服务进行读写

    事实上`processutils/analyze.py`的术语生成及过滤标准并不完美，可以继续开发升级: `processutils/analyze_dev.py`
    
4. 使用`mytrain/my_split.py`拆分训练集和测试集
    * `data.data.src.encode` =\> `data.data.src.encode.train`, `data.data.src.encode.valid`
    * `data.data.tgt.encode` =\> `data.data.tgt.encode.train`, `data.data.tgt.encode.valid`
    * `data.data.src.encode.dict` =\> `data.data.src.encode.dict.train`, `data.data.src.encode.dict.valid`
    * `data.data.tgt.encode.dict` =\> `data.data.tgt.encode.dict.train`, `data.data.tgt.encode.dict.valid`
    * `data.data.origin` =\> `data.data.origin.train`, `data.data.origin.valid`
    
    将`test/medicine.sample.data.filter/data.data.origin.valid`复制到`test/medicine.sample.data/data.valid`
    
5. 使用`mytrain/my_segment.py`对encode结果进行分词。使用分词包`nltk`及`jieba`，关闭`jieba`的`HMM`新词发现。由于`tensor2tensor`中使用`SubWordEncode`
生成词典，所以中文分词的准确率不会太影响翻译结果好坏。
    * `data.data.src.encode.train` =\> `data.data.src.encode.train.seg` 
    * `data.data.tgt.encode.train` =\> `data.data.tgt.encode.train.seg` 
    * `data.data.src.encode.valid` =\> `data.data.src.encode.valid.seg` 
    * `data.data.tgt.encode.valid` =\> `data.data.tgt.encode.valid.seg` 
    
6. 将分词过后的数据放在`test/medicine.sample.gen/medicine`下，并打包到`medicine.tar.gz`
    * `data.data.src.encode.train.seg` =\> `train.zh`
    * `data.data.tgt.encode.train.seg` =\> `train.en` 
    * `data.data.src.encode.valid.seg` =\> `valid.zh` 
    * `data.data.tgt.encode.valid.seg` =\> `valid.en` 

7. 在`tensor2tensor/data_generators`下注册新任务`translate_zhen_med.py`，并在`all_problems.py`中注册
    ```python
    from tensor2tensor.data_generators import translate_zhen_med
    ```

8. 使用`tensor2tensor/bin/t2t_datagen.py`进行`SubWordEncode`生成词典和`tensor2tensor`的训练数据，其中
    * `problem`为刚才注册过的`translate_zhen_med_small_vocab`，词典大小为`30000`
    * `tmp_dir`为刚才导出数据的`test/medicine.sample.gen`
    * `data_dir`为指定的存放词典及训练数据文件夹`test/t2t_datagen/new_med`

数据预处理结束以后，可以在`test/t2t_datagen/new_med`下看到两个词典文件
* `med.vocab.zhen-en.30000`
* `med.vocab.zhen-zh.30000`

多份准备好的训练数据及验证数据
* `translate_zhen_med_small_vocab-train-000*-of-00100`
* `translate_zhen_med_small_vocab-dev-00000-of-00001`

### 训练
采用`tensor2tensor`的`transformer`模型训练机器翻译模型，首先要确定`transformer`的参数，
在`tensor2tensor/models/transformer.py`中注册新的`hparams_set`: `transformer_big_single_gpu_batch_size_1600`

全部代码存放在`mytrain/train_t2t_training.sh`文件中

具体参数如下：
 * `problems`: `translate_zhen_med_small_vocab`
 * `model`: `transformer`
 * `hparams_set`: `transformer_big_single_gpu_batch_size_1600`
 * `data_dir`: `test/t2t_datagen/new_med`
 * `output_dir`: `test/t2t_train/new_med/translate_zhen_med_small_vocab/transformer-transformer_big_single_gpu_batch_size_1600`
 * `worker_gpu`: 1, 可以改为2

在训练过程中，可以使用`tensorboard`查看训练情况
```shell
cd test/t2t_train
source activate py36
tensorboard --logdir=new_med
```
在浏览器中输入`localhost:6006`可以看到训练情况



## 机器翻译预测

训练程序所在的文件夹为`mynmt`，入口为
* `my_translate_inline.py`: 直接进行翻译
* `my_translate_eval_inline.py`: 从双语文本中进行翻译并计算BLEU

大概流程有以下几个
1. `before_translate`
    * 双语句对解包（如果输入单语文件直接翻译，则忽略）
    * 生成原文术语`src_encode_dict`及术语encode之后的原文`src_encode`
    * 生成译文术语`tgt_encode_dict`及术语encode之后的译文`tgt_encode`（可忽略）
    * 分词及分词后处理，生成`src_encode_seg`
    * 分词及分词后处理，生成`tgt_encode_seg`（可忽略）
2. `translate_one`
    * 翻译，使用`SessPredictField`及`decode`函数，这里仅仅是对原始的`tensor2tensor`提供的解码器进行了一个改装。由于使用大于1的`batch_size`可以加速解码，故在`mynmt/my_config.py`中支持`batch_size`修改。没有生成静态图，而是直接从`tensorflow`的`.ckpt`文件中恢复参数。后续可以考虑成成静态图进行优化升级。
3. `after_translate`
    * 将`src_encode_dict`应用到翻译结果上，进行`decode`。如果翻译结果比较差，则`decode`失败，故需要后备处理。
    * 翻译后处理，参考`yicat`的`QAProcess`，开发时请参考翻译结果
        * 标点符号前后多余空格删除
        * 跳过常见的几个缩略词
        * 结束标点后转换为大写
        * 中文和英文、中文和中文直接的空格删除
        * 特殊字符前后空格删除
        * 连字符前后空格删除，有例外情况需要判定
4. `bleu_calc`
    * 全部翻译完以后可以进行BLEU计算，使用`nltk`实现

由于`python`版本的解码器速度太慢，约0.6s一条，因此可以考虑使用`c++`实现。但是需要重写整个模型，故工程量很大。



## 机器翻译服务

`tornadoserver`，使用`tornado`搭建，不同于`file-down`，这个服务依赖其他模块较多，且端口（8001）与`file-down`不同（8000）

要指定好`tornadoserver/config.py`的参数，启动入口为根目录下的`tornadoserver.sh`
```shell
bash tornadoserver/tornadoserver.sh 
```
