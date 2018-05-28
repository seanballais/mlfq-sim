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

        if len(self.queues) == 1:
            while not self.arrival_queue.empty():
                self.queues[0].add_process(self.arrival_queue.get())

            schedule, _, _, _, _, run_time = self.queues[0].execute(0, 0)
        else:
            while not self.arrival_queue.empty() or self._queues_has_processes():
                if len(self.arrival_times) > 0:
                    preemption_time = self.arrival_times.pop(0)
                else:
                    preemption_time = None

                current_queue = self.queues[0]

                (queue_schedule,
                 arrival_queue,
                 wait_queue,
                 promoted_processes,
                 demoted_processes,
                 run_time
                 ) = current_queue.execute(0, run_time)


            """while not self.arrival_queue.empty() or self._queues_has_processes():
                if len(self.arrival_times) > 0:
                    preemption_time = self.arrival_times.pop(0)
                else:
                    preemption_time = None

                # Find the next queue to execute.
                current_queue = self.queues[current_queue_index]
                while not current_queue.has_processes():
                    current_queue_index = (current_queue_index + 1) % len(self.queues)
                    current_queue = self.queues[current_queue_index]

                if preemption_time is not None:
                    time_allotment = preemption_time - run_time

                    for time in range(run_time, preemption_time):
                        process = self.arrival_queue.get_process(time)
                        while process is not None:
                            current_queue.add_process(process)
                            process = self.arrival_queue.get_process(time)
                else:
                    time_allotment = 0

                    # For cases where you just gonna need to get all the processes.
                    while not self.arrival_queue.empty():
                        current_queue.add_process(self.arrival_queue.get())

                (queue_schedule,
                 arrival_queue,
                 wait_queue,
                 promoted_processes,
                 demoted_processes,
                 run_time
                 ) = current_queue.execute(time_allotment, run_time)

                schedule += queue_schedule

                # Set up the other queues.
                for process in arrival_queue:
                    self.arrival_queue.put(process)

                for process in wait_queue:
                    current_queue.add_process(process)

                for process in promoted_processes:
                    self.queues[max(0, current_queue_index - 1)].add_process(process)

                for process in demoted_processes:
                    self.queues[min(len(self.queues) - 1, current_queue_index + 1)].add_process(process)

                if time_allotment == 0:
                    # Continue to the lower queue.
                    current_queue_index = (current_queue_index + 1) % len(self.queues)
                else:
                    # Hooooo boi, go the top queue.
                    current_queue_index = 0

                # Better fill the top queue with the newly arrived process.
                process = self.arrival_queue.get_process(preemption_time)
                if process is not None:
                    self.queues[0].add_process(process)"""

        return self._merge_same_adjacent_elements(schedule), self.processes, run_time

    def _schedule_fixed_time_slots(self):
        return 1, 2, 3

    def _queues_has_processes(self):
        for queue in self.queues:
            if queue.has_processes():
                return True

        return False

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
