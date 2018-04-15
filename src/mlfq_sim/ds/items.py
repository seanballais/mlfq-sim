#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ExecutionHistoryItem:
    def __init__(self, start_time, length):
        self.start_time = start_time
        self.length = length

    def __repr__(self):
        return 'Execution History Item ' \
               '(executed starting at {0} for {1} units)'.format(self.start_time,
                                                                 self.length)

    def get_start(self):
        return self.start_time

    def get_length(self):
        return self.length

    def get_end(self):
        return self.start_time + self.length


class ScheduleItem:
    def __init__(self, pid, start_time, length):
        self.pid = pid
        self.start_time = start_time
        self.length = length

    def get_pid(self):
        return self.pid

    def get_start_time(self):
        return self.start_time

    def get_length(self):
        return self.length

    def get_end(self):
        return self.start_time + self.length
