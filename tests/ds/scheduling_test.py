#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from mlfq_sim.ds.pcb import ProcessControlBlock
from mlfq_sim.ds.scheduling import ScheduleItem
from mlfq_sim.ds.scheduling import WaitQueue
from mlfq_sim.ds.scheduling import ArrivalQueue


class TestScheduleItem:
    @classmethod
    def setup_class(self):
        self.item = ScheduleItem(0, 0, 3)

    def test_pid(self):
        assert self.item.get_pid() == 0

    def test_start_time(self):
        assert self.item.get_start_time() == 0

    def test_length(self):
        assert self.item.get_length() == 3

    def test_end(self):
        assert self.item.get_end() == 3


class TestWaitQueue:
    @classmethod
    def setup_class(self):
        self.queue = WaitQueue()

    def test__get(self):
        assert self.queue._get() is None


class TestArrivalQueue:
    @classmethod
    def setup_class(self):
        self.queue = ArrivalQueue()

    def test_get_process(self):
        assert self.queue.get_process(0) == None

        test_process = ProcessControlBlock(0, 0, 1, 1)
        self.queue.put(test_process)

        assert self.queue.get_process(0) == test_process
