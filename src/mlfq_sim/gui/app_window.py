# -*- coding: utf-8 -*-
import json
import random

from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image, ImageDraw

from mlfq_sim.gui.vendor.QtImageViewer import QtImageViewer

from mlfq_sim.ds.pcb import ProcessControlBlock
from mlfq_sim.scheduler import algorithms
from mlfq_sim.scheduler.mlfq import MLFQ
from mlfq_sim.scheduler.mlfq import MLFQQueue

class Ui_AppWindow(object):
    def __init__(self):
        self._used_process_colours = set()
        self._used_pids = set()


    def setupUi(self, AppWindow):
        AppWindow.setObjectName("AppWindow")
        AppWindow.resize(878, 507)
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
        self.queues_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        
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
        self.processes_info.setText(_translate(
            "AppWindow",
            "NOTE: Higher priority number has higher priority. To edit a cell's value, just select a cell and type."
        ))
        self.simulate_mlfq_button.setText(_translate("AppWindow", "▷ Simulate MLFQ"))

    def add_new_row_to_process(self):
        num_processes = self.processes_table.rowCount()
        self.processes_table.insertRow(num_processes)
        self.processes_table.setItem(num_processes, 0, QtWidgets.QTableWidgetItem(str(self._get_random_pid())))

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
        self._used_pids.clear()
        self._used_process_colours.clear()  # Clearing ensures that we are able to reuse colours that
                                            # have been previously used. Each simulation run will use a
                                            # different colour for each process. This constant colour
                                            # change on every new run will also allow users to easily
                                            # notice that a new simulation run has occurred.

        # Gather all processes and queues.
        processes = []
        queues = []

        num_processes = self.processes_table.rowCount()
        if num_processes == 0:
            error_message = QtWidgets.QMessageBox()
            error_message.setIcon(QtWidgets.QMessageBox.Critical)
            error_message.setText('No processes entered!')
            error_message.setInformativeText('We cannot simulate CPU scheduling without processes.')
            error_message.setWindowTitle('Multi-Level Feedback Queue Simulator Error')
            error_message.exec()
            return

        used_pids = set()
        for row_index in range(num_processes):
            try:
                if self.processes_table.item(row_index, 0) is None:
                    error_message = QtWidgets.QMessageBox()
                    error_message.setIcon(QtWidgets.QMessageBox.Critical)
                    error_message.setText('Empty PID!')
                    error_message.setInformativeText('One of the processes does not have a PID.')
                    error_message.setWindowTitle('Multi-Level Feedback Queue Simulator Error')
                    error_message.exec()
                    return

                pid = int(self.processes_table.item(row_index, 0).text())
                if pid in used_pids:
                    error_message = QtWidgets.QMessageBox()
                    error_message.setIcon(QtWidgets.QMessageBox.Critical)
                    error_message.setText('PID Already Used!')
                    error_message.setInformativeText('No two processes can have the same PID.')
                    error_message.setWindowTitle('Multi-Level Feedback Queue Simulator Error')
                    error_message.exec()
                    return
                else:
                    used_pids.add(pid)

                if self.processes_table.item(row_index, 1) is None:
                    error_message = QtWidgets.QMessageBox()
                    error_message.setIcon(QtWidgets.QMessageBox.Critical)
                    error_message.setText('Empty Arrival Time!')
                    error_message.setInformativeText('One of the processes does not have an arrival time.')
                    error_message.setWindowTitle('Multi-Level Feedback Queue Simulator Error')
                    error_message.exec()
                    return

                arrival_time = abs(int(self.processes_table.item(row_index, 1).text()))

                if self.processes_table.item(row_index, 2) is None:
                    error_message = QtWidgets.QMessageBox()
                    error_message.setIcon(QtWidgets.QMessageBox.Critical)
                    error_message.setText('Empty Burst Time!')
                    error_message.setInformativeText('One of the processes does not have a burst time.')
                    error_message.setWindowTitle('Multi-Level Feedback Queue Simulator Error')
                    error_message.exec()
                    return

                burst_time = abs(int(self.processes_table.item(row_index, 2).text()))

                if self.processes_table.item(row_index, 3) is None:
                    error_message = QtWidgets.QMessageBox()
                    error_message.setIcon(QtWidgets.QMessageBox.Critical)
                    error_message.setText('Empty Priority Number!')
                    error_message.setInformativeText('One of the processes does not have a priority number.')
                    error_message.setWindowTitle('Multi-Level Feedback Queue Simulator Error')
                    error_message.exec()
                    return
                priority = abs(int(self.processes_table.item(row_index, 3).text()))

                processes.append(ProcessControlBlock(pid, arrival_time, burst_time, priority))
            except ValueError:
                error_message = QtWidgets.QMessageBox()
                error_message.setIcon(QtWidgets.QMessageBox.Critical)
                error_message.setText('Only use numbers!')
                error_message.setInformativeText('PIDs, Arrival and Burst Times, and Priority Numbers must be numbers.')
                error_message.setWindowTitle('Multi-Level Feedback Queue Simulator Error')
                error_message.exec()
                return

        num_queues = self.queues_table.rowCount()
        if num_queues == 0:
            error_message = QtWidgets.QMessageBox()
            error_message.setIcon(QtWidgets.QMessageBox.Critical)
            error_message.setText('No processes entered!')
            error_message.setInformativeText('We cannot simulate CPU scheduling without processes.')
            error_message.setWindowTitle('Multi-Level Feedback Queue Simulator Error')
            error_message.exec()
            return

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
        time_unit_size = 50 # This is in pixels.
        timeline_width = output['run_time'] * time_unit_size
        image_width = timeline_width + 100
        image_height = 210

        schedule_image = Image.new('RGB', (image_width, image_height), (255, 255, 255))

        draw = ImageDraw.Draw(schedule_image)

        for process in output['processes']:
            fill_colour = self._get_random_colour()

            for item in process['execution_history']:
                # Draw a timeline unit for the process.
                x0, y0 = (item['start'] * time_unit_size) + 50, 70
                x1, y1 = (item['end'] * time_unit_size) + 50, 140
                draw.rectangle((x0, y0, x1, y1), fill=fill_colour)

                # Draw the text.
                draw.text((x0 - 2, y1 + 15), str(item['start']), fill=(108, 122, 137))
                draw.text((x1 - 2, y1 + 15), str(item['end']), fill=(108, 122, 137))

                # Draw the text markers.
                draw.line((x0, y0, x0, y1 + 10), fill=(0, 0, 0))
                draw.line((x1, y0, x1, y1 + 10), fill=(0, 0, 0))

                # Draw process id.
                x_midpoint = x0 + ((x1 - x0) / 2)
                y_midpoint = y0 + ((y1 - y0) / 2)
                draw.text((x_midpoint - 3, y_midpoint - 3), 'P' + str(process['pid']), fill=(255, 255, 255))

        # Draw the timeline box and the zero time marker.
        box_x0 = (image_width / 2) - (timeline_width / 2)
        box_x1 = (image_width / 2) + (timeline_width / 2)

        # Draw the top line of the box.        
        draw.line((box_x0, 70, box_x1, 70), fill=(0, 0, 0))

        # Draw the bottom line of the box.
        draw.line((box_x0, 140, box_x1, 140), fill=(0, 0, 0))

        # Draw the left line of the box.
        draw.line((box_x0, 70, box_x0, 140), fill=(0, 0, 0))

        # No need to draw the right line of the box since we can be sure that
        # it has been rendered already when the process timeline units were
        # being rendered. The same reason goes for skipping rendering the
        # last time marker text.

        # Draw the zero time marker.
        draw.line((box_x0, 70, box_x0, 150), fill=(0, 0, 0))

        # Draw the zero time marker text.
        draw.text((box_x0 - 2, 155), '0', fill=(108, 122, 137))

        del draw

        schedule_image.save('schedule.png')


    def _get_random_colour(self):
        # Get a random flat colour that has not been used already by a
        # process in the current simulation run.
        gotUnusedColour = False
        colour = None
        while not gotUnusedColour:
            colour = (self._get_random_colour_component_value(),
                      self._get_random_colour_component_value(),
                      self._get_random_colour_component_value())
            if colour not in self._used_process_colours:
                gotUnusedColour = True
                self._used_process_colours.add(colour)

        return colour


    def _get_random_colour_component_value(self):
        # Colours based on the colour wheel from
        # http://paletton.com/#uid=1300u0kllllaFw0g0qFqFg0w0aF.
        # Value of the first hex column can range from 0x2 to 0xA.
        # The value of the second hex column can be any of the following:
        #    0, 1, 3, 4, 6, 7, 9, A, C, E, F
        first_hex_column_values = [str(i + 2) for i in list(range(8))] + ['A']
        first_hex_column_value = random.choice(first_hex_column_values)
        second_hex_column_value = random.choice(['0', '1', '3',
                                                 '4', '6', '7',
                                                 '9', 'A', 'C',
                                                 'E', 'F'])
        hex_value = '0x{}{}'.format(first_hex_column_value,
                                    second_hex_column_value)

        return int(hex_value, 0)


    def _get_random_pid(self):
        # Get a random PID that has not been used already by a
        # process in the current simulation run.
        gotUnusedPid = False
        pid = None
        num_processes = self.processes_table.rowCount()
        while not gotUnusedPid:
            pid = random.choice(range(num_processes + 100))
            if pid not in self._used_pids:
                gotUnusedPid = True
                self._used_pids.add(pid)

        return pid
