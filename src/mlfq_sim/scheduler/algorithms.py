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


class FCFS(SchedulingAlgorithm):
    def schedule(self, processes):
        schedule = queue.Queue(0)

        process_start = 0
        sorted_processes = sorted(processes,
                                  key=lambda process: process.get_arrival_time())
        for process in sorted_processes:
            schedule.put(ScheduleItem(process.get_pid(),
                                      process_start,
                                      process.get_length()))
            process_start += process.get_length()

        return schedule


class SJF(SchedulingAlgorithm):
    def schedule(self, processes):
        schedule = queue.Queue(0)

        process_start = 0
        sorted_processes = sorted(processes,
                                  key=lambda process: process.get_arrival_time())
        for process in sorted_processes:
            schedule.put(ScheduleItem(process.get_pid(),
                                      process_start,
                                      process.get_length()))
            process_start += process.get_length()

        return schedule


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
