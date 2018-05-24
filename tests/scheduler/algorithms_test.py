#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mlfq_sim.ds import ProcessControlBlock
from mlfq_sim.scheduler import algorithms


class TestSchedulingAlgorithms:
    def test_fcfs(self):
        # Test for case where there is no overlapping arrival times.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 5, 5, 0)]
        assert algorithms.fcfs(processes) == ([0, 1], [], [], [], [], 10)

        # Test for case where there is one overlapping arrival times.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 3, 5, 0)]
        assert algorithms.fcfs(processes) == ([0, 1], [], [], [], [], 10)

        # Test for case where there are same arrival times for two processes but no running process.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 0, 5, 0)]
        assert algorithms.fcfs(processes) == ([0, 1], [], [], [], [], 10)

        # Test for case where there are two processes that arrived at the same time while another process is running.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 3, 5, 0),
                     ProcessControlBlock(2, 3, 5, 0)]
        assert algorithms.fcfs(processes) == ([0, 1, 2], [], [], [], [], 15)

        # Test for case where there is a gap between process arrivals.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 10, 5, 0)]
        assert algorithms.fcfs(processes) == ([0, 1], [], [], [], [], 15)

        # Test for case where queue is preempted because the time slot was already filled up.
        processes = [ProcessControlBlock(0, 0, 5, 0)]
        resulting_process = ProcessControlBlock(0, 0, 5, 0)
        resulting_process.execute(0, 2)
        assert algorithms.fcfs(processes, time_allotment=2) == ([0], [], [], [resulting_process], [], 2)

        # Test for case where queue is preempted even though there are still processes arriving.
        processes = [ProcessControlBlock(0, 10, 5, 0)]
        assert algorithms.fcfs(processes, time_allotment=5) == ([], [ProcessControlBlock(0, 10, 5, 0)], [], [], [], 5)

        # Test for case where queue is preempted even though there are still processes waiting to have a first run.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 1, 5, 0)]
        promoted_process = ProcessControlBlock(0, 0, 5, 0)
        promoted_process.execute(0, 2)
        assert algorithms.fcfs(processes, time_allotment=2) == ([0],
                                                                [],
                                                                [ProcessControlBlock(1, 1, 5, 0)],
                                                                [promoted_process],
                                                                [],
                                                                2)

        # Test for case where another set of processes are added from another queue.
        processes = [ProcessControlBlock(0, 0, 5, 0)]
        additional_processes = [ProcessControlBlock(1, 1, 5, 0)]
        assert algorithms.fcfs(processes, additional_processes) == ([0, 1], [], [], [], [], 10)

    def test_sjf(self):
        # Test for case where there is no overlapping arrival times.
        # Test for case where there is one overlapping arrival times.
        # Test for case where there are same arrival times for two processes but no running process.
        # Test for case where there are two processes that arrived at the same time while another process is running.
        # Test for case where there is a gap between process arrivals.
        # Test for case where queue is preempted because the time slot was already filled up.
        # Test for case where queue is preempted even though there are still processes arriving.
        # Test for case where queue is preempted even though there are still processes waiting to have a first run.
        # Test for case where another set of processes are added from another queue.
        pass

    def test_srtf(self):
        # Test for case where there is no overlapping arrival times.
        # Test for case where there is one overlapping arrival times.
        # Test for case where there are same arrival times for two processes but no running process.
        # Test for case where there are two processes that arrived at the same time while another process is running.
        # Test for case where there is a gap between process arrivals.
        # Test for case where queue is preempted because the time slot was already filled up.
        # Test for case where queue is preempted even though there are still processes arriving.
        # Test for case where queue is preempted even though there are still processes waiting to have a first run.
        # Test for case where another set of processes are added from another queue.
        pass

    def test_non_preemptive(self):
        # Test for case where there is no overlapping arrival times.
        # Test for case where there is one overlapping arrival times.
        # Test for case where there are same arrival times for two processes but no running process.
        # Test for case where there are two processes that arrived at the same time while another process is running.
        # Test for case where there is a gap between process arrivals.
        # Test for case where queue is preempted because the time slot was already filled up.
        # Test for case where queue is preempted even though there are still processes arriving.
        # Test for case where queue is preempted even though there are still processes waiting to have a first run.
        # Test for case where another set of processes are added from another queue.
        pass

    def test_preemptive(self):
        # Test for case where there is no overlapping arrival times.
        # Test for case where there is one overlapping arrival times.
        # Test for case where there are same arrival times for two processes but no running process.
        # Test for case where there are two processes that arrived at the same time while another process is running.
        # Test for case where there is a gap between process arrivals.
        # Test for case where queue is preempted because the time slot was already filled up.
        # Test for case where queue is preempted even though there are still processes arriving.
        # Test for case where queue is preempted even though there are still processes waiting to have a first run.
        # Test for case where another set of processes are added from another queue.
        pass

    def test_round_robin(self):
        # Test for case where there is no overlapping arrival times.
        # Test for case where there is one overlapping arrival times.
        # Test for case where there are same arrival times for two processes but no running process.
        # Test for case where there are two processes that arrived at the same time while another process is running.
        # Test for case where there is a gap between process arrivals.
        # Test for case where queue is preempted because the time slot was already filled up.
        # Test for case where queue is preempted even though there are still processes arriving.
        # Test for case where queue is preempted even though there are still processes waiting to have a first run.
        # Test for case where another set of processes are added from another queue.
        pass
