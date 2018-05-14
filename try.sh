#!/usr/bin/env bash

export PYTHONPATH="/home/tmxmall/PycharmProjects/medicine-translate/t2t-learning-2:$PYTHONPATH"

#python mynmt/my_translate_inline.py --file_path test/test.en --src_lan en --tgt_lan zh

python tornadoserver/service.py


