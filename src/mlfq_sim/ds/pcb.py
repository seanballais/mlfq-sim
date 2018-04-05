#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ProcessControlBlock:
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

    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority
        self.execution_history = []

    def __repr__(self):
        return 'A Generic Process (pid {0})\n' \
               'Arrival: {1}\tBurst: {1}\tPriority: {3}'.format(self.pid,
                                                                self.arrival_time,
                                                                self.burst_time,
                                                                self.priority)

    def get_pid(self):
        return self.pid

    def get_arrival_time(self):
        return self.arrival_time

    def get_burst_time(self):
        return self.burst_time

    def get_remaining_time(self):
        return self.remaining_time

    def get_priority():
        return self.priority

    def execute(self, start_time, length):
        if self.remaining_time == 0:
            return

        self.remaining_time = max(self.remaining_time - length, 0)
        self.execution_history.append(ExecutionHistoryItem(start_time, length))
