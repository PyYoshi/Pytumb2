#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

import pytz

from pytumb.error import PytumbError

class Utils:
    @staticmethod
    def join_string(l,string):
        if l != [] or l != None:
            ret = ""
            for i in l:
                ret += str(i) + string
            return ret
        else:
            return None

    @staticmethod
    def check_type(p_obj, p_obj_name, class_or_type):
        if p_obj != None:
            if class_or_type in [int,long]:
                if not isinstance(long(p_obj),(int,long)): raise PytumbError("Invalid %s. Must be %s object."%(p_obj_name,class_or_type.__name__))
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
        local_dt_gmt = datetime.datetime.strptime(gmtstring,cls.GMT_FORMAT)
        return cls.GMT.localize(local_dt_gmt)

    @classmethod
    def datetime2gmtstring(cls,local_dt=datetime.datetime.now()):
        """description
        Args:
            local_dt: datetime.datetime,
        Returns:
            str, style is '%Y-%m-%d %H:%M:%S %Z'
                e.g.) '2012-07-10 22:55:46 GMT'
        """
        local_dt_gmt = cls.GMT.localize(local_dt)
        return local_dt_gmt.strftime(cls.GMT_FORMAT)

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
