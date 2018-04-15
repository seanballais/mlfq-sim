#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
import copy
import queue

from sortedcontainers import SortedList

from mlfq_sim.ds.items import ScheduleItem


class SchedulingAlgorithm:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def schedule(self, processes):
        pass


class SortableScheduling(SchedulingAlgorithm):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_sort_criterion(self, process):
        pass

    def schedule(self, processes):
        schedule = queue.Queue(0)

        process_start = 0
        sorted_processes = sorted(processes,
                                  key=self.get_sort_criterion)
        for process in sorted_processes:
            schedule.put(ScheduleItem(process.get_pid(),
                                      process_start,
                                      process.get_length()))
            process_start += process.get_length()

        return schedule


class FCFS(SortableScheduling):
    def get_sort_criterion(self, process):
        return process.get_arrival_time()


class SJF(SchedulingAlgorithm):
    def get_sort_criterion(self, process):
        return process.get_burst_time()


class SRTF(SchedulingAlgorithm):
    def schedule(self, processes):
        pass


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
