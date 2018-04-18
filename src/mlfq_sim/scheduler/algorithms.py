#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import queue

from mlfq_sim.ds.scheduling import ScheduleItem
from mlfq_sim.ds.scheduling import WaitQueue
from mlfq_sim.ds.scheduling import ArrivalQueue


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
    schedule_tmp = []
    proxy_processes = copy.deepcopy(processes)

    arrival_queue = ArrivalQueue()
    wait_queue = WaitQueue(key=lambda process: -process.get_priority())

    # Populate the arrival queue.
    for proxy_process in proxy_processes:
        arrival_queue.put(proxy_process)

    # Time to schedule.
    run_time = 0
    process_start = 0
    curr_process = arrival_queue.get_process(run_time)
    while not arrival_queue.empty() or not wait_queue.empty() or curr_process is not None:
        if curr_process is not None:
            new_process = arrival_queue.get_process(run_time)
            if new_process is not None:
                # This means that there is a process that has arrived while there
                # is process currently running. We also better check if there are
                # more processes that arrived.
                while new_process is not None:
                    wait_queue.put(new_process)
                    new_process = arrival_queue.get_process(run_time)

            curr_process.execute(process_start, 1, record=False)
            run_time += 1
            if curr_process.get_remaining_time() == 0:
                schedule.put(ScheduleItem(curr_process.get_pid(),
                                          process_start,
                                          curr_process.get_burst_time()))
                schedule_tmp.append(curr_process)

                # We can safely get from the wait queue since at this point,
                # any newly arrived processes have been placed in the
                # wait queue.
                if not wait_queue.empty():
                    # This goes to an infinite loop if we don't check the queue's size.
                    # We should investigate this. Sean, investigate it.
                    curr_process = wait_queue.get()
                else:
                    curr_process = None
                process_start = run_time
        else:
            # There is no currently running process.
            # Let's check the arrival queue first.
            new_process = arrival_queue.get_process(run_time)
            if not wait_queue.empty():
                waiting_process = wait_queue.get()
            else:
                waiting_process = None

            if new_process is not None and waiting_process is not None:
                if new_process.get_priority() > waiting_process.get_priority():
                    curr_process = new_process
                    wait_queue.put(waiting_process)
                else:
                    # We give higher precedence to those waiting in
                    # the queue if they have the same priority
                    # to prevent starvation.
                    curr_process = waiting_process
                    wait_queue.put(new_process)
        
                process_start = run_time

            run_time += 1

    return schedule

def preemptive(processes):
    pass

def round_robin(processes):
    pass
