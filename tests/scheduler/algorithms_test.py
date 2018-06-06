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
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 5, 5, 0)]
        assert algorithms.sjf(processes) == ([0, 1], [], [], [], [], 10)

        # Test for case where there are overlapping arrival times.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 1, 3, 0)]
        assert algorithms.sjf(processes) == ([0, 1], [], [], [], [], 8)

        # Test for case where there are same arrival times for two processes but no running process.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 0, 3, 0)]
        assert algorithms.sjf(processes) == ([1, 0], [], [], [], [], 8)

        # Test for case where there are two processes that arrived at the same time while another process is running.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 1, 5, 0),
                     ProcessControlBlock(2, 1, 5, 0)]
        assert algorithms.sjf(processes) == ([0, 1, 2], [], [], [], [], 15)

        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 2, 2, 0),
                     ProcessControlBlock(2, 2, 1, 0)]
        assert algorithms.sjf(processes) == ([0, 2, 1], [], [], [], [], 8)

        # Test for case where there is a gap between process arrivals.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 10, 5, 0)]
        assert algorithms.sjf(processes) == ([0, 1], [], [], [], [], 15)

        # Test for case where queue is preempted because the time slot was already filled up.
        processes = [ProcessControlBlock(0, 0, 5, 0)]
        resulting_process = ProcessControlBlock(0, 0, 5, 0)
        resulting_process.execute(0, 2)
        assert algorithms.sjf(processes, time_allotment=2) == ([0], [], [], [resulting_process], [], 2)

        # Test for case where queue is preempted even though there are still processes arriving.
        processes = [ProcessControlBlock(0, 10, 5, 0)]
        assert algorithms.sjf(processes, time_allotment=5) == ([], [ProcessControlBlock(0, 10, 5, 0)], [], [], [], 5)

        # Test for case where queue is preempted even though there are still processes waiting to have a first run.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 1, 5, 0)]
        promoted_process = ProcessControlBlock(0, 0, 5, 0)
        promoted_process.execute(0, 2)
        assert algorithms.sjf(processes, time_allotment=2) == ([0],
                                                               [],
                                                               [ProcessControlBlock(1, 1, 5, 0)],
                                                               [promoted_process],
                                                               [],
                                                               2)

        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 0, 3, 0)]
        promoted_process = ProcessControlBlock(1, 0, 3, 0)
        promoted_process.execute(0, 2)
        assert algorithms.sjf(processes, time_allotment=2) == ([1],
                                                               [],
                                                               [ProcessControlBlock(0, 0, 5, 0)],
                                                               [promoted_process],
                                                               [],
                                                               2)

        # Test for case where another set of processes are added from another queue.
        processes = [ProcessControlBlock(0, 2, 5, 0)]
        additional_processes = [ProcessControlBlock(1, 1, 5, 0)]
        # New processes that have arrived already will tend to be the first ones to be executed.
        assert algorithms.sjf(processes, additional_processes, start_time=1) == ([1, 0], [], [], [], [], 11)

        processes = [ProcessControlBlock(0, 0, 5, 0)]
        additional_processes = [ProcessControlBlock(1, 0, 3, 0)]
        assert algorithms.sjf(processes, additional_processes) == ([1, 0], [], [], [], [], 8)

    def test_srtf(self):
        # Test for case where there is no overlapping arrival times.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 5, 5, 0)]
        assert algorithms.srtf(processes) == ([0, 1], [], [], [], [], 10)

        # Test for case where there are overlapping arrival times.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 1, 3, 0)]
        promoted_process = ProcessControlBlock(0, 0, 5, 0)
        promoted_process.execute(0, 1)
        assert algorithms.srtf(processes) == ([0, 1], [], [], [promoted_process], [], 4)

        processes = [ProcessControlBlock(0, 0, 3, 0),
                     ProcessControlBlock(1, 1, 5, 0)]
        assert algorithms.srtf(processes) == ([0, 1], [], [], [], [], 8)

        # Test for case where there are same arrival times for two processes but no running process.
        processes = [ProcessControlBlock(0, 5, 5, 0),
                     ProcessControlBlock(1, 5, 3, 0)]
        assert algorithms.srtf(processes) == ([1, 0], [], [], [], [], 13)

        # Test for case where there are two processes that arrived at the same time while another process is running.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 1, 5, 0),
                     ProcessControlBlock(2, 1, 5, 0)]
        assert algorithms.srtf(processes) == ([0, 1, 2], [], [], [], [], 15)

        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 2, 2, 0),
                     ProcessControlBlock(2, 2, 1, 0)]
        promoted_process = ProcessControlBlock(0, 0, 5, 0)
        promoted_process.execute(0, 2)
        assert algorithms.srtf(processes) == ([0, 2, 1], [], [], [promoted_process], [], 5)

        # Test for case where there is a gap between process arrivals.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 10, 5, 0)]
        assert algorithms.srtf(processes) == ([0, 1], [], [], [], [], 15)

        # Test for case where queue is preempted because the time slot was already filled up.
        processes = [ProcessControlBlock(0, 0, 5, 0)]
        resulting_process = ProcessControlBlock(0, 0, 5, 0)
        resulting_process.execute(0, 2)
        assert algorithms.srtf(processes, time_allotment=2) == ([0], [], [], [resulting_process], [], 2)

        # Test for case where queue is preempted even though there are still processes arriving.
        processes = [ProcessControlBlock(0, 10, 5, 0)]
        assert algorithms.srtf(processes, time_allotment=5) == ([], [ProcessControlBlock(0, 10, 5, 0)], [], [], [], 5)

        # Test for case where queue is preempted even though there are still processes waiting to have a first run.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 1, 5, 0)]
        promoted_process = ProcessControlBlock(0, 0, 5, 0)
        promoted_process.execute(0, 2)
        assert algorithms.srtf(processes, time_allotment=2) == ([0],
                                                               [],
                                                               [ProcessControlBlock(1, 1, 5, 0)],
                                                               [promoted_process],
                                                               [],
                                                               2)

        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 0, 3, 0)]
        promoted_process = ProcessControlBlock(1, 0, 3, 0)
        promoted_process.execute(0, 2)
        assert algorithms.srtf(processes, time_allotment=2) == ([1],
                                                                [],
                                                                [ProcessControlBlock(0, 0, 5, 0)],
                                                                [promoted_process],
                                                                [],
                                                                2)

        # Test for case where another set of processes are added from another queue.
        processes = [ProcessControlBlock(0, 2, 5, 0)]
        additional_processes = [ProcessControlBlock(1, 1, 5, 0)]
        assert algorithms.srtf(processes, additional_processes, start_time=1) == ([1, 0], [], [], [], [], 11)

        processes = [ProcessControlBlock(0, 0, 5, 0)]
        additional_processes = [ProcessControlBlock(1, 0, 3, 0)]
        assert algorithms.srtf(processes, additional_processes) == ([1, 0], [], [], [], [], 8)

    def test_non_preemptive(self):
        # Test for case where there is no overlapping arrival times.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 5, 5, 0)]
        assert algorithms.non_preemptive(processes) == ([0, 1], [], [], [], [], 10)

        # Test for case where there are overlapping arrival times.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 1, 3, 1)]
        assert algorithms.non_preemptive(processes) == ([0, 1], [], [], [], [], 8)

        # Test for case where there are same arrival times for two processes but no running process.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 0, 3, 1)]
        assert algorithms.non_preemptive(processes) == ([1, 0], [], [], [], [], 8)

        # Test for case where there are two processes that arrived at the same time while another process is running.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 1, 5, 1),
                     ProcessControlBlock(2, 1, 5, 1)]
        assert algorithms.non_preemptive(processes) == ([0, 1, 2], [], [], [], [], 15)

        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 2, 2, 0),
                     ProcessControlBlock(2, 2, 1, 1)]
        assert algorithms.non_preemptive(processes) == ([0, 2, 1], [], [], [], [], 8)

        # Test for case where there is a gap between process arrivals.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 10, 5, 1)]
        assert algorithms.non_preemptive(processes) == ([0, 1], [], [], [], [], 15)

        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 10, 5, 0)]
        assert algorithms.non_preemptive(processes) == ([0, 1], [], [], [], [], 15)

        # Test for case where queue is preempted because the time slot was already filled up.
        processes = [ProcessControlBlock(0, 0, 5, 0)]
        resulting_process = ProcessControlBlock(0, 0, 5, 0)
        resulting_process.execute(0, 2)
        assert algorithms.non_preemptive(processes, time_allotment=2) == ([0], [], [], [resulting_process], [], 2)

        # Test for case where queue is preempted even though there are still processes arriving.
        processes = [ProcessControlBlock(0, 10, 5, 0)]
        assert algorithms.non_preemptive(processes, time_allotment=5) == ([], [ProcessControlBlock(0, 10, 5, 0)],
                                                                          [], [], [], 5)

        # Test for case where queue is preempted even though there are still processes waiting to have a first run.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 1, 5, 0)]
        promoted_process = ProcessControlBlock(0, 0, 5, 0)
        promoted_process.execute(0, 2)
        assert algorithms.non_preemptive(processes, time_allotment=2) == ([0],
                                                                          [],
                                                                          [ProcessControlBlock(1, 1, 5, 0)],
                                                                          [promoted_process],
                                                                          [],
                                                                          2)

        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 0, 3, 1)]
        promoted_process = ProcessControlBlock(1, 0, 3, 1)
        promoted_process.execute(0, 2)
        assert algorithms.non_preemptive(processes, time_allotment=2) == ([1],
                                                                          [],
                                                                          [ProcessControlBlock(0, 0, 5, 0)],
                                                                          [promoted_process],
                                                                          [],
                                                                          2)

        # Test for case where another set of processes are added from another queue.
        processes = [ProcessControlBlock(0, 2, 5, 0)]
        additional_processes = [ProcessControlBlock(1, 1, 5, 0)]
        # New processes that have arrived already will tend to be the first ones to be executed.
        assert algorithms.non_preemptive(processes, additional_processes, start_time=1) == ([1, 0], [], [], [], [], 11)

        processes = [ProcessControlBlock(0, 0, 5, 0)]
        additional_processes = [ProcessControlBlock(1, 0, 3, 1)]
        assert algorithms.non_preemptive(processes, additional_processes) == ([1, 0], [], [], [], [], 8)

    def test_preemptive(self):
        # Test for case where there is no overlapping arrival times.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 5, 5, 0)]
        assert algorithms.preemptive(processes) == ([0, 1], [], [], [], [], 10)

        # Test for case where there are overlapping arrival times.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 1, 3, 1)]
        promoted_process = ProcessControlBlock(0, 0, 5, 0)
        promoted_process.execute(0, 1)
        assert algorithms.preemptive(processes) == ([0, 1], [], [], [promoted_process], [], 4)

        processes = [ProcessControlBlock(0, 0, 3, 1),
                     ProcessControlBlock(1, 1, 5, 0)]
        assert algorithms.preemptive(processes) == ([0, 1], [], [], [], [], 8)

        # Test for case where there are same arrival times for two processes but no running process.
        processes = [ProcessControlBlock(0, 5, 5, 0),
                     ProcessControlBlock(1, 5, 3, 1)]
        assert algorithms.preemptive(processes) == ([1, 0], [], [], [], [], 13)

        # Test for case where there are two processes that arrived at the same time while another process is running.
        processes = [ProcessControlBlock(0, 0, 5, 1),
                     ProcessControlBlock(1, 1, 5, 0),
                     ProcessControlBlock(2, 1, 5, 0)]
        assert algorithms.preemptive(processes) == ([0, 1, 2], [], [], [], [], 15)

        processes = [ProcessControlBlock(0, 0, 5, 1),
                     ProcessControlBlock(1, 2, 2, 2),
                     ProcessControlBlock(2, 2, 1, 3)]
        promoted_process = ProcessControlBlock(0, 0, 5, 1)
        promoted_process.execute(0, 2)
        assert algorithms.preemptive(processes) == ([0, 2, 1], [], [], [promoted_process], [], 5)

        # Test for case where there is a gap between process arrivals.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 10, 5, 0)]
        assert algorithms.preemptive(processes) == ([0, 1], [], [], [], [], 15)

        # Test for case where queue is preempted because the time slot was already filled up.
        processes = [ProcessControlBlock(0, 0, 5, 0)]
        resulting_process = ProcessControlBlock(0, 0, 5, 0)
        resulting_process.execute(0, 2)
        assert algorithms.preemptive(processes, time_allotment=2) == ([0], [], [], [resulting_process], [], 2)

        # Test for case where queue is preempted even though there are still processes arriving.
        processes = [ProcessControlBlock(0, 10, 5, 0)]
        assert algorithms.preemptive(processes, time_allotment=5) == ([],
                                                                      [ProcessControlBlock(0, 10, 5, 0)],
                                                                      [], [], [], 5)

        # Test for case where queue is preempted even though there are still processes waiting to have a first run.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 1, 5, 0)]
        promoted_process = ProcessControlBlock(0, 0, 5, 0)
        promoted_process.execute(0, 2)
        assert algorithms.preemptive(processes, time_allotment=2) == ([0],
                                                                      [],
                                                                      [ProcessControlBlock(1, 1, 5, 0)],
                                                                      [promoted_process],
                                                                      [],
                                                                      2)

        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 0, 3, 1)]
        promoted_process = ProcessControlBlock(1, 0, 3, 1)
        promoted_process.execute(0, 2)
        assert algorithms.preemptive(processes, time_allotment=2) == ([1],
                                                                      [],
                                                                      [ProcessControlBlock(0, 0, 5, 0)],
                                                                      [promoted_process],
                                                                      [],
                                                                      2)

        # Test for case where another set of processes are added from another queue.
        processes = [ProcessControlBlock(0, 2, 5, 0)]
        additional_processes = [ProcessControlBlock(1, 1, 5, 1)]
        assert algorithms.preemptive(processes, additional_processes, start_time=1) == ([1, 0], [], [], [], [], 11)

        processes = [ProcessControlBlock(0, 0, 5, 0)]
        additional_processes = [ProcessControlBlock(1, 0, 3, 1)]
        assert algorithms.preemptive(processes, additional_processes) == ([1, 0], [], [], [], [], 8)

    def test_round_robin(self):
        # Test for case where there is no overlapping arrival times.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 5, 5, 0)]
        assert algorithms.round_robin(processes, quanta=5) == ([0, 1], [], [], [], [], 10)

        # Test for case where there is one overlapping arrival times.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 3, 5, 0)]
        assert algorithms.round_robin(processes, quanta=5) == ([0, 1], [], [], [], [], 10)

        # Test for case where a process did not consume all of the quanta.
        processes = [ProcessControlBlock(0, 0, 4, 0),
                     ProcessControlBlock(1, 3, 5, 0)]
        assert algorithms.round_robin(processes, quanta=5) == ([0, 1], [], [], [], [], 9)

        # Test for case where there are same arrival times for two processes but no running process.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 0, 5, 0)]
        assert algorithms.round_robin(processes, quanta=5) == ([0, 1], [], [], [], [], 10)

        # Test for case where there are two processes that arrived at the same time while another process is running.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 3, 5, 0),
                     ProcessControlBlock(2, 3, 5, 0)]
        assert algorithms.round_robin(processes, quanta=5) == ([0, 1, 2], [], [], [], [], 15)

        # Test for case where there is a gap between process arrivals.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 10, 5, 0)]
        assert algorithms.round_robin(processes, quanta=5) == ([0], [ProcessControlBlock(1, 10, 5, 0)], [], [], [], 5)

        # Test for case where queue is preempted because the time slot was already filled up.
        processes = [ProcessControlBlock(0, 0, 5, 0)]
        resulting_process = ProcessControlBlock(0, 0, 5, 0)
        resulting_process.execute(0, 2)
        assert algorithms.round_robin(processes, quanta=5, time_allotment=2) == ([0], [], [], [],
                                                                                 [resulting_process], 2)

        # Test for case where queue is preempted even though there are still processes arriving.
        processes = [ProcessControlBlock(0, 10, 5, 0)]
        assert algorithms.round_robin(processes, quanta=5, time_allotment=5) == ([], [ProcessControlBlock(0, 10, 5, 0)],
                                                                                 [], [], [], 0)

        # Test for case where queue is preempted even though there are still processes waiting to have a first run.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 1, 5, 0)]
        promoted_process = ProcessControlBlock(0, 0, 5, 0)
        promoted_process.execute(0, 2)
        assert algorithms.round_robin(processes, quanta=5, time_allotment=2) == ([0],
                                                                       [],
                                                                       [ProcessControlBlock(1, 1, 5, 0)],
                                                                       [],
                                                                       [promoted_process],
                                                                       2)

        # Test for case where queue has a time block and a gap between processes.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 10, 5, 0)]
        assert algorithms.round_robin(processes, quanta=5, time_allotment=15) == ([0],
                                                                                  [ProcessControlBlock(1, 10, 5, 0)],
                                                                                  [], [], [], 5)

        # Test for case where another set of processes are added from another queue.
        processes = [ProcessControlBlock(0, 0, 5, 0)]
        additional_processes = [ProcessControlBlock(1, 1, 5, 0)]
        assert algorithms.round_robin(processes, additional_processes, quanta=5) == ([0, 1], [], [], [], [], 10)
