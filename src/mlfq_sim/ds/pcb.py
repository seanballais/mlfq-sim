#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class ProcessControlBlock:
    class ExecutionHistoryItem:
        def __init__(self, start_time, length):
            self.start_time = start_time
            self.length = length

        def __repr__(self):
            return 'Execution History Item ' \
                   '(executed starting at {0} for {1} units)'.format(self.start_time,
                                                                     self.length)

        def get_start(self):
            return self.start_time

        def get_length(self):
            return self.length

        def get_end(self):
            return self.start_time + self.length


    class ExecutionRecordingException(Exception):
        def __init__(self, *args, **kwargs):
           Exception.__init__(self, *args, **kwargs)


    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority
        self.execution_history = []

    def __repr__(self):
        return 'A Generic Process (pid {0})\n' \
               'Arrival: {1}\tBurst: {2}\tPriority: {3}'.format(self.pid,
                                                                self.arrival_time,
                                                                self.burst_time,
                                                                self.priority)

    def get_pid(self):
        return self.pid

    def get_arrival_time(self):
        return self.arrival_time

    def get_burst_time(self):
        return self.burst_time

    def get_remaining_time(self):
        return self.remaining_time

    def get_priority(self):
        return self.priority

    def get_execution_history(self):
        return self.execution_history

    def execute(self, start_time, length):
        if self.remaining_time == 0:
            raise self.ExecutionRecordingException('Cannot record execution period ' \
                                                   'because the process has already' \
                                                   ' completed execution.')

        if len(self.execution_history) > 0:
            max_item_index = max(len(self.execution_history) - 1, 0)
            recent_execution_item = self.execution_history[max_item_index]
            recent_item_start = recent_execution_item.get_start()
            recent_item_length = recent_execution_item.get_length()

            if (start_time <= recent_item_start  # Remember that we cannot run a process
                                                 # in the past, only in the present.
                or start_time < recent_item_start + recent_item_length  # We can start the process
                                                                        # exactly right where we
                                                                        # ended the process
                                                                        # execution temporarily.
                                                                        # Thus, we are allowing
                                                                        # `start_time`` to be equal
                                                                        # to `recent_item_start +
                                                                        # recent_item_length`. That
                                                                        # we are only using `<`
                                                                        # instead of `<=`.
                ):
                raise self.ExecutionRecordingException('Cannot record an execution period that has' \
                                                       ' occurred in the past, or in between ' \
                                                       'a certain previous execution period of ' \
                                                       'the process.')

        self.remaining_time = max(self.remaining_time - length, 0)
        self.execution_history.append(self.ExecutionHistoryItem(start_time, length))
