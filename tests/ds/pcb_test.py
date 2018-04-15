#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from mlfq_sim.ds import ProcessControlBlock

class TestProcessControlBlock:
    @classmethod
    def setup_class(self):
        self.pcb = ProcessControlBlock(0, 12, 12, 1)

    def test_repr(self):
        assert repr(self.pcb) == 'A Generic Process (pid 0)\n' \
                                 'Arrival: 12\tBurst: 12\tPriority: 1'

    def test_pid(self):
        assert self.pcb.get_pid() == 0

    def test_arrival_time(self):
        assert self.pcb.get_arrival_time() == 12

    def test_burst_time(self):
        assert self.pcb.get_burst_time() == 12

    def test_remaining_time(self):
        assert self.pcb.get_remaining_time() == 12

    def test_priority(self):
        assert self.pcb.get_priority() == 1

    def test_execute_func(self):
        # Test that we get the correct remaining time after executing
        # the process starting at 12 for 6 units.
        self.pcb.record_execution(12, 6)
        assert self.pcb.get_remaining_time() == 6

        # Test that we do not reduce the remaining time when the start
        # time is less than the time when the process was last executed.
        with pytest.raises(ProcessControlBlock.ExecutionRecordingException) as ee_info:
            self.pcb.record_execution(11, 6)
        
        with pytest.raises(ProcessControlBlock.ExecutionRecordingException) as ee_info:
            self.pcb.record_execution(12, 6)

        with pytest.raises(ProcessControlBlock.ExecutionRecordingException) as ee_info:
            self.pcb.record_execution(13, 5)
        
        assert self.pcb.get_remaining_time() == 6

        execution_history_item = self.pcb.get_execution_history()[0]
        assert execution_history_item.get_start() == 12
        assert execution_history_item.get_length() == 6
        assert execution_history_item.get_end() == 18

        self.pcb.record_execution(20, 6)
        assert len(self.pcb.get_execution_history()) == 2

        with pytest.raises(ProcessControlBlock.ExecutionRecordingException) as ee_info:
            self.pcb.record_execution(11, 6)
