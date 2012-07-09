#!/usr/bin/env python
# -*- coding: utf-8 -*-

class PytumbError(Exception):
    """pytumb exception"""

    def __init__(self, reason, response=None):
        self.__reason = str(reason)
        self.__response = response

    def get_response(self):
        return self.__response

    def __str__(self):
        return self.__reason