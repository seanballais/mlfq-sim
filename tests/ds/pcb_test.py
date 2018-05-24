#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from mlfq_sim.ds import ProcessControlBlock
from mlfq_sim.ds import pcb


class TestExecutionHistoryItem:
    def test_item_equality(self):
        item1 = pcb.ExecutionHistoryItem(0, 1)
        item1a = pcb.ExecutionHistoryItem(0, 1)
        item2 = pcb.ExecutionHistoryItem(0, 2)

        assert item1 == item1a
        assert item1 != item2


class TestProcessControlBlock:
    @classmethod
    def setup_class(self):
        self.pcb = ProcessControlBlock(0, 12, 12, 1)

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
        self.pcb.execute(12, 6)
        assert self.pcb.get_remaining_time() == 6

        # Test that we do not reduce the remaining time when the start
        # time is less than the time when the process was last executed.
        with pytest.raises(pcb.ExecutionRecordingException) as ee_info:
            self.pcb.execute(11, 6)
        
        with pytest.raises(pcb.ExecutionRecordingException) as ee_info:
            self.pcb.execute(12, 6)

        with pytest.raises(pcb.ExecutionRecordingException) as ee_info:
            self.pcb.execute(13, 5)
        
        assert self.pcb.get_remaining_time() == 6

        execution_history_item = self.pcb.get_execution_history()[0]
        assert execution_history_item.get_start() == 12
        assert execution_history_item.get_length() == 6
        assert execution_history_item.get_end() == 18

        self.pcb.execute(20, 6)
        assert len(self.pcb.get_execution_history()) == 2

        with pytest.raises(pcb.ExecutionRecordingException) as ee_info:
            self.pcb.execute(11, 6)

    def test_execute_history(self):
        test_pcb = ProcessControlBlock(0, 0, 3, 1)

        test_pcb.execute(0, 1)
        test_pcb.execute(1, 1)
        assert len(test_pcb.get_execution_history()) == 1

        test_pcb.execute(3, 1)
        assert len(test_pcb.get_execution_history()) == 2
        
        execution_history = test_pcb.get_execution_history()
        assert execution_history[0].get_start() == 0
        assert execution_history[0].get_length() == 2
        assert execution_history[0].get_end() == 2
        assert execution_history[1].get_start() == 3
        assert execution_history[1].get_length() == 1
        assert execution_history[1].get_end() == 4
        assert test_pcb.get_remaining_time() == 0

    def test_no_history_recording(self):
        test_pcb = ProcessControlBlock(0, 0, 1, 1)
        
        test_pcb.execute(0, 1, record=False)
        assert len(test_pcb.get_execution_history()) == 0

    def test_pcb_equality(self):
        pcb1 = ProcessControlBlock(0, 0, 5, 0)
        pcb1a = ProcessControlBlock(0, 0, 5, 0)
        pcb2 = ProcessControlBlock(0, 1, 5, 0)

        assert pcb1 == pcb1a
        assert pcb1 != pcb2
