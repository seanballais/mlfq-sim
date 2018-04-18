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


class WaitQueue(queue.PriorityQueue):
    def __init__(self, key=lambda process: process.get_arrival_time(), max_size=0):
        super().__init__(max_size)
        self._index = 0
        self._key = key

    def _put(self, process):
        heapq.heappush(self.queue, (self._key(process), self._index, process))
        self._index += 1

    def _get(self):
        # The object itself is the third element
        # in the tuple.
        return heapq.heappop(self.queue)[2]

    def peek(self):
        return self.queue[0]


class ArrivalQueue(WaitQueue):
    def __init__(self, max_size=0):
        super().__init__(max_size)

    def get_process(self, arrival_time, block=True, timeout=None):
        if arrival_time == self.peek().get_arrival_time():
            return self.get(block, timeout)

        return None