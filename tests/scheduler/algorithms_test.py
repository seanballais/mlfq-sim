#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from mlfq_sim.ds import ProcessControlBlock
from mlfq_sim.scheduler.algorithms import FCFS
from mlfq_sim.scheduler.algorithms import SJF


class TestSchedulingAlgorithms:
    @classmethod
    def setup_class(self):
        self.processes = [ProcessControlBlock(0, 0, 8, 0),
                          ProcessControlBlock(2, 2, 9, 0),
                          ProcessControlBlock(1, 1, 4, 0)]
        self.fcfs = FCFS()
        self.sjf = SJF()

    def test_fcfs(self):
        scheduled_processes = self.fcfs.schedule(self.processes)
        expected_pid_order = [0, 1, 2]
        pid_index = 0
        while not scheduled_processes.empty():
            assert scheduled_processes.get().get_pid() == expected_pid_order[pid_index]
            pid_index += 1

    def test_sjf(self):
        scheduled_processes = self.sjf.schedule(self.processes)
        expected_pid_order = [1, 0, 2]
        pid_index = 0
        while not scheduled_processes.empty():
            assert scheduled_processes.get().get_pid() == expected_pid_order[pid_index]
            pid_index += 1
