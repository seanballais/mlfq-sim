#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import queue

from mlfq_sim.ds.scheduling import ScheduleItem
from mlfq_sim.ds.scheduling import WaitQueue
from mlfq_sim.ds.scheduling import ArrivalQueue
from mlfq_sim.ds.scheduling import PeekableQueue


def fcfs(processes):
    return _simulate_schedule(processes, 'get_arrival_time', high_number_prio=False)


def sjf(processes):
    return _simulate_schedule(processes, 'get_burst_time', high_number_prio=False)


def srtf(processes):
    return _simulate_schedule(processes, 'get_remaining_time', is_preemptive=True, high_number_prio=False)


def non_preemptive(processes):
    return _simulate_schedule(processes, 'get_priority')


def preemptive(processes):
    return _simulate_schedule(processes, 'get_priority', is_preemptive=True)


def round_robin(processes, quanta=5):
    schedule = queue.Queue()
    proxy_processes = copy.deepcopy(processes)
    proxy_processes = sorted(proxy_processes, key=lambda process: process.get_arrival_time())

    ready_queue = PeekableQueue()
    for proxy_process in proxy_processes:
        ready_queue.put(proxy_process)

    run_time = 0
    process_start = 0
    quanta_counter = 0
    curr_process = None
    encountered_processes = set()
    while not ready_queue.empty():
        if curr_process is None:
            if ready_queue.peek() is not None:
                if (ready_queue.peek().get_arrival_time() <= run_time
                   or ready_queue.peek().get_pid() in encountered_processes):
                    curr_process = ready_queue.get()
                    encountered_processes.add(curr_process.get_pid())
                    process_start = run_time
                else:
                    run_time += 1
                    continue
            else:
                # No process for us yet. :(
                # Let's move on for now.
                run_time += 1
                continue

        while quanta_counter < quanta and curr_process.get_remaining_time() > 0:
            curr_process.execute(run_time, 1)
            run_time += 1
            quanta_counter += 1

        schedule.put(ScheduleItem(curr_process.get_pid(),
                                  process_start,
                                  run_time - process_start))

        if curr_process.get_remaining_time() > 0:
            # Still got stuff to do.
            ready_queue.put(curr_process)

        curr_process = None
        quanta_counter = 0

    return schedule


def _simulate_schedule(processes, priority_criterion, is_preemptive=False, high_number_prio=True):
    schedule = queue.Queue()
    proxy_processes = copy.deepcopy(processes)
    proxy_processes = sorted(proxy_processes, key=lambda process: process.get_arrival_time())

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
    while not arrival_queue.empty() or not wait_queue.empty():
        curr_process = arrival_queue.get_process(run_time)
        if curr_process is None:
            newly_arrived_process = arrival_queue.get_process(run_time)
            if not wait_queue.empty():
                waiting_process = wait_queue.get()
            else:
                waiting_process = None

            if newly_arrived_process is not None and waiting_process is not None:
                if comparison_func(getattr(newly_arrived_process, priority_criterion)(), getattr(waiting_process, priority_criterion)()):
                    # We will use the newly arrived process.
                    curr_process = newly_arrived_process
                    wait_queue.put(waiting_process)
                else:
                    # We will use the waiting process.
                    curr_process = waiting_process
                    wait_queue.put(newly_arrived_process)
            elif waiting_process is not None and newly_arrived_process is None:
                curr_process = waiting_process
            elif newly_arrived_process is not None and waiting_process is None:
                curr_process = newly_arrived_process
            else:
                curr_process = None
                run_time += 1
                continue

        process_start = run_time
        while curr_process.get_remaining_time() > 0:
            newly_arrived_process = arrival_queue.get_process(run_time)
            if newly_arrived_process is not None:
                if is_preemptive:
                    if comparison_func(getattr(curr_process, priority_criterion)(), getattr(newly_arrived_process, priority_criterion)()):
                        # We will still use the current process since it has higher priority.
                        # So better put the newly arrived process to the wait queue.
                        wait_queue.put(newly_arrived_process)
                    else:
                        # Pre-empt the current process.
                        schedule.put(ScheduleItem(curr_process.get_pid(),
                                                  process_start,
                                                  run_time - process_start))
                        wait_queue.put(curr_process)
                        curr_process = newly_arrived_process
                        process_start = run_time
                else:
                    # Since we are not pre-empting processes, we're just gonna put it
                    # in the wait queue.
                    wait_queue.put(newly_arrived_process)

            # Well, execute current process.
            curr_process.execute(run_time, 1)
            run_time += 1

        schedule.put(ScheduleItem(curr_process.get_pid(),
                                  process_start,
                                  run_time - process_start))
        curr_process = None

    return schedule


def _is_greater_than(a, b):
    if a > b:
        return True

    return False


def _is_less_than(a, b):
    if a < b:
        return True

    return False
