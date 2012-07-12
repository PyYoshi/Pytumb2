#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from pytumb.models import ModelFactory
from pytumb.utils import Utils

class Parser:
    def parse(self,method,content):
        raise NotImplementedError
    def parse_error(self,content):
        raise NotImplementedError

class RawParser(Parser):
    """For debug"""
    def parse(self,method,content):
        return content
    def parse_error(self,content):
        return content

class ModelParser(Parser):
    """ """
    def __init__(self):
        self.model_factory = ModelFactory
        self.json_lib = Utils.import_simplejson()

    def parse(self,method,content):
        model = getattr(self.model_factory,method.response_type)
        if method.response_type == method.api.RESPONSE_TYPE_AVATAR: # get_avatar()
            result = model.parse(method.api,content)
        else:
            json = self.json_lib.loads(content)
            if method.response_list:
                result = model.parse_list(method.api,json['response'])
            else:
                result = model.parse(method.api,json['response'])
        return result

    def parse_error(self,content):
        json = self.json_lib.loads(content)
        status_code = json['meta']['status']
        err_msg = json['meta']['msg']
        return "status: %d, msg: %s" % (status_code,err_msg)