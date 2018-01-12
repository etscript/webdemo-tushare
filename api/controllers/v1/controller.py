#!/usr/bin/env python
#-*- coding: utf-8 -*-
from pecan import rest
from wsme import types as wtypes
from webdemo.api import expose
#from webdemo.api.controllers.v1 import users as v1_users
from webdemo.api.controllers.v1 import stocks as v1_stocks
import logging
logger = logging.getLogger(__name__)

from urllib import pathname2url as quote

class v1Controller(rest.RestController):
    #users = v1_users.UsersController()
    stocks = v1_stocks.StocksController()
    """
    test eg:
         http://127.0.0.1:8080/v1/
    """
    @expose.expose(wtypes.text)
    def get(self):
        logger.info("v1Controller Method Get is called ...")
        #return "python-web-frame: pecan & wsme by v1Controller"
        a = {"code":0,"msg":"成功".encode('utf-8'),"data":{"event":{"answerTime":10,"desc":"12.下列哪个不是西游记中的人物？".encode('utf-8'),"displayOrder":11,"liveId":92,"options":"['孙悟空','唐僧','小红帽']","questionId":1053,"showTime":1515590057640,"status":0,"type":"showQuestion"},"type":"showQuestion"}}
        return a
