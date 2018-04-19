#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import queue

from mlfq_sim.ds.scheduling import ScheduleItem
from mlfq_sim.ds.scheduling import WaitQueue
from mlfq_sim.ds.scheduling import ArrivalQueue


def fcfs(processes):
    return sortably_schedule(processes, lambda process: process.get_arrival_time())


def sjf(processes):
    return sortably_schedule(processes, lambda process: process.get_burst_time())


def srtf(processes):
    return simulation_schedule(processes, 'get_remaining_time', is_preemptive=True, high_number_prio=False)


def non_preemptive(processes):
    return simulation_schedule(processes, 'get_priority')


def preemptive(processes):
    return simulation_schedule(processes, 'get_priority', is_preemptive=True)


def round_robin(processes):
    pass


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


def simulation_schedule(processes, priority_criterion, is_preemptive=False, high_number_prio=True):
    schedule = queue.Queue()
    proxy_processes = copy.deepcopy(processes)

    arrival_queue = ArrivalQueue()

    # Here, we're negating the process priority criterion if we follow the higher number, higher priority
    # scheme since priority queues sort ascendingly. Having a smaller priority criterion will make the
    # wait queue put the item closer to the front of the queue. We negate the item's priority so that the
    # items with a higher priority gets placed closer to the front. Essentially, we are exploiting the
    # aforementioned behaviour of the queue. This would have been easier done, implementation-wise, if we
    # utilized the low number, high priority scheme.
    #
    # On the other hand, if we want to follow a lower number, higher priority scheme (such is the case
    # in the SRTF algorithm, where a process with a shorter burst time gets higher priority), there is no
    # need to negate the priority criterion.
    wait_queue = WaitQueue(
        key=lambda process: (-getattr(process, priority_criterion)() if high_number_prio
                             else getattr(process, priority_criterion)())
    )
    # Populate the arrival queue.
    for proxy_process in proxy_processes:
        arrival_queue.put(proxy_process)

    if high_number_prio:
        comparison_func = _is_greater_than
    else:  # Sp we do the low number, higher priority thing that it is in SRTF.
        comparison_func = _is_less_than

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

                if is_preemptive:
                    if not wait_queue.empty():
                        new_process = wait_queue.get()
                    else:
                        new_process = None

                    # New process should preempt the current process since it has
                    # a higher priority.
                    if new_process is not None:
                        if comparison_func(getattr(new_process, priority_criterion)(),
                                           getattr(curr_process, priority_criterion)()):
                            schedule.put(ScheduleItem(curr_process.get_pid(),
                                                      process_start,
                                                      run_time - process_start))
                            wait_queue.put(curr_process)
                            curr_process = new_process
                            process_start = run_time
                        else:
                            # Back to gul... waiting queue now.
                            wait_queue.put(new_process)

            curr_process.execute(process_start, 1, record=False)
            run_time += 1
            if curr_process.get_remaining_time() == 0:
                schedule.put(ScheduleItem(curr_process.get_pid(),
                                          process_start,
                                          run_time - process_start))

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
                if comparison_func(getattr(new_process, priority_criterion)(),
                                   getattr(curr_process, priority_criterion)()()):
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


def _is_greater_than(a, b):
    if a > b:
        return True

    return False

def _is_less_than(a, b):
    if a < b:
        return True

    return False