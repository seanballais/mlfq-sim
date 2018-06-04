#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys


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

    def as_dict(self):
        return {
            'start': self.get_start(),
            'length': self.get_length(),
            'end': self.get_end()
        }

    def __eq__(self, other):
        if (self.get_start() == other.get_start()
           and self.get_length() == other.get_length()
           and self.get_end() == other.get_end()):
            return True

        return False


class ExecutionRecordingException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class ProcessControlBlock:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority
        self.execution_history = []

    def __repr__(self):
        return 'A Generic Process (pid {0})\t' \
               'Arrival: {1}\tBurst: {2}\tPriority: {3}'.format(self.pid,
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

    def get_priority(self):
        return self.priority

    def get_execution_history(self):
        return self.execution_history

    def execute(self, start_time, length, record=True):
        if self.remaining_time == 0:
            sys.exit(-1)  # For testing purposes. Do not include malformed result.

        num_execution_items = len(self.execution_history)
        recent_item = None
        increment_item = False

        if num_execution_items > 0:
            max_item_index = max(num_execution_items - 1, 0)
            recent_item = self.execution_history[max_item_index]
            item_start = recent_item.get_start()
            item_end = item_start + recent_item.get_length()
            
            if start_time <= item_start or start_time < item_end:
                sys.exit(-1) # For testing purposes. Do not include malformed result.
            elif start_time == item_end:
                increment_item = True

        self.remaining_time = max(self.remaining_time - length, 0)
        
        if record:
            if increment_item:
                # Meaning that the process was actually executed continuously.
                # We gotta use the "consenting adults" philosophy here.
                recent_item.length += length
            else:
                self.execution_history.append(ExecutionHistoryItem(start_time, length))

    def as_dict(self):
        process_execution_history = self.get_execution_history()
        execution_history = []
        for item in process_execution_history:
            execution_history.append(item.as_dict())

        if len(process_execution_history) > 0:
            response_time = self.get_execution_history()[0].get_start() - self.get_arrival_time()
        else:
            response_time = 0

        waiting_time = response_time
        for index in range(1, len(process_execution_history)):
            waiting_time += (process_execution_history[index].get_start()
                             - process_execution_history[index - 1].get_end())

        if len(process_execution_history) > 0:
            turnaround_time = (process_execution_history[len(process_execution_history) - 1].get_end()
                               - self.get_arrival_time())
        else:
            turnaround_time = 0

        return {
            'pid': self.get_pid(),
            'arrival_time': self.get_arrival_time(),
            'burst_time': self.get_burst_time(),
            'priority': self.get_priority(),
            'response_time': response_time,
            'waiting_time': waiting_time,
            'turnaround_time': turnaround_time,
            'execution_history': execution_history
        }

    def to_json(self):
        return json.dumps(self.as_dict())

    def __eq__(self, other):
        if (self.get_pid() == other.get_pid()
           and self.get_arrival_time() == other.get_arrival_time()
           and self.get_burst_time() == other.get_burst_time()
           and self.get_remaining_time() == other.get_remaining_time()
           and self.get_priority() == other.get_priority()
           and self.get_execution_history() == other.get_execution_history()):
            return True

        return False
