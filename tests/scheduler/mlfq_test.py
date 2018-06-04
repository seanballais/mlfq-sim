#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from mlfq_sim.ds import ProcessControlBlock
from mlfq_sim.scheduler import algorithms
from mlfq_sim.scheduler import mlfq


class TestMLFQ:
    def test_setup(self):
        with pytest.raises(ValueError) as ve:
            mlfq.MLFQ([], [], time_slot=-1)

    def test_one_queue(self):
        # SCENARIO: Testing higher over lower priority MLFQ scheduling.
        # Test with one process only.
        processes = [ProcessControlBlock(0, 0, 5, 1)]
        queues = [mlfq.MLFQQueue(algorithms.fcfs)]

        mlfq1 = mlfq.MLFQ(processes, queues)
        schedule, process, run_time = mlfq1.simulate()

        assert schedule == [0]
        assert process[0].get_pid() == 0
        assert run_time == 5

        # Test with three processes.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 3, 5, 0),
                     ProcessControlBlock(2, 3, 5, 0)]
        queues = [mlfq.MLFQQueue(algorithms.fcfs)]

        mlfq1 = mlfq.MLFQ(processes, queues)
        schedule, process, run_time = mlfq1.simulate()

        assert schedule == [0, 1, 2]
        assert process[0].get_pid() == 0
        assert process[1].get_pid() == 1
        assert process[2].get_pid() == 2
        assert run_time == 15

        # SCENARIO: Testing fixed time slot MLFQ scheduling.
        # Test with one process only.
        processes = [ProcessControlBlock(0, 0, 5, 1)]
        queues = [mlfq.MLFQQueue(algorithms.fcfs)]

        mlfq1 = mlfq.MLFQ(processes, queues, time_slot=5)
        schedule, process, run_time = mlfq1.simulate()

        assert schedule == [0]
        assert process[0].get_pid() == 0
        assert run_time == 5

        # Test with three processes.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 3, 5, 0),
                     ProcessControlBlock(2, 3, 5, 0)]
        queues = [mlfq.MLFQQueue(algorithms.fcfs)]

        mlfq1 = mlfq.MLFQ(processes, queues, time_slot=5)
        schedule, process, run_time = mlfq1.simulate()

        assert schedule == [0, 1, 2]
        assert process[0].get_pid() == 0
        assert process[1].get_pid() == 1
        assert process[2].get_pid() == 2
        assert run_time == 15

    def test_two_queues(self):
        # SCENARIO: Testing higher over lower priority MLFQ scheduling.
        # Test with one process only.
        processes = [ProcessControlBlock(0, 0, 10, 1)]
        queues = [mlfq.MLFQQueue(algorithms.round_robin, quanta=5),
                  mlfq.MLFQQueue(algorithms.fcfs)]

        mlfq1 = mlfq.MLFQ(processes, queues)
        schedule, process, run_time = mlfq1.simulate()

        assert schedule == [0]
        assert process[0].get_pid() == 0
        assert run_time == 10

        # Test with three processes.
        processes = [ProcessControlBlock(0, 0, 20, 0),
                     ProcessControlBlock(1, 15, 5, 0),
                     ProcessControlBlock(2, 20, 5, 0)]
        queues = [mlfq.MLFQQueue(algorithms.round_robin, quanta=5),
                  mlfq.MLFQQueue(algorithms.fcfs)]

        mlfq1 = mlfq.MLFQ(processes, queues)
        schedule, process, run_time = mlfq1.simulate()

        assert schedule == [0, 1, 2, 0]
        assert process[0].get_pid() == 0
        assert process[1].get_pid() == 1
        assert process[2].get_pid() == 2
        assert run_time == 30

        # Test with gaps in between processes.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 10, 5, 0)]
        queues = [mlfq.MLFQQueue(algorithms.round_robin, quanta=5),
                  mlfq.MLFQQueue(algorithms.fcfs)]

        mlfq1 = mlfq.MLFQ(processes, queues)
        schedule, process, run_time = mlfq1.simulate()
        assert schedule == [0, 1]
        assert process[0].get_pid() == 0
        assert process[1].get_pid() == 1
        assert run_time == 15

        # SCENARIO: Testing fixed time slot MLFQ scheduling.
        # Test with one process only.
        processes = [ProcessControlBlock(0, 0, 10, 1)]
        queues = [mlfq.MLFQQueue(algorithms.round_robin, quanta=5),
                  mlfq.MLFQQueue(algorithms.fcfs)]

        mlfq1 = mlfq.MLFQ(processes, queues, time_slot=5)
        schedule, process, run_time = mlfq1.simulate()

        assert schedule == [0]
        assert process[0].get_pid() == 0
        assert run_time == 10

        # Test with three processes.
        processes = [ProcessControlBlock(0, 0, 20, 0),
                     ProcessControlBlock(1, 15, 5, 0),
                     ProcessControlBlock(2, 20, 5, 0)]
        queues = [mlfq.MLFQQueue(algorithms.round_robin, quanta=5),
                  mlfq.MLFQQueue(algorithms.fcfs)]

        mlfq1 = mlfq.MLFQ(processes, queues, time_slot=5)
        schedule, process, run_time = mlfq1.simulate()

        assert schedule == [0, 1, 2]
        assert process[0].get_pid() == 0
        assert process[1].get_pid() == 1
        assert process[2].get_pid() == 2
        assert run_time == 30

        # Test with gaps in between processes.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 10, 5, 0)]
        queues = [mlfq.MLFQQueue(algorithms.round_robin, quanta=5),
                  mlfq.MLFQQueue(algorithms.fcfs)]

        mlfq1 = mlfq.MLFQ(processes, queues, time_slot=5)
        schedule, process, run_time = mlfq1.simulate()
        assert schedule == [0, 1]
        assert process[0].get_pid() == 0
        assert process[1].get_pid() == 1
        assert run_time == 15

        # Invoke processes to remain in the same queue.
        processes = [ProcessControlBlock(0, 0, 10, 0),
                     ProcessControlBlock(1, 0, 10, 0),
                     ProcessControlBlock(2, 10, 10, 0)]
        queues = [mlfq.MLFQQueue(algorithms.round_robin, quanta=5),
                  mlfq.MLFQQueue(algorithms.round_robin, quanta=5)]

        mlfq1 = mlfq.MLFQ(processes, queues)
        schedule, process, run_time = mlfq1.simulate()
        assert schedule == [0, 1, 2, 0, 1, 2]
        assert process[0].get_pid() == 0
        assert process[1].get_pid() == 1
        assert process[2].get_pid() == 2
        assert run_time == 30

    def test_three_queues(self):
        # SCENARIO: Testing higher over lower priority MLFQ scheduling.
        # Test with one process only.
        processes = [ProcessControlBlock(0, 0, 15, 1)]
        queues = [mlfq.MLFQQueue(algorithms.round_robin, quanta=5),
                  mlfq.MLFQQueue(algorithms.round_robin, quanta=5),
                  mlfq.MLFQQueue(algorithms.fcfs)]

        mlfq1 = mlfq.MLFQ(processes, queues)
        schedule, process, run_time = mlfq1.simulate()

        assert schedule == [0]
        assert process[0].get_pid() == 0
        assert run_time == 15

        # Test with three processes.
        processes = [ProcessControlBlock(0, 0, 20, 0),
                     ProcessControlBlock(1, 15, 5, 0),
                     ProcessControlBlock(2, 20, 5, 0)]
        queues = [mlfq.MLFQQueue(algorithms.round_robin, quanta=5),
                  mlfq.MLFQQueue(algorithms.round_robin, quanta=5),
                  mlfq.MLFQQueue(algorithms.fcfs)]

        mlfq1 = mlfq.MLFQ(processes, queues)
        schedule, process, run_time = mlfq1.simulate()

        assert schedule == [0, 1, 2, 0]
        assert process[0].get_pid() == 0
        assert process[1].get_pid() == 1
        assert process[2].get_pid() == 2
        assert run_time == 30

        # Test with gaps in between processes.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 10, 5, 0)]
        queues = [mlfq.MLFQQueue(algorithms.round_robin, quanta=5),
                  mlfq.MLFQQueue(algorithms.round_robin, quanta=5),
                  mlfq.MLFQQueue(algorithms.fcfs)]

        mlfq1 = mlfq.MLFQ(processes, queues)
        schedule, process, run_time = mlfq1.simulate()
        assert schedule == [0, 1]
        assert process[0].get_pid() == 0
        assert process[1].get_pid() == 1
        assert run_time == 15

        # SCENARIO: Testing fixed time slot MLFQ scheduling.
        # Test with one process only.
        processes = [ProcessControlBlock(0, 0, 15, 1)]
        queues = [mlfq.MLFQQueue(algorithms.round_robin, quanta=5),
                  mlfq.MLFQQueue(algorithms.round_robin, quanta=5),
                  mlfq.MLFQQueue(algorithms.fcfs)]

        mlfq1 = mlfq.MLFQ(processes, queues, time_slot=5)
        schedule, process, run_time = mlfq1.simulate()

        assert schedule == [0]
        assert process[0].get_pid() == 0
        assert run_time == 15

        # Test with three processes.
        processes = [ProcessControlBlock(0, 0, 20, 0),
                     ProcessControlBlock(1, 15, 5, 0),
                     ProcessControlBlock(2, 20, 5, 0)]
        queues = [mlfq.MLFQQueue(algorithms.round_robin, quanta=5),
                  mlfq.MLFQQueue(algorithms.round_robin, quanta=5),
                  mlfq.MLFQQueue(algorithms.fcfs)]

        mlfq1 = mlfq.MLFQ(processes, queues, time_slot=5)
        schedule, process, run_time = mlfq1.simulate()

        assert schedule == [0, 1, 2]
        assert process[0].get_pid() == 0
        assert process[1].get_pid() == 1
        assert process[2].get_pid() == 2
        assert run_time == 30

        # Test with gaps in between processes.
        processes = [ProcessControlBlock(0, 0, 5, 0),
                     ProcessControlBlock(1, 10, 5, 0)]
        queues = [mlfq.MLFQQueue(algorithms.round_robin, quanta=5),
                  mlfq.MLFQQueue(algorithms.round_robin, quanta=5),
                  mlfq.MLFQQueue(algorithms.fcfs)]

        mlfq1 = mlfq.MLFQ(processes, queues, time_slot=5)
        schedule, process, run_time = mlfq1.simulate()
        assert schedule == [0, 1]
        assert process[0].get_pid() == 0
        assert process[1].get_pid() == 1
        assert run_time == 15

    def test_nearest_preemption_time(self):
        mlfq1 = mlfq.MLFQ([], [])
        assert mlfq1._nearest_preemption_time(1) is None

        mlfq1 = mlfq.MLFQ([ProcessControlBlock(0, 0, 1, 0),
                           ProcessControlBlock(1, 5, 3, 0)], [])
        assert mlfq1._nearest_preemption_time(1) == 5
