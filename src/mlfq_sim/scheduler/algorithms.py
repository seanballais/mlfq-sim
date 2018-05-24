#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import queue

from mlfq_sim.ds.scheduling import WaitQueue
from mlfq_sim.ds.scheduling import ArrivalQueue


def fcfs(processes, additional_processes=list(), time_allotment=0, start_time=0):
    return _simulate_schedule(processes, 'get_arrival_time',
                              additional_processes=additional_processes,
                              high_number_prio=False, time_allotment=time_allotment, start_time=start_time)


def sjf(processes, additional_processes=list(), time_allotment=0, start_time=0):
    return _simulate_schedule(processes, 'get_burst_time',
                              additional_processes=additional_processes,
                              high_number_prio=False, time_allotment=time_allotment, start_time=start_time)


def srtf(processes, additional_processes=list(), time_allotment=0, start_time=0):
    return _simulate_schedule(processes, 'get_remaining_time',
                              additional_processes=additional_processes,
                              is_preemptive=True, high_number_prio=False, time_allotment=time_allotment,
                              start_time=start_time)


def non_preemptive(processes, additional_processes=list(), time_allotment=0, start_time=0):
    return _simulate_schedule(processes, 'get_priority',
                              additional_processes=additional_processes, time_allotment=time_allotment,
                              start_time=start_time)


def preemptive(processes, additional_processes=list(), time_allotment=0, start_time=0):
    return _simulate_schedule(processes, 'get_priority',
                              additional_processes=additional_processes,
                              is_preemptive=True, time_allotment=time_allotment, start_time=start_time)


def round_robin(processes, additional_processes=list(), quanta=5, time_allotment=0, start_time=0):
    # Currently limited to one process where time unit.
    schedule = []

    ready_queue = queue.Queue()
    arrival_queue = ArrivalQueue()
    promoted_processes = []
    demoted_processes = []

    for process in (processes + additional_processes):
        arrival_queue.put(process)

    run_time = 0
    quanta_counter = 0
    remaining_time = time_allotment
    while not ready_queue.empty() or not arrival_queue.empty():
        if remaining_time <= 0 < time_allotment:
            # Not adding remaining_time in the while condition since remaining_time only matters
            # if there is a time_allotment set.
            break

        curr_process = arrival_queue.get_process(run_time)

        if curr_process is None:
            if not ready_queue.empty():
                curr_process = ready_queue.get()
            else:
                run_time += 1
                continue
        else:
            ready_queue.put(curr_process)
            curr_process = ready_queue.get()

        while quanta_counter < quanta and curr_process.get_remaining_time() > 0:
            if remaining_time <= 0 < time_allotment:
                # Not adding remaining_time in the while condition since remaining_time only matters
                # if there is a time_allotment set.
                break

            curr_process.execute(run_time, 1)

            newly_arrived_process = arrival_queue.get_process(run_time)
            while newly_arrived_process is not None:
                ready_queue.put(newly_arrived_process)
                newly_arrived_process = arrival_queue.get_process(run_time)

            run_time += 1
            quanta_counter += 1

        if curr_process.get_remaining_time() > 0:
            if quanta_counter > 0:
                promoted_processes.append(curr_process)
            else:
                demoted_processes.append(curr_process)

        schedule.append(curr_process.get_pid())

        quanta_counter = 0

    return (schedule,
            _queue_to_list(arrival_queue),
            _queue_to_list(ready_queue),
            promoted_processes,
            demoted_processes,
            run_time
            )


def _simulate_schedule(processes, priority_criterion,
                       additional_processes=list(), time_allotment=0, is_preemptive=False, high_number_prio=True,
                       start_time=0):
    # Currently limited to one process where time unit.
    schedule = []

    arrival_queue = ArrivalQueue()
    promoted_processes = []

    # `demoted_processes` will always be empty unless you use round robin. Kept to provide consistency with the
    # round robin algorithm.
    demoted_processes = []

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
        key=lambda _process: (-getattr(_process, priority_criterion)() if high_number_prio
                              else getattr(_process, priority_criterion)())
    )

    # Populate wait queue for any already processed processes.
    for process in additional_processes:
        wait_queue.put(process)

    # Populate the arrival queue.
    for process in processes:
        arrival_queue.put(process)

    if high_number_prio:
        comparison_func = _is_greater_than
    else:  # Sp we do the low number, higher priority thing that it is in SRTF.
        comparison_func = _is_less_than

    # Time to schedule.
    run_time = start_time
    remaining_time = time_allotment
    while not arrival_queue.empty() or not wait_queue.empty():
        if remaining_time <= 0 < time_allotment:
            # Not adding remaining_time in the while condition since remaining_time only matters
            # if there is a time_allotment set.
            break

        # Capture all processes arriving at the same time.
        new_process = arrival_queue.get_process(run_time)
        while new_process is not None:
            wait_queue.put(new_process)
            new_process = arrival_queue.get_process(run_time)

        if not wait_queue.empty():
            curr_process = wait_queue.get()
        else:
            run_time += 1

            if time_allotment > 0:
                remaining_time -= 1

            continue

        while curr_process.get_remaining_time() > 0:
            if remaining_time <= 0 < time_allotment:
                break

            newly_arrived_process = arrival_queue.get_process(run_time)
            while newly_arrived_process is not None:
                if is_preemptive:
                    if comparison_func(getattr(curr_process, priority_criterion)(),
                                       getattr(newly_arrived_process, priority_criterion)()):
                        # We will still use the current process since it has higher priority.
                        # So better put the newly arrived process to the wait queue.
                        wait_queue.put(newly_arrived_process)
                    else:
                        # Preempt the current process.
                        schedule.append(curr_process.get_pid())
                        promoted_processes.append(curr_process)
                        curr_process = newly_arrived_process
                else:
                    # Since we are not preempting processes, we're just gonna put it
                    # in the wait queue.
                    wait_queue.put(newly_arrived_process)

                newly_arrived_process = arrival_queue.get_process(run_time)

            # Well, execute current process.
            curr_process.execute(run_time, 1)
            run_time += 1

            if time_allotment > 0:
                remaining_time -= 1

        if curr_process.get_remaining_time() > 0:
            # It was preempted. Promote it.
            promoted_processes.append(curr_process)

        schedule.append(curr_process.get_pid())

    return (schedule,
            _queue_to_list(arrival_queue),
            _queue_to_list(wait_queue),
            promoted_processes,
            demoted_processes,
            run_time
            )


def _queue_to_list(q):
    new_list = []
    while not q.empty():
        new_list.append(q.get())

    return new_list


def _is_greater_than(a, b):
    if a > b:
        return True

    return False


def _is_less_than(a, b):
    if a < b:
        return True

    return False
