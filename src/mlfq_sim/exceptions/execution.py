#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ExecutionRecordingException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)