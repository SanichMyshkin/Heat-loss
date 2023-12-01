from PyQt6.QtWidgets import QDoubleSpinBox, QComboBox, QTableWidgetItem, QMessageBox
from PyQt6 import QtCore


class CalculateTable():
    MAX_RANGE = 10000.0

    def __init__(self):
        self.list_rooms = []

    def GetRooms(self):
        self.Get_and_update_rooms()
        self.CalculateComboBox()

    def AddCalculateRow(self):
        self.CalculateTableWidget.insertRow(self.CalculateTableWidget.rowCount())  # noqa E501
        self.CalculateCountSpinBox()
        self.CalculateComboBox()
        self.CalculateWallComboBox()
        self.MakeCalculateCellReadOnly()

    def RemoveCalculateRow(self):
        self.CalculateTableWidget.removeRow(self.CalculateTableWidget.rowCount() - 1)  # noqa E501

    def CalculateCountSpinBox(self):
        column_number = [5, 6]
        current_row = self.CalculateTableWidget.rowCount() - 1
        for number in column_number:
            coeff_thermal_conductivity = QDoubleSpinBox()  # noqa F405
            coeff_thermal_conductivity.setMaximum(self.MAX_RANGE)
            self.CalculateTableWidget.setCellWidget(current_row, number, coeff_thermal_conductivity)  # noqa E501

    def CalculateComboBox(self):
        column_number = [0, 1]
        # row = self.WallsTableWidget.rowCount() - 1
        for row in range(self.CalculateTableWidget.rowCount()):
            for number in column_number:
                combo_box = QComboBox()
                combo_box.addItems(self.parse_rooms(self.list_rooms))
                self.CalculateTableWidget.setCellWidget(row, number, combo_box)

    def CalculateWallComboBox(self):
        for row in range(self.CalculateTableWidget.rowCount()):
            combo_box = QComboBox()
            combo_box.addItems(['Тут будет ипморт стен'])
            self.CalculateTableWidget.setCellWidget(row, 4, combo_box)

    def MakeCalculateCellReadOnly(self):
        column_number = [2, 3, 7, 8, 9]
        flags = QtCore.Qt.ItemFlag.ItemIsEnabled
        for row in range(self.CalculateTableWidget.rowCount()):
            for col in column_number:
                item = self.CalculateTableWidget.item(row, col)
                if item is None:
                    item = QTableWidgetItem()
                    self.CalculateTableWidget.setItem(row, col, item)
                item.setFlags(flags)

    def Get_and_update_rooms(self):
        table_contents = []
        count_temp = 0
        count_name = 0
        for row in range(self.RoomsTableWidget.rowCount()):
            room_name_item = self.RoomsTableWidget.item(row, 0)
            temp = self.RoomsTableWidget.cellWidget(row, 1)

            if room_name_item and temp:
                room_name = room_name_item.text()
                temp = temp.value()
                row_data = {'rooms_name': room_name, 'temp': temp}
                table_contents.append(row_data)
                count_name += 1
            else:
                message_box = QMessageBox()
                message_box.critical(
                    None, "Ошибка!", f"У помещения № {count_name + 1} не заполнено название")
                message_box.setFixedSize(500, 200)
                count_name = 0
                return

        for rooms in table_contents:
            if rooms['temp'] == 0.0:
                message_box = QMessageBox()
                message_box.critical(
                    None, "Ошибка!", f"Температура для помещения № {count_temp + 1} не заполнен")
                message_box.setFixedSize(500, 200)
                count_temp = 0
                return
            count_temp += 1
        self.list_rooms = table_contents

    def parse_rooms(self, data):
        result = []
        for rooms_and_temp in data:
            result.append(rooms_and_temp['rooms_name'])
        return result

    def ClearTableCalculate(self):
        self.CalculateTableWidget.setRowCount(0)
        self.AddCalculateRow()
