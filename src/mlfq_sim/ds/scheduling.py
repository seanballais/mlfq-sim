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


class MLFQQueue:
    def __init__(self, processes=[], scheduling_algorithm=None):
        self.processes = {}
        for process in processes:
            self.processes[process.get_pid()] = process

        self.scheduling_algorithm = scheduling_algorithm
        self.schedule = None

    def add_process(self, process):
        self.processes[process.get_pid()] = process

    def remove_process(self, pid):
        process = self.processes[pid]
        del self.processes[pid]
        return process

    def set_scheduling_algorithm(self, algorithm):
        self.scheduling_algorithm = algorithm

    def schedule_processes(self, quanta=0):
        listed_processes = []
        for key, value in self.processes.items():
            listed_processes.append(value)

        if quanta > 0:
            self.schedule = self.scheduling_algorithm(listed_processes, quanta)
        else:
            self.schedule = self.scheduling_algorithm(listed_processes)

    def get_schedule(self):
        return self.schedule


    def empty(self):
        return len(self.processes) == 0


class PeekableQueue(queue.Queue):
    def __init__(self, max_size=0):
        super().__init__(max_size)

    def peek(self):
        if len(self.queue) == 0:
            return None

        return self.queue[0]


class WaitQueue(queue.PriorityQueue):
    def __init__(self, key=lambda process: process.get_arrival_time(), max_size=0):
        super().__init__(max_size)
        self._index = 0
        self._key = key
        self._priority_key = lambda process: process.get_priority()

    def _put(self, process):
        heapq.heappush(self.queue, (self._key(process),
                                    self._priority_key(process),
                                    self._index,
                                    process))
        self._index += 1

    def _get(self):
        # The object itself is the fourth element
        # in the tuple.
        try:
            process = heapq.heappop(self.queue)
            return process[3]
        except IndexError:
            return None

    def peek(self):
        if len(self.queue) == 0:
            return None
        
        return self.queue[0][3]

    def to_str(self):
        return str(self.queue)


class ArrivalQueue(WaitQueue):
    def __init__(self, max_size=0):
        super().__init__(max_size=0)

    def get_process(self, arrival_time, block=True, timeout=None):
        new_process = self.peek()
        if new_process is not None and arrival_time == new_process.get_arrival_time():
                return self.get(block, timeout)

        return None
