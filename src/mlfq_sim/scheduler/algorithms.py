#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
import copy
import queue

from mlfq_sim.ds.scheduling import ScheduleItem
from mlfq_sim.ds.scheduling import WaitQueue


def queue_by_arrival(processes):
    proxy_processes = copy.deepcopy(processes)
    proxy_processes.sort(key=lambda process: (process.get_arrival_time(), process.get_priority()))
    for process in proxy_processes:
        yield process

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
    schedule = queue.Queue()
    proxy_processes = queue_by_arrival(processes)
    wait_queue = WaitQueue(key=lambda process: process.get_priority())


    process_start = 0
    curr_process = next(proxy_processes, None)

    while curr_process is not None or not wait_queue.empty():
        wait_queue.put(curr_process)
        process = wait_queue.get()
        schedule.put(ScheduleItem(process.get_pid(),
                                  process_start,
                                  process.get_burst_time()))

        process_start += process.get_burst_time()
        curr_process = next(proxy_processes, None)

def preemptive(processes):
    pass

def round_robin(processes):
    pass
