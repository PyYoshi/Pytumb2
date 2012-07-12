#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import urlparse as urlparse_lib

import pytz

from pytumb.error import PytumbError

class Utils:
    @staticmethod
    def join_string(l,string):
        if l != [] or l != None:
            ret = ""
            l_len = len(l)
            for i in range(l_len):
                if i < l_len-1:
                    ret += str(l[i]) + string
                else:
                    ret += str(l[i])
            return ret
        else:
            return None

    @staticmethod
    def check_type(p_obj, p_obj_name, class_or_type):
        if p_obj != None:
            if class_or_type in [int,long]:
                if not isinstance(long(p_obj),(int,long)): raise PytumbError("Invalid %s. Must be %s object."%(p_obj_name,class_or_type.__name__))
            elif class_or_type in [str,unicode]:
                if not isinstance(p_obj,(str,unicode)): raise PytumbError("Invalid %s. Must be %s object."%(p_obj_name,class_or_type.__name__))
            else:
                if not isinstance(p_obj,class_or_type): raise PytumbError("Invalid %s. Must be %s object."%(p_obj_name,class_or_type.__name__))

    GMT = pytz.timezone("GMT")
    GMT_FORMAT = '%Y-%m-%d %H:%M:%S %Z'

    @classmethod
    def gmtstring2datetime(cls,gmtstring):
        """description
        Args:
            gmtstring: str, style is '%Y-%m-%d %H:%M:%S %Z'
                e.g.) gmtstring='2012-07-10 22:55:46 GMT'
        Returns:
            datetime.datetime
        """
        if gmtstring:
            local_dt_gmt = datetime.datetime.strptime(gmtstring,cls.GMT_FORMAT)
            return cls.GMT.localize(local_dt_gmt)
        else:
            return None

    @classmethod
    def datetime2gmtstring(cls,local_dt=datetime.datetime.now()):
        """description
        Args:
            local_dt: datetime.datetime,
        Returns:
            str, style is '%Y-%m-%d %H:%M:%S %Z'
                e.g.) '2012-07-10 22:55:46 GMT'
        """
        if local_dt:
            local_dt_gmt = cls.GMT.localize(local_dt)
            return local_dt_gmt.strftime(cls.GMT_FORMAT)
        else:
            return None

    @staticmethod
    def import_simplejson():
        # written by Joshua Roesslein. https://github.com/tweepy/tweepy/blob/master/tweepy/utils.py
        try:
            import ujson as json
        except ImportError:
            try:
                import simplejson as json
            except ImportError:
                try:
                    import json  # Python 2.6+
                except ImportError:
                    try:
                        from django.utils import simplejson as json  # Google App Engine
                    except ImportError:
                        raise ImportError("Can't load a json library")
        return json

    @staticmethod
    def unixtime2datetime(unixtimestamp):
        return datetime.datetime.fromtimestamp(unixtimestamp)

    @staticmethod
    def urlparse(url):
        return urlparse_lib.urlparse(url)

    @staticmethod
    def parse_qs(qs):
        return urlparse_lib.parse_qs(qs)