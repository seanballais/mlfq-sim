# -*- coding: utf-8 -*-
import json

from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image, ImageDraw

from mlfq_sim.gui.vendor.QtImageViewer import QtImageViewer

from mlfq_sim.ds.pcb import ProcessControlBlock
from mlfq_sim.scheduler import algorithms
from mlfq_sim.scheduler.mlfq import MLFQ
from mlfq_sim.scheduler.mlfq import MLFQQueue

class Ui_AppWindow(object):
    def setupUi(self, AppWindow):
        AppWindow.setObjectName("AppWindow")
        AppWindow.resize(853, 507)
        self.centralWidget = QtWidgets.QWidget(AppWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.main_separator = QtWidgets.QVBoxLayout()
        self.main_separator.setSpacing(6)
        self.main_separator.setObjectName("main_separator")

        self.gantt_chart = QtImageViewer()
        self.gantt_chart.setAlignment(QtCore.Qt.AlignCenter)
        self.gantt_chart.setObjectName("gantt_chart")
        self.gantt_chart.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.gantt_chart.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.gantt_chart.canZoom = True
        self.gantt_chart.canPan = True

        self.main_separator.addWidget(self.gantt_chart)
        self.gantt_chart_note = QtWidgets.QLabel(self.centralWidget)
        self.gantt_chart_note.setObjectName("gantt_chart_note")
        self.main_separator.addWidget(self.gantt_chart_note)
        self.process_queue_creator = QtWidgets.QHBoxLayout()
        self.process_queue_creator.setSpacing(6)
        self.process_queue_creator.setObjectName("process_queue_creator")
        self.queues_panel = QtWidgets.QVBoxLayout()
        self.queues_panel.setSpacing(6)
        self.queues_panel.setObjectName("queues_panel")
        self.queues_label = QtWidgets.QLabel(self.centralWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.queues_label.setFont(font)
        self.queues_label.setObjectName("queues_label")
        self.queues_panel.addWidget(self.queues_label)

        self.queues_table = QtWidgets.QTableWidget(self.centralWidget)
        self.queues_table.setObjectName("queues_table")
        self.queues_table.setColumnCount(2)
        self.queues_table.setRowCount(0)
        self.queues_table.setHorizontalHeaderLabels('Queue Scheduling Algorithm; Time Allotment'.split(';'))
        self.queues_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        self.queues_panel.addWidget(self.queues_table)
        self.add_queue_layout = QtWidgets.QVBoxLayout()
        self.add_queue_layout.setSpacing(6)
        self.add_queue_layout.setObjectName("add_queue_layout")
        self.add_queue_label = QtWidgets.QLabel(self.centralWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.add_queue_label.setFont(font)
        self.add_queue_label.setObjectName("add_queue_label")
        self.add_queue_layout.addWidget(self.add_queue_label)
        self.add_queue_label_widgets = QtWidgets.QHBoxLayout()
        self.add_queue_label_widgets.setSpacing(6)
        self.add_queue_label_widgets.setObjectName("add_queue_label_widgets")
        self.algorithm_selection_label = QtWidgets.QLabel(self.centralWidget)
        self.algorithm_selection_label.setObjectName("algorithm_selection_label")
        self.add_queue_label_widgets.addWidget(self.algorithm_selection_label)
        
        self.algorithms_selection = QtWidgets.QComboBox(self.centralWidget)
        self.algorithms_selection.setObjectName("algorithms_selection")
        self.algorithms_selection.addItems((
            'First Come, First Serve',
            'Shortest Job First',
            'Shortest Remaining Time First',
            'Non-Preemptive Priority',
            'Preemptive Priority',
            'Round Robin'
        ))

        self.add_queue_label_widgets.addWidget(self.algorithms_selection)
        self.queue_quanta_label = QtWidgets.QLabel(self.centralWidget)
        self.queue_quanta_label.setObjectName("queue_quanta_label")
        self.add_queue_label_widgets.addWidget(self.queue_quanta_label)
        self.queue_quanta = QtWidgets.QSpinBox(self.centralWidget)
        self.queue_quanta.setObjectName("queue_quanta")
        self.add_queue_label_widgets.addWidget(self.queue_quanta)

        self.add_new_queue_button = QtWidgets.QPushButton(self.centralWidget)
        self.add_new_queue_button.setObjectName("add_new_queue_button")
        self.add_new_queue_button.clicked.connect(self.add_new_queue)
        
        self.add_queue_label_widgets.addWidget(self.add_new_queue_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.add_queue_label_widgets.addItem(spacerItem)
        self.add_queue_layout.addLayout(self.add_queue_label_widgets)
        self.add_queue_info = QtWidgets.QLabel(self.centralWidget)
        self.add_queue_info.setObjectName("add_queue_info")
        self.add_queue_layout.addWidget(self.add_queue_info)
        self.queues_panel.addLayout(self.add_queue_layout)
        self.delete_queue_layout = QtWidgets.QVBoxLayout()
        self.delete_queue_layout.setSpacing(6)
        self.delete_queue_layout.setObjectName("delete_queue_layout")
        self.delete_queue_label = QtWidgets.QLabel(self.centralWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.delete_queue_label.setFont(font)
        self.delete_queue_label.setObjectName("delete_queue_label")
        self.delete_queue_layout.addWidget(self.delete_queue_label)
        self.delete_queue_widgets = QtWidgets.QHBoxLayout()
        self.delete_queue_widgets.setSpacing(6)
        self.delete_queue_widgets.setObjectName("delete_queue_widgets")

        self.delete_queue_button = QtWidgets.QPushButton(self.centralWidget)
        self.delete_queue_button.setObjectName("delete_queue_button")
        self.delete_queue_button.clicked.connect(self.delete_selected_queue)
        self.delete_queue_widgets.addWidget(self.delete_queue_button)

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.delete_queue_widgets.addItem(spacerItem1)
        self.delete_queue_layout.addLayout(self.delete_queue_widgets)
        self.queues_panel.addLayout(self.delete_queue_layout)
        self.set_mlfq_config_widgets = QtWidgets.QVBoxLayout()
        self.set_mlfq_config_widgets.setSpacing(6)
        self.set_mlfq_config_widgets.setObjectName("set_mlfq_config_widgets")
        self.mlfq_config_label = QtWidgets.QLabel(self.centralWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.mlfq_config_label.setFont(font)
        self.mlfq_config_label.setObjectName("mlfq_config_label")
        self.set_mlfq_config_widgets.addWidget(self.mlfq_config_label)
        self.mlfq_config_widgets = QtWidgets.QHBoxLayout()
        self.mlfq_config_widgets.setSpacing(6)
        self.mlfq_config_widgets.setObjectName("mlfq_config_widgets")
        self.mlfq_algorith_label = QtWidgets.QLabel(self.centralWidget)
        self.mlfq_algorith_label.setObjectName("mlfq_algorith_label")
        self.mlfq_config_widgets.addWidget(self.mlfq_algorith_label)

        self.mlfq_algorithm_selection = QtWidgets.QComboBox(self.centralWidget)
        self.mlfq_algorithm_selection.setObjectName("mlfq_algorithm_selection")
        self.mlfq_algorithm_selection.addItems((
            'Higher over Lower Priority',
            'Fixed Time Slots'
        ))

        self.mlfq_config_widgets.addWidget(self.mlfq_algorithm_selection)
        self.time_allotment_label = QtWidgets.QLabel(self.centralWidget)
        self.time_allotment_label.setObjectName("time_allotment_label")
        self.mlfq_config_widgets.addWidget(self.time_allotment_label)
        self.mlfq_time_allotment_value = QtWidgets.QSpinBox(self.centralWidget)
        self.mlfq_time_allotment_value.setObjectName("mlfq_time_allotment_value")
        self.mlfq_config_widgets.addWidget(self.mlfq_time_allotment_value)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.mlfq_config_widgets.addItem(spacerItem2)
        self.set_mlfq_config_widgets.addLayout(self.mlfq_config_widgets)
        self.queues_panel.addLayout(self.set_mlfq_config_widgets)
        self.process_queue_creator.addLayout(self.queues_panel)
        self.processes_panel = QtWidgets.QVBoxLayout()
        self.processes_panel.setSpacing(6)
        self.processes_panel.setObjectName("processes_panel")
        self.processes_label = QtWidgets.QLabel(self.centralWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.processes_label.setFont(font)
        self.processes_label.setObjectName("processes_label")
        self.processes_panel.addWidget(self.processes_label)

        self.processes_table = QtWidgets.QTableWidget(self.centralWidget)
        self.processes_table.setObjectName("processes_table")
        self.processes_table.setColumnCount(4)
        self.processes_table.setRowCount(0)
        self.processes_table.setHorizontalHeaderLabels('PID;Arrival Time;Burst Time; Priority'.split(';'))
        self.processes_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.processes_panel.addWidget(self.processes_table)
        self.processes_buttons_layout = QtWidgets.QHBoxLayout()
        self.processes_buttons_layout.setSpacing(6)
        self.processes_buttons_layout.setObjectName("processes_buttons_layout")

        self.add_new_process_button = QtWidgets.QPushButton(self.centralWidget)
        self.add_new_process_button.setObjectName("add_new_process_button")
        self.add_new_process_button.clicked.connect(self.add_new_row_to_process)

        self.processes_buttons_layout.addWidget(self.add_new_process_button)
        self.view_process_execution_details = QtWidgets.QPushButton(self.centralWidget)
        self.view_process_execution_details.setEnabled(False)
        self.view_process_execution_details.setObjectName("view_process_execution_details")
        self.processes_buttons_layout.addWidget(self.view_process_execution_details)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.processes_buttons_layout.addItem(spacerItem5)

        self.delete_selected_process_button = QtWidgets.QPushButton(self.centralWidget)
        self.delete_selected_process_button.setObjectName("delete_selected_process_button")
        self.delete_selected_process_button.clicked.connect(self.delete_selected_process)

        self.processes_buttons_layout.addWidget(self.delete_selected_process_button)
        self.processes_panel.addLayout(self.processes_buttons_layout)
        self.processes_info = QtWidgets.QLabel(self.centralWidget)
        self.processes_info.setObjectName("processes_info")
        self.processes_panel.addWidget(self.processes_info)
        self.process_queue_creator.addLayout(self.processes_panel)
        self.main_separator.addLayout(self.process_queue_creator)
        self.gridLayout.addLayout(self.main_separator, 0, 0, 1, 1)
        self.simulate_mlfq_layout = QtWidgets.QHBoxLayout()
        self.simulate_mlfq_layout.setSpacing(6)
        self.simulate_mlfq_layout.setObjectName("simulate_mlfq_layout")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.simulate_mlfq_layout.addItem(spacerItem7)

        self.simulate_mlfq_button = QtWidgets.QPushButton(self.centralWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.simulate_mlfq_button.setFont(font)
        self.simulate_mlfq_button.setObjectName("simulate_mlfq_button")
        self.simulate_mlfq_button.clicked.connect(self.simulate_mlfq)

        self.simulate_mlfq_layout.addWidget(self.simulate_mlfq_button)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.simulate_mlfq_layout.addItem(spacerItem8)
        self.gridLayout.addLayout(self.simulate_mlfq_layout, 1, 0, 1, 1)
        AppWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(AppWindow)
        QtCore.QMetaObject.connectSlotsByName(AppWindow)


    def retranslateUi(self, AppWindow):
        _translate = QtCore.QCoreApplication.translate
        AppWindow.setWindowTitle(_translate("AppWindow", "Multi-Level Feedback Queue Simulator"))
        self.gantt_chart_note.setText(_translate("AppWindow", "NOTE: Use the left mouse button to pan. Use right button and drag to zoom. Double right click to zoom out to the full image."))
        self.queues_label.setText(_translate("AppWindow", "Queues"))
        self.add_queue_label.setText(_translate("AppWindow", "Add Queue"))
        self.algorithm_selection_label.setText(_translate("AppWindow", "Select algorithm"))
        self.queue_quanta_label.setText(_translate("AppWindow", "Quanta (if applicable)"))
        self.add_new_queue_button.setText(_translate("AppWindow", "Add New Queue"))
        self.add_queue_info.setText(_translate("AppWindow", "NOTE: Topmost queue will be the first queue in the MLFQ."))
        self.delete_queue_label.setText(_translate("AppWindow", "Delete Queue"))
        self.delete_queue_button.setText(_translate("AppWindow", "Delete Selected Queue"))
        self.mlfq_config_label.setText(_translate("AppWindow", "MLFQ Configuration"))
        self.mlfq_algorith_label.setText(_translate("AppWindow", "Select algorithm"))
        self.time_allotment_label.setText(_translate("AppWindow", "Time Allotment"))
        self.processes_label.setText(_translate("AppWindow", "Processes"))
        self.add_new_process_button.setText(_translate("AppWindow", "Add New Process"))
        self.delete_selected_process_button.setText(_translate("AppWindow", "Delete Selected Process"))
        self.view_process_execution_details.setText(_translate("AppWindow", "View Process Execution Details"))
        self.processes_info.setText(_translate("AppWindow", "NOTE: Start modifying a process's data by double clicking on a process's row cell."))
        self.simulate_mlfq_button.setText(_translate("AppWindow", "▷ Simulate MLFQ"))

    def add_new_row_to_process(self):
        num_processes = self.processes_table.rowCount()
        self.processes_table.insertRow(num_processes)

    def delete_selected_process(self):
        if len(self.processes_table.selectedIndexes()) > 0:
            cell = self.processes_table.selectedIndexes()[0]
            self.processes_table.removeRow(cell.row())

    def add_new_queue(self):
        queue_algorithm = self.algorithms_selection.currentText()
        quanta = self.queue_quanta.text()
        if queue_algorithm != 'Round Robin':
            quanta = '0'
        elif queue_algorithm == 'Round Robin' and int(quanta) == 0:
            error_message = QtWidgets.QMessageBox()
            error_message.setIcon(QtWidgets.QMessageBox.Critical)
            error_message.setText('Wrong quanta entered!')
            error_message.setInformativeText('Queue quanta cannot be 0 when using round robin.')
            error_message.setWindowTitle('Multi-Level Feedback Queue Simulator Error')
            error_message.exec()
            return

        num_queues = self.queues_table.rowCount()
        
        self.queues_table.insertRow(num_queues)
        self.queues_table.setItem(num_queues, 0, QtWidgets.QTableWidgetItem(queue_algorithm))
        self.queues_table.setItem(num_queues, 1, QtWidgets.QTableWidgetItem(quanta))

    def delete_selected_queue(self):
        if len(self.queues_table.selectedIndexes()) > 0:
            cell = self.queues_table.selectedIndexes()[0]
            self.queues_table.removeRow(cell.row())
            
    def simulate_mlfq(self):
        # Gather all processes and queues.
        processes = []
        queues = []

        num_processes = self.processes_table.rowCount()
        for row_index in range(num_processes):
            pid = int(self.processes_table.item(row_index, 0).text())
            arrival_time = int(self.processes_table.item(row_index, 1).text())
            burst_time = int(self.processes_table.item(row_index, 2).text())
            priority = int(self.processes_table.item(row_index, 3).text())

            processes.append(ProcessControlBlock(pid, arrival_time, burst_time, priority))

        num_queues = self.queues_table.rowCount()
        for row_index in range(num_queues):
            algorithm = self.queues_table.item(row_index, 0).text()
            if algorithm == 'First Come, First Serve':
                algorithm = 'fcfs'
            elif algorithm == 'Shortest Job First':
                algorithm = 'sjf'
            elif algorithm == 'Shortest Remaining Time First':
                algorithm = 'srtf'
            elif algorithm == 'Non-Preemptive Priority':
                algorithm = 'non_preemptive'
            elif algorithm == 'Preemptive Priority':
                algorithm = 'preemptive'
            elif algorithm == 'Round Robin':
                algorithm = 'round_robin'

            mlfq_algorithm = getattr(algorithms, algorithm)
            quanta = self.queues_table.item(row_index, 1).text()

            queues.append(MLFQQueue(mlfq_algorithm, int(quanta)))

        # Set MLFQ config.
        mlfq_algorithm = self.mlfq_algorithm_selection.currentText()
        time_allotment = int(self.mlfq_time_allotment_value.text())
        if mlfq_algorithm != 'Fixed Time Slots':
            time_allotment = 0
        elif mlfq_algorithm == 'Fixed Time Slots' and time_allotment == 0:
            error_message = QtWidgets.QMessageBox()
            error_message.setIcon(QtWidgets.QMessageBox.Critical)
            error_message.setText('Wrong quanta entered!')
            error_message.setInformativeText('Queue quanta cannot be 0 when using round robin.')
            error_message.setWindowTitle('Multi-Level Feedback Queue Simulator Error')
            error_message.exec()
            return

        mlfq1 = MLFQ(processes, queues, time_allotment)
        schedule, processes, run_time = mlfq1.simulate()

        output = {
            'schedule': schedule,
            'processes': [process.as_dict() for process in processes],
            'run_time': run_time
        }

        self._draw_schedule(output)

        schedule_image = QtGui.QImage('schedule.png')
        self.gantt_chart.setImage(schedule_image)

    def _draw_schedule(self, output):
        image_width = (output['run_time'] * 10) + 100  # 10 px per time unit.
        image_height = 210

        schedule_image = Image.new('RGB', (image_width, image_height), (255, 255, 255))

        draw = ImageDraw.Draw(schedule_image)
        for process in output['processes']:
            for item in process['execution_history']:
                # Draw the timeline.
                x0, y0 = (item['start'] * 10) + 50, 70
                x1, y1 = (item['end'] * 10) + 50, 140
                draw.rectangle((x0, y0, x1, y1), fill=(1, 50, 67))

                # Draw the text.
                draw.text((x0 - 2, y0 + 85), str(item['start']), fill=(108, 122, 137))
                draw.text((x1 - 2, y1 + 15), str(item['end']), fill=(108, 122, 137))

                # Draw the text markers.
                draw.line((x0, y0, x0, y0 + 80), fill=(0, 0, 0))
                draw.line((x1, y0, x1, y1 + 10), fill=(0, 0, 0))

                # Draw process id.
                x_midpoint = x0 + ((x1 - x0) / 2)
                y_midpoint = y0 + ((y1 - y0) / 2)
                draw.text((x_midpoint - 3, y_midpoint - 3), 'P' + str(process['pid']), fill=(255, 255, 255))

        del draw

        schedule_image.save('schedule.png')

