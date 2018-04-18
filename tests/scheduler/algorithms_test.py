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

    def _test_algorithms(self, algorithm, expected_pid_order):
        scheduled_processes = algorithm(self.processes)
        assert scheduled_processes.qsize() == len(expected_pid_order)

        pid_index = 0
        while not scheduled_processes.empty():
            assert scheduled_processes.get().get_pid() == expected_pid_order[pid_index]
            pid_index += 1

    def test_fcfs(self):
        self._test_algorithms(algorithms.fcfs, [0, 1, 2, 3, 4])

    def test_sjf(self):
        self._test_algorithms(algorithms.sjf, [4, 1, 3, 0, 2])

    def test_non_preemptive(self):
        self._test_algorithms(algorithms.non_preemptive, [0, 2, 4, 1, 3])

    def test_preemptive(self):
        self._test_algorithms(algorithms.preemptive, [0, 1, 2, 4, 1, 0, 3])

