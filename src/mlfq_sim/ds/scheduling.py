#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import queue
import heapq


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


class AgedQueue(queue.PriorityQueue):
    def __init__(self, max_size=0):
        super().__init__(max_size)
        self._index = 0

    def _put(self, process):
        process_age = len(process.get_execution_history())
        heapq.heappush(self.queue, (process_age, self._index, process))
        self._index += 1

    def _get(self):
        # The object itself is the third element
        # in the tuple.
        try:
            process = heapq.heappop(self.queue)
            return process[2]
        except IndexError:
            return None


class WaitQueue(queue.PriorityQueue):
    def __init__(self, key=lambda process: process.get_arrival_time(), max_size=0):
        super().__init__(max_size)
        self._index = 0
        self._key = key
        self._priority_key = lambda process: process.get_priority()

    def _put(self, process):
        process_age = len(process.get_execution_history())
        key = self._key(process)
        priority_key = self._priority_key(process)
        heapq.heappush(self.queue, (process_age, key, priority_key, self._index, process))
        self._index += 1

    def _get(self):
        # The object itself is the fifth element
        # in the tuple.
        try:
            process = heapq.heappop(self.queue)
            return process[4]
        except IndexError:
            return None

    def peek(self):
        if len(self.queue) == 0:
            return None
        
        return self.queue[0][4]


class ArrivalQueue(WaitQueue):
    def __init__(self, max_size=0):
        super().__init__(max_size=0)

    def get_process(self, arrival_time, block=True, timeout=None):
        new_process = self.peek()
        if new_process is not None and arrival_time == new_process.get_arrival_time():
            return self.get(block, timeout)

        return None
