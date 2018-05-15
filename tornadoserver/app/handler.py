# -*-coding: utf-8 -*-
# __author__ : tinytiger
# __time__   : '2018/1/4 11:08'
# If this runs wrong, don't ask me, I don't know why;
# If this runs right, thank god, and I don't know why.
# Maybe the answer, my friend, is blowing in the wind.

import json
import tornado.web
from tornadoserver.app.biz import sess_field
from tornadoserver.app.biz import decode_inline
from tornadoserver.loginst import logger


class Translate(tornado.web.RequestHandler):
    def post(self):
        data = self.get_argument("args")
        datas = json.loads(data)
        if not isinstance(datas, list) or not all(map(lambda x: isinstance(x, str), datas)):
            logger.warn("[handler] Translate.post: invalid input")
            self.write(json.dumps({"result": "invalid input"}))
        else:
            logger.info("[handler] Translate.post: get sentence and put into input queue")
            # logger.info("[handler] Translate.post: " + data)
            try:
                result = []
                num_of_batch = (len(datas) - 1) // sess_field.batch_size + 1
                for k in range(num_of_batch):
                    lines = datas[k * sess_field.batch_size: (k + 1) * sess_field.batch_size]
                    src_lines, trans_lines = decode_inline(lines)
                    result += trans_lines
                self.write(json.dumps({"result": result}))
                logger.info("[handler] Translate.post: send translated sentence")
            except Exception as e:
                logger.warn("[handler] Translate.post: tornadoserver failed %s %s" % (e.__class__, e.__context__))
                self.write(json.dumps({"result": "tornadoserver failed"}))
