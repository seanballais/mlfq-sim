# -*- coding: utf-8 -*-

import json

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from mlfq_sim.ds import ProcessControlBlock
from mlfq_sim.ds.scheduling import MLFQQueue
from mlfq_sim.scheduler import algorithms
from mlfq_sim.gui.vendor import gantt

class Ui_AppWindow(object):
    def __init__(self):
        self.processes = {}
        self.mlfq_queue = MLFQQueue()

    def setupUi(self, AppWindow):
        AppWindow.setObjectName("AppWindow")
        AppWindow.resize(800, 600)
        AppWindow.setMinimumSize(QtCore.QSize(800, 600))
        AppWindow.setMaximumSize(QtCore.QSize(800, 600))
        self.centralWidget = QtWidgets.QWidget(AppWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 261, 601))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.processLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.processLayout.setContentsMargins(11, 11, 11, 11)
        self.processLayout.setSpacing(6)
        self.processLayout.setObjectName("processLayout")
        self.processSettingsLayout = QtWidgets.QVBoxLayout()
        self.processSettingsLayout.setContentsMargins(11, 11, 11, 11)
        self.processSettingsLayout.setSpacing(6)
        self.processSettingsLayout.setObjectName("processSettingsLayout")
        self.scheduleProcessesLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.scheduleProcessesLabel.setFont(font)
        self.scheduleProcessesLabel.setObjectName("scheduleProcessesLabel")
        self.processSettingsLayout.addWidget(self.scheduleProcessesLabel)
        self.schedulingAlgorithmSelection = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.schedulingAlgorithmSelection.setObjectName("schedulingAlgorithmSelection")
        self.schedulingAlgorithmSelection.addItems((
            'First Come, First Serve',
            'Shortest Job First',
            'Shortest Remaining Time First',
            'Non-Preemptive Priority',
            'Preemptive Priority',
            'Round Robin'
        ))
        self.processSettingsLayout.addWidget(self.schedulingAlgorithmSelection)
        self.quantaLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.quantaLabel.setObjectName("quantaLabel")
        self.processSettingsLayout.addWidget(self.quantaLabel)
        self.quantaTimeTextbox = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.quantaTimeTextbox.setObjectName("quantaTimeTextbox")
        self.processSettingsLayout.addWidget(self.quantaTimeTextbox)
        self.scheduleButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.scheduleButton.setObjectName("scheduleButton")
        self.scheduleButton.clicked.connect(self.scheduleProcesses)
        self.processSettingsLayout.addWidget(self.scheduleButton)
        self.additionTitle = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.additionTitle.setFont(font)
        self.additionTitle.setObjectName("additionTitle")
        self.processSettingsLayout.addWidget(self.additionTitle)
        self.processIDLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.processIDLabel.setObjectName("processIDLabel")
        self.processSettingsLayout.addWidget(self.processIDLabel)
        self.processIDTextbox = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.processIDTextbox.setObjectName("processIDTextbox")
        self.processSettingsLayout.addWidget(self.processIDTextbox)
        self.arrivalTimeLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.arrivalTimeLabel.setObjectName("arrivalTimeLabel")
        self.processSettingsLayout.addWidget(self.arrivalTimeLabel)
        self.arrivalTimeTextbox = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.arrivalTimeTextbox.setObjectName("arrivalTimeTextbox")
        self.processSettingsLayout.addWidget(self.arrivalTimeTextbox)
        self.burstTimeLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.burstTimeLabel.setObjectName("burstTimeLabel")
        self.processSettingsLayout.addWidget(self.burstTimeLabel)
        self.burstTimeTextbox = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.burstTimeTextbox.setObjectName("burstTimeTextbox")
        self.processSettingsLayout.addWidget(self.burstTimeTextbox)
        self.priorityLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.priorityLabel.setObjectName("priorityLabel")
        self.processSettingsLayout.addWidget(self.priorityLabel)
        self.priorityTextbox = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.priorityTextbox.setObjectName("priorityTextbox")
        self.processSettingsLayout.addWidget(self.priorityTextbox)
        self.addNewProcessButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.addNewProcessButton.setObjectName("addNewProcessButton")
        self.addNewProcessButton.clicked.connect(self.addProcessToList)
        self.processSettingsLayout.addWidget(self.addNewProcessButton)
        self.deleteProcessLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.deleteProcessLabel.setFont(font)
        self.deleteProcessLabel.setObjectName("deleteProcessLabel")
        self.processSettingsLayout.addWidget(self.deleteProcessLabel)
        self.deleteProcessIDLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.deleteProcessIDLabel.setObjectName("deleteProcessIDLabel")
        self.processSettingsLayout.addWidget(self.deleteProcessIDLabel)
        self.deletePIDTextbox = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.deletePIDTextbox.setObjectName("deletePIDTextbox")
        self.processSettingsLayout.addWidget(self.deletePIDTextbox)
        self.deleteProcessButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.deleteProcessButton.setObjectName("deleteProcessButton")
        self.deleteProcessButton.clicked.connect(self.deleteProcess)
        self.processSettingsLayout.addWidget(self.deleteProcessButton)
        self.processLayout.addLayout(self.processSettingsLayout)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(259, 0, 541, 411))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.chartLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.chartLayout.setContentsMargins(11, 11, 11, 11)
        self.chartLayout.setSpacing(6)
        self.chartLayout.setObjectName("chartLayout")
        self.chartScrollArea = QtWidgets.QScrollArea(self.horizontalLayoutWidget)
        self.chartScrollArea.setWidgetResizable(True)
        self.chartScrollArea.setObjectName("chartScrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 537, 407))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.chartHolder = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.chartHolder.setGeometry(QtCore.QRect(2, 5, 501, 391))
        self.chartHolder.setAlignment(QtCore.Qt.AlignCenter)
        self.chartHolder.setObjectName("chartHolder")
        self.chartHolder.setScaledContents(True)
        self.chartScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.chartLayout.addWidget(self.chartScrollArea)
        self.layoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.layoutWidget.setGeometry(QtCore.QRect(260, 410, 541, 191))
        self.layoutWidget.setObjectName("layoutWidget")
        self.processTableLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.processTableLayout.setContentsMargins(11, 11, 11, 11)
        self.processTableLayout.setSpacing(6)
        self.processTableLayout.setObjectName("processTableLayout")
        self.processTableLabel = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.processTableLabel.setFont(font)
        self.processTableLabel.setObjectName("processTableLabel")
        self.processTableLayout.addWidget(self.processTableLabel)
        self.processTable = QtWidgets.QTableWidget(self.layoutWidget)
        self.processTable.setObjectName("processTable")
        self.processTable.setColumnCount(4)
        self.processTable.setRowCount(0)
        self.processTable.setHorizontalHeaderLabels('Process;Arrival Time;Burst Time;Priority'.split(';'))
        self.processTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.processTableLayout.addWidget(self.processTable)
        AppWindow.setCentralWidget(self.centralWidget)

        self.errorMessageBox = QtWidgets.QMessageBox()
        self.errorMessageBox.setWindowTitle(
            'Multi-Level Feedback Queue Simulator - Error')
        self.errorMessageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.errorMessageBox.setIcon(QtWidgets.QMessageBox.Critical)

        self.retranslateUi(AppWindow)
        QtCore.QMetaObject.connectSlotsByName(AppWindow)

    def retranslateUi(self, AppWindow):
        _translate = QtCore.QCoreApplication.translate
        AppWindow.setWindowTitle(_translate("AppWindow", "Multi-Level Feedback Queue Simulator"))
        self.scheduleProcessesLabel.setText(_translate("AppWindow", "Schedule Processes"))
        self.quantaLabel.setText(_translate("AppWindow", "Quanta (default: 5)"))
        self.scheduleButton.setText(_translate("AppWindow", "Schedule Processes"))
        self.additionTitle.setText(_translate("AppWindow", "Add A New Process"))
        self.processIDLabel.setText(_translate("AppWindow", "Process ID"))
        self.arrivalTimeLabel.setText(_translate("AppWindow", "Arrival Time"))
        self.burstTimeLabel.setText(_translate("AppWindow", "Burst Time"))
        self.priorityLabel.setText(_translate("AppWindow", "Priority"))
        self.addNewProcessButton.setText(_translate("AppWindow", "Add process"))
        self.deleteProcessLabel.setText(_translate("AppWindow", "Delete A Process"))
        self.deleteProcessIDLabel.setText(_translate("AppWindow", "Process ID"))
        self.deleteProcessButton.setText(_translate("AppWindow", "Delete process"))
        self.chartHolder.setText(_translate("AppWindow", "The schedule of your processes will appear here."))
        self.processTableLabel.setText(_translate("AppWindow", "Processes"))

    def addProcessToList(self):
        pid = self.processIDTextbox.text()
        arrival_time = self.arrivalTimeTextbox.text()
        burst_time = self.burstTimeTextbox.text()
        priority = self.priorityTextbox.text()

        # Input validation.
        if pid == '':
            self.errorMessageBox.setText('Cannot add process. Process ID field is empty')
            self.errorMessageBox.show()
            self.processIDTextbox.setFocus()
            return
        elif int(pid) in self.processes:
            self.errorMessageBox.setText('Cannot add process. Another process already uses ID {0}'.format(pid))
            self.errorMessageBox.show()
            self.processIDTextbox.setFocus()
            return
        elif int(pid) < 0:
            self.errorMessageBox.setText('Cannot add process. Process ID cannot be less than 0.')
            self.errorMessageBox.show()
            self.processIDTextbox.setFocus()
            return

        if arrival_time == '':
            self.errorMessageBox.setText('Cannot add process. Arrival Time field is empty')
            self.errorMessageBox.show()
            self.arrivalTimeTextbox.setFocus()
            return
        elif int(arrival_time) < 0:
            self.errorMessageBox.setText('Cannot add process. Arrival time cannot be less than 0.')
            self.errorMessageBox.show()
            self.arrivalTimeTextbox.setFocus()
            return

        if burst_time == '':
            self.errorMessageBox.setText('Cannot add process. Burst Time field is empty')
            self.errorMessageBox.show()
            self.burstTimeTextbox.setFocus()
            return
        elif int(burst_time) < 0:
            self.errorMessageBox.setText('Cannot add process. Burst Time cannot be less than 0.')
            self.errorMessageBox.show()
            self.burstTimeTextbox.setFocus()
            return

        if priority == '':
            self.errorMessageBox.setText('Priority field is empty')
            self.errorMessageBox.show()
            self.priorityTextbox.setFocus()
            return

        num_rows = self.processTable.rowCount()
        self.processes[int(pid)] = num_rows
        self.mlfq_queue.add_process(ProcessControlBlock(int(pid),
                                                        int(arrival_time),
                                                        int(burst_time),
                                                        int(priority)))
        self.processTable.insertRow(num_rows)
        self.processTable.setItem(
            num_rows,
            0,
            QtWidgets.QTableWidgetItem(pid)
        )
        self.processTable.setItem(
            num_rows,
            1,
            QtWidgets.QTableWidgetItem(arrival_time)
        )
        self.processTable.setItem(
            num_rows,
            2,
            QtWidgets.QTableWidgetItem(burst_time)
        )
        self.processTable.setItem(
            num_rows,
            3,
            QtWidgets.QTableWidgetItem(priority)
        )

        self.processIDTextbox.setFocus()

    def deleteProcess(self):
        pid = self.deletePIDTextbox.text()

        if pid == '':
            self.errorMessageBox.setText('Unable to perform deletion. No process ID specified.'.format(pid))
            self.errorMessageBox.show()
            self.deletePIDTextbox.setFocus()
            return
        elif int(pid) < 0:
            self.errorMessageBox.setText('Unable to perform deletion. Negatives IDs are not allowed.'.format(pid))
            self.errorMessageBox.show()
            self.deletePIDTextbox.setFocus()
            return
        elif int(pid) not in self.processes:
            self.errorMessageBox.setText('Process with the ID {0} does not exist.'.format(pid))
            self.errorMessageBox.show()
            self.deletePIDTextbox.setFocus()
            return

        self.mlfq_queue.remove_process(int(pid))
        self.processTable.removeRow(self.processes[int(pid)])
        del self.processes[int(pid)]
        self.deletePIDTextbox.setFocus()

    def scheduleProcesses(self):
        if self.mlfq_queue.empty():
            self.errorMessageBox.setText('There is nothing to schedule.')
            self.errorMessageBox.show()
            return

        algorithm_text = self.schedulingAlgorithmSelection.currentText()
        quanta = 0
        if algorithm_text == 'First Come, First Serve':
            self.mlfq_queue.set_scheduling_algorithm(algorithms.fcfs)
        elif algorithm_text == 'Shortest Job First':
            self.mlfq_queue.set_scheduling_algorithm(algorithms.sjf)
        elif algorithm_text == 'Shortest Remaining Time First':
            self.mlfq_queue.set_scheduling_algorithm(algorithms.srtf)
        elif algorithm_text == 'Non-Preemptive Priority':
            self.mlfq_queue.set_scheduling_algorithm(algorithms.non_preemptive)
        elif algorithm_text == 'Preemptive Priority':
            self.mlfq_queue.set_scheduling_algorithm(algorithms.preemptive)
        elif algorithm_text == 'Round Robin':
            self.mlfq_queue.set_scheduling_algorithm(algorithms.round_robin)
            quanta = self.quantaTimeTextbox.text() or 5
            quanta = int(quanta)

        # Schedule time
        if quanta > 0:
            self.mlfq_queue.schedule_processes(quanta)
        else:
            self.mlfq_queue.schedule_processes()

        schedule = self.mlfq_queue.get_schedule()

        # Prepare the Gantt Chart!
        chart_data = {}
        chart_data['packages'] = []
        chart_data['title'] = '{0} Process Scheduling'.format(algorithm_text)
        chart_data['xlabel'] = 'Time (units)'

        last_process = None
        ctr = 0
        while not schedule.empty():
            process_schedule = schedule.get()
            last_process = process_schedule
            chart_data['packages'].append(
                {
                    'label': "Process {0} ({1})".format(process_schedule.get_pid(),
                                                     ctr),
                    'start': process_schedule.get_start_time(),
                    'end': process_schedule.get_end()
                }
            )

            ctr += 1

        chart_data['xticks'] = list(range(last_process.get_end() + 1))

        # Write the schedule JSON file.
        with open('schedule.json', 'w+') as schedule_file:
            json.dump(chart_data, schedule_file)

        self.chartHolder.setText('Loading schedule...')

        g = gantt.Gantt('schedule.json')
        g.render()
        g.save('schedule.png')

        label_pixmap = QtGui.QPixmap('schedule.png')
        self.chartHolder.setPixmap(label_pixmap)

