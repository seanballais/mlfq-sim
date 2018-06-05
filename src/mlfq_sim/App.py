#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json

from PyQt5 import QtWidgets

from mlfq_sim.ds.pcb import ProcessControlBlock
from mlfq_sim.scheduler import algorithms
from mlfq_sim.scheduler.mlfq import MLFQ
from mlfq_sim.scheduler.mlfq import MLFQQueue
from mlfq_sim.gui import app_window


__author__ = "Sean Francis N. Ballais, Warren Kenn H. Pulma"
__copyright__ = "Sean Francis N. Ballais, Warren Kenn H. Pulma"
__license__ = "mit"


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = app_window.Ui_AppWindow()
        self.ui.setupUi(self)


def main():
    if len(sys.argv) > 1:
        # Generate processes.
        processes = []
        with open(sys.argv[1]) as processes_data:
            p = json.load(processes_data)
            json_processes = []
            for key in sorted(p.keys()):
                json_processes.append((key, p[key]))

            for _, process in json_processes:
                pid = int(process['pid'])
                arrival_time = int(process['arrival_time'])
                burst_time = int(process['burst_time'])
                priority = int(process['priority'])
                processes.append(ProcessControlBlock(pid, arrival_time, burst_time, priority))

        # Generate queues.
        queues = []
        with open(sys.argv[2]) as queues_data:
            q = json.load(queues_data)
            json_queues = []
            for key in sorted(q.keys()):
                json_queues.append((key, q[key]))

            for _, queue in json_queues:
                algorithm = getattr(algorithms, queue['algorithm'])
                quanta = int(queue['quanta'])
                queues.append(MLFQQueue(algorithm, quanta))

        time_slot = int(sys.argv[3])

        mlfq1 = MLFQ(processes, queues, time_slot)
        schedule, processes, run_time = mlfq1.simulate()

        output = {
            'schedule': schedule,
            'processes': [process.as_dict() for process in processes],
            'run_time': run_time
        }

        print(json.dumps(output))
    else:
        app = QtWidgets.QApplication(sys.argv)
        application = ApplicationWindow()
        application.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
