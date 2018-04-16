#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
import copy
import queue
import heapq


class SchedulingAlgorithm:
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


    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def schedule(self, processes):
        pass


class SortableScheduling(SchedulingAlgorithm):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def _get_sort_criterion(self, process):
        pass

    def schedule(self, processes):
        schedule = queue.Queue()
        proxy_processes = copy.deepcopy(processes)

        process_start = 0
        sorted_processes = sorted(proxy_processes,
                                  key=self._get_sort_criterion)
        for process in sorted_processes:
            schedule.put(SchedulingAlgorithm.ScheduleItem(process.get_pid(),
                                                          process_start,
                                                          process.get_burst_time()))
            process_start += process.get_burst_time()

        return schedule


class FCFS(SortableScheduling):
    def _get_sort_criterion(self, process):
        return process.get_arrival_time()


class SJF(SortableScheduling):
    def _get_sort_criterion(self, process):
        return process.get_burst_time()


class SRTF(SchedulingAlgorithm):
    class ProcessBurstQueue(queue.PriorityQueue):
        def __init__(self, max_size=0):
            super().__init__(self, max_size)
            self._index = 0

        def _put(self, process):
            heapq.heappush(self.queue, (process.get_remaining_time(), self._index, process))
            self._index += 1

        def _get(self):
            return heapq.heappop(self.queue)[2]  # The object itself is the third element
                                                 # in the tuple.

        def peek(self):
            return self.queue[0]


    def schedule(self, processes):
        schedule = queue.Queue()
        proxy_processes = self._create_process_queue(processes)
        process_queue = self.ProcessBurstQueue()

        while not process_queue.empty() or not proxy_processes.empty():
            curr_process = proxy_processes.get() or process_queue.empty()
    
    def _create_process_queue(self, processes):
        proxy_processes = copy.deepcopy(processes)
        proxy_processes.sort(key=lambda proxy_process: proxy_process.get_arrival_time())
        q = queue.PriorityQueue()
        for process in proxy_processes:
            q.put(process)

        return q


class NonPreemptivePriority(SchedulingAlgorithm):
    def schedule(self, processes):
        pass


class PreemptivePriority(SchedulingAlgorithm):
    def schedule(self, processes):
        pass


class RoundRobin(SchedulingAlgorithm):
    def __init__(self, quantum=5):
        # Had to do this cause we need a time quantum.
        self.quantum = quantum

    def schedule(self, processes):
        pass
