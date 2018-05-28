#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum

from mlfq_sim.ds.scheduling import ArrivalQueue


class MLFQQueue:
    def __init__(self, scheduling_algorithm, quanta=0):
        self.scheduling_algorithm = scheduling_algorithm
        self.processes = []
        self.quanta = quanta

    def has_processes(self):
        return len(self.processes) > 0

    def add_process(self, process):
        self.processes.append(process)

    def execute(self, time_allotment, start_time):
        if self.quanta > 0:
            (schedule,
             arrival_queue,
             wait_queue,
             promoted_processes,
             demoted_processes,
             run_time
             ) = self.scheduling_algorithm(self.processes, quanta=self.quanta,
                                           time_allotment=time_allotment, start_time=start_time)
        else:
            (schedule,
             arrival_queue,
             wait_queue,
             promoted_processes,
             demoted_processes,
             run_time
             ) = self.scheduling_algorithm(self.processes, time_allotment=time_allotment, start_time=start_time)

        self.processes = []

        return (schedule,
                arrival_queue,
                wait_queue,
                promoted_processes,
                demoted_processes,
                run_time
                )


class QueuingScheme(Enum):
    higher_over_lower = 0
    fixed_time_slots = 1


class MLFQ:
    def __init__(self, processes, queues, time_slot=0):
        self.processes = processes
        self.queues = queues

        self.arrival_times = set()
        self.arrival_queue = ArrivalQueue()
        for process in processes:
            self.arrival_times.add(process.get_arrival_time())
            self.arrival_queue.put(process)

        self.arrival_times = sorted(list(self.arrival_times))

        if time_slot > 0:
            # Queuing scheme is fixed time slot.
            self.queuing_scheme = QueuingScheme.fixed_time_slots
        elif time_slot == 0:
            self.queuing_scheme = QueuingScheme.higher_over_lower
        else:
            raise ValueError('time_slot can never be a negative number.')

    def simulate(self):
        if self.queuing_scheme == QueuingScheme.higher_over_lower:
            return self._schedule_higher_over_lower()
        else:
            return self._schedule_fixed_time_slots()

    def _schedule_higher_over_lower(self):
        schedule = []
        current_queue_index = 0
        run_time = 0
        time_allotment = 0

        if len(self.queues) == 1:
            while not self.arrival_queue.empty():
                self.queues[0].add_process(self.arrival_queue.get())

            schedule, _, _, _, _, run_time = self.queues[0].execute(0, 0)
        else:
            while not self.arrival_queue.empty() or self._queues_has_processes():
                preemption_time = self._nearest_preemption_time(run_time)
                current_queue = self.queues[current_queue_index]

                if current_queue_index == 0:
                    while not self.arrival_queue.empty():
                        current_queue.add_process(self.arrival_queue.get())

                traversed_queues = 0
                found_queue_with_processes = True
                while not current_queue.has_processes():
                    current_queue_index = (current_queue_index + 1) % len(self.queues)
                    current_queue = self.queues[current_queue_index]
                    traversed_queues += 1

                    if traversed_queues == len(self.queues):
                        found_queue_with_processes = False
                        break

                if not found_queue_with_processes:
                    run_time = preemption_time
                    current_queue_index = 0
                    continue

                (queue_schedule,
                 arrival_queue,
                 wait_queue,
                 promoted_processes,
                 demoted_processes,
                 run_time
                 ) = current_queue.execute(time_allotment, run_time)

                schedule += queue_schedule

                for process in arrival_queue:
                    self.arrival_queue.put(process)

                for process in wait_queue:
                    current_queue.add_process(process)

                for process in promoted_processes:
                    self.queues[max(0, current_queue_index - 1)].add_process(process)

                for process in demoted_processes:
                    self.queues[min(len(self.queues) - 1, current_queue_index + 1)].add_process(process)

                if preemption_time is not None:
                    if preemption_time - run_time > 0:
                        # Hoooo boi, we got space to move to the next queue.
                        # No need to worry about the time in the next queues.
                        current_queue_index = min(len(self.queues) - 1, current_queue_index + 1)
                        time_allotment = preemption_time - run_time
                    else:
                        # We gotta go back to the top!
                        current_queue_index = 0
                        time_allotment = 0
                else:
                    time_allotment = 0

        return self._merge_same_adjacent_elements(schedule), self.processes, run_time

    def _schedule_fixed_time_slots(self):
        return 1, 2, 3

    def _queues_has_processes(self):
        for queue in self.queues:
            if queue.has_processes():
                return True

        return False

    def _nearest_preemption_time(self, run_time):
        if len(self.arrival_times) > 0:
            for time in self.arrival_times:
                if time > run_time:
                    return time

        return None

    @staticmethod
    def _merge_same_adjacent_elements(element_list):
        new_list = []
        if len(element_list) > 0:
            current_element = element_list[0]
            new_list.append(current_element)
            for index in range(1, len(element_list)):
                if current_element != element_list[index]:
                    current_element = element_list[index]
                    new_list.append(current_element)

        return new_list
