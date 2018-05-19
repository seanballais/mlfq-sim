#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from mlfq_sim.ds import ProcessControlBlock
from mlfq_sim.scheduler import algorithms


class TestSchedulingAlgorithms:
    @classmethod
    def setup_class(self):
        self.processes = [ProcessControlBlock(0, 0, 8, 2),
                          ProcessControlBlock(1, 1, 4, 3),
                          ProcessControlBlock(2, 2, 9, 5),
                          ProcessControlBlock(3, 3, 5, 1),
                          ProcessControlBlock(4, 7, 1, 4)]

    def test_fcfs(self):
        self._test_algorithms(algorithms.fcfs, self.processes, [0, 1, 2, 3, 4])

        processes = [ProcessControlBlock(0, 0, 3, 0),
                     ProcessControlBlock(1, 10, 1, 3)]
        self._test_algorithms(algorithms.fcfs, processes, [0, 1])

        processes = [ProcessControlBlock(0, 0, 3, 0)]
        self._test_algorithms(algorithms.fcfs, processes, [0])

    def test_sjf(self):
        self._test_algorithms(algorithms.sjf, self.processes, [0, 4, 1, 3, 2])

        processes = [ProcessControlBlock(0, 0, 3, 0),
                     ProcessControlBlock(1, 10, 1, 3)]
        self._test_algorithms(algorithms.sjf, processes, [0, 1])

        processes = [ProcessControlBlock(0, 0, 3, 0)]
        self._test_algorithms(algorithms.sjf, processes, [0])

    def test_srtf(self):
        self._test_algorithms(algorithms.srtf, self.processes, [0, 1, 3, 4, 3, 0, 2])

        processes = [ProcessControlBlock(0, 0, 3, 0),
                     ProcessControlBlock(1, 10, 1, 3)]
        self._test_algorithms(algorithms.srtf, processes, [0, 1])

        processes = [ProcessControlBlock(0, 0, 3, 0)]
        self._test_algorithms(algorithms.srtf, processes, [0])

    def test_non_preemptive(self):
        self._test_algorithms(algorithms.non_preemptive, self.processes, [0, 2, 4, 1, 3])

        processes = [ProcessControlBlock(0, 0, 3, 0),
                     ProcessControlBlock(1, 10, 1, 3)]
        self._test_algorithms(algorithms.non_preemptive, processes, [0, 1])

        processes = [ProcessControlBlock(0, 0, 3, 0)]
        self._test_algorithms(algorithms.non_preemptive, processes, [0])

    def test_preemptive(self):
        self._test_algorithms(algorithms.preemptive, self.processes, [0, 1, 2, 4, 1, 0, 3])

        processes = [ProcessControlBlock(0, 0, 3, 0),
                     ProcessControlBlock(1, 10, 1, 3)]
        self._test_algorithms(algorithms.preemptive, processes, [0, 1])

        processes = [ProcessControlBlock(0, 0, 3, 0)]
        self._test_algorithms(algorithms.preemptive, processes, [0])

    def test_round_robin(self):
        self._test_algorithms(algorithms.round_robin, self.processes, [0, 1, 2, 3, 4, 0, 2], 5)

        # Test process scheduling with arrival time quite spread apart.
        processes = [ProcessControlBlock(0, 0, 3, 0),
                     ProcessControlBlock(1, 10, 1, 3)]
        self._test_algorithms(algorithms.round_robin, processes, [0, 1])

        # Test with only one process.
        processes = [ProcessControlBlock(0, 0, 3, 0)]
        self._test_algorithms(algorithms.round_robin, processes, [0])

    @staticmethod
    def _test_algorithms(algorithm, processes, expected_pid_order, quanta=0):
        if quanta > 0:
            scheduled_processes = algorithm(processes, quanta)
        else:
            scheduled_processes = algorithm(processes)

        assert scheduled_processes.qsize() == len(expected_pid_order)

        pid_index = 0
        while not scheduled_processes.empty():
            assert scheduled_processes.get().get_pid() == expected_pid_order[pid_index]
            pid_index += 1
