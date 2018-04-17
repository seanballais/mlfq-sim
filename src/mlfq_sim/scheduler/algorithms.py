#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
import copy
import queue

from mlfq_sim.ds.scheduling import ScheduleItem


def queue_by_arrival(processes):
    proxy_processes = copy.deepcopy(processes)
    proxy_processes.sort(key=lambda process: process.get_arrival_time())
    q = queue.Queue()
    for process in proxy_processes:
        q.put(process)

    return q

def sortably_schedule(processes, sort_criterion):
    schedule = queue.Queue()
    proxy_processes = copy.deepcopy(processes)

    process_start = 0
    sorted_processes = sorted(proxy_processes,
                              key=sort_criterion)
    for process in sorted_processes:
        schedule.put(ScheduleItem(process.get_pid(),
                                  process_start,
                                  process.get_burst_time()))
        process_start += process.get_burst_time()

    return schedule


def fcfs(processes):
    return sortably_schedule(processes, lambda process: process.get_arrival_time())

def sjf(processes):
    return sortably_schedule(processes, lambda process: process.get_burst_time())

def srtf(processes):
    pass

def non_preemptive(processes):
    pass

def preemptive(processes):
    pass

def round_robin(processes):
    pass
