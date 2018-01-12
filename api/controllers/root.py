#!/usr/bin/env python
#-*- coding: utf-8 -*-
from pecan import rest
from wsme import types as wtypes
from webdemo.api import expose
from webdemo.api.controllers.v1 import controller as v1_controller
import logging
logger = logging.getLogger(__name__)
import json

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class RootController(rest.RestController):
    v1 = v1_controller.v1Controller()
    """
    test eg:
         http://127.0.0.1:8080/
    """
    @expose.expose(wtypes.text)
    def get(self):
        logger.info("Method Get is called ...")
        a = {"code": 0, "msg": "成功", "data": {
            "event": {"answerTime": 10, "desc": "12.下列哪个是西游记中的人物？", "displayOrder": 11, "liveId": 92,
                      "options": "['辣鸡','唐僧','小红帽']", "questionId": 1053, "showTime": 1515590057640, "status": 0,
                      "type": "showQuestion"}, "type": "showQuestion"}}
        return a
        #return "python-web-frame: pecan & wsme "
