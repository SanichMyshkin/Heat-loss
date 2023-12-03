from PyQt6.QtWidgets import QDoubleSpinBox, \
    QComboBox, QTableWidgetItem, QMessageBox
from PyQt6 import QtCore


class CalculateTable():
    MAX_RANGE = 10000.0

    def __init__(self):
        self.list_rooms = []
        self.list_rooms_position = []

        self.list_walls = []
        self.list_walls_position = []

    def GetRoomsAndWalls(self):
        self.GetAndUpdateWalls()
        self.GetAndUpdateRooms()
        self.CalculateWallsComboBox()
        self.CalculateRoomsComboBox()

        self.UpdateRoomsComboBox()
        self.UpdateWallsComboBox()

    def AddCalculateRow(self):
        self.CalculateTableWidget.insertRow(
            self.CalculateTableWidget.rowCount())
        self.CalculateCountSpinBox()
        self.CalculateWallsComboBox()
        self.CalculateRoomsComboBox()
        self.MakeCalculateCellReadOnly()

    def RemoveCalculateRow(self):
        self.CalculateTableWidget.removeRow(
            self.CalculateTableWidget.rowCount() - 1)

    def CalculateCountSpinBox(self):
        column_number = [5, 6]
        current_row = self.CalculateTableWidget.rowCount() - 1
        for number in column_number:
            coeff_thermal_conductivity = QDoubleSpinBox()
            coeff_thermal_conductivity.setMaximum(self.MAX_RANGE)
            self.CalculateTableWidget.setCellWidget(
                current_row, number, coeff_thermal_conductivity)

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

    def GetAndUpdateRooms(self):
        table_contents = []
        count_temp = 0
        count_name = 0
        existing_rooms = set()

        for row in range(self.RoomsTableWidget.rowCount()):
            room_name_item = self.RoomsTableWidget.item(row, 0)
            coefficient_item = self.RoomsTableWidget.cellWidget(row, 1)

            if room_name_item and coefficient_item:
                room_name = room_name_item.text()

                if room_name in existing_rooms:
                    message_box = QMessageBox()
                    message_box.critical(
                        None, "Ошибка!", f"Помещение с названием '{room_name}' уже существует")  # noqa
                    message_box.setFixedSize(500, 200)
                    return
                else:
                    existing_rooms.add(room_name)

                temperature = coefficient_item.value()
                row_data = {'rooms_name': room_name,
                            'temperature': temperature}
                table_contents.append(row_data)
                count_name += 1
            else:
                message_box = QMessageBox()
                message_box.critical(
                    None, "Ошибка!", f"У помещения № {count_name + 1} не заполнено название")
                message_box.setFixedSize(500, 200)
                count_name = 0
                return

        for materials in table_contents:
            if materials['temperature'] == 0.0:
                message_box = QMessageBox()
                message_box.critical(
                    None, "Ошибка!", f"Температура для помещения № {count_temp + 1} не заполнена")
                message_box.setFixedSize(500, 200)
                count_temp += 1
                return

        self.list_rooms = table_contents
        self.ClearAndPopulateRoomsComboBox()
        self.CalculateRoomsComboBox()

    def ClearAndPopulateRoomsComboBox(self):
        column_number = [0, 1]
        for row in range(self.CalculateTableWidget.rowCount()):
            for col in column_number:
                combo_box = self.CalculateTableWidget.cellWidget(row, col)
                current_text = combo_box.currentText()
                combo_box.clear()
                combo_box.addItems(self.parse_rooms(self.list_rooms))
                index = combo_box.findText(current_text)
                if index != -1:
                    combo_box.setCurrentIndex(index)
                elif combo_box.count() > 0:
                    combo_box.setCurrentIndex(0)

    def UpdateRoomsComboBox(self):
        column_number = [0, 1]
        for row in range(self.CalculateTableWidget.rowCount()):
            for col in column_number:
                combo_box = self.CalculateTableWidget.cellWidget(row, col)
                current_text = combo_box.currentText()
                combo_box.clear()
                combo_box.addItems(self.parse_rooms(self.list_rooms))
                index = combo_box.findText(current_text)
                if index != -1:
                    combo_box.setCurrentIndex(index)

    def CalculateRoomsComboBox(self):
        column_number = [0, 1]
        for row in range(self.CalculateTableWidget.rowCount()):
            for number in column_number:
                combo_box = self.CalculateTableWidget.cellWidget(row, number)
                if combo_box is None:
                    combo_box = QComboBox()
                    self.CalculateTableWidget.setCellWidget(
                        row, number, combo_box)
                existing_items = [combo_box.itemText(
                    i) for i in range(combo_box.count())]
                for new_item in self.parse_rooms(self.list_rooms):
                    if new_item not in existing_items:
                        combo_box.addItem(new_item)

    def parse_rooms(self, data):
        result = []
        for rooms_and_temp in data:
            result.append(rooms_and_temp['rooms_name'])
        return result

    def SavePositionRooms(self):
        number_column = [0, 1]
        if self.list_rooms_position:
            self.list_rooms_position.clear()

        for row in range(self.CalculateTableWidget.rowCount()):
            row_data = [self.CalculateTableWidget.cellWidget(
                row, col).currentText() for col in number_column]
            self.list_rooms_position.append(row_data)

    def ClearTableCalculate(self):
        self.CalculateTableWidget.setRowCount(0)
        self.AddCalculateRow()

    def GetAndUpdateWalls(self):
        table_contents = []
        count_name = 0
        existing_materials = set()

        for row in range(self.WallsTableWidget.rowCount()):
            wall_name_item = self.WallsTableWidget.item(row, 0)
            coefficient_item = self.WallsTableWidget.item(row, 9)

            if not coefficient_item:
                message_box = QMessageBox()
                message_box.critical(
                    None, "Ошибка!", "Коэффициенты теплопередачи для стен не расcчитанны!")
                message_box.setFixedSize(500, 200)
                return

            if wall_name_item:
                wall_name = wall_name_item.text()

                if wall_name in existing_materials:
                    message_box = QMessageBox()
                    message_box.critical(
                        None, "Ошибка!", f"Стена с названием '{wall_name}' уже существует") #
                    message_box.setFixedSize(500, 200)
                    return
                else:
                    existing_materials.add(wall_name)

                coefficient_value = coefficient_item.text()
                row_data = {'wall_name': wall_name,
                            'coefficient_value': coefficient_value}
                table_contents.append(row_data)
                count_name += 1
            else:
                message_box = QMessageBox()
                message_box.critical(
                    None, "Ошибка!", f"У стены № {count_name + 1} не заполнено название")
                message_box.setFixedSize(500, 200)
                count_name = 0
                return

        self.list_walls = table_contents
        self.CalculateWallsComboBox()  # Обновите комбобоксы после обновления материалов

    def CalculateWallsComboBox(self):
        column_number = [4]
        for row in range(self.CalculateTableWidget.rowCount()):
            for number in column_number:
                combo_box = self.CalculateTableWidget.cellWidget(row, number)
                if combo_box is None:
                    combo_box = QComboBox()
                    self.CalculateTableWidget.setCellWidget(
                        row, number, combo_box)
                existing_items = [combo_box.itemText(
                    i) for i in range(combo_box.count())]
                for new_item in self.parse_walls(self.list_walls):
                    if new_item not in existing_items:
                        combo_box.addItem(new_item)

    def UpdateWallsComboBox(self):
        self.SavePositionWalls()
        for row in range(self.CalculateTableWidget.rowCount()):
            combo_box = self.CalculateTableWidget.cellWidget(row, 4)
            combo_box.clear()
            combo_box.addItems(self.parse_walls(self.list_walls))
            if row < len(self.list_walls_position) and len(self.list_walls_position[row]) > 0:
                current_text = self.list_walls_position[row][0]
                index = combo_box.findText(current_text)
                if index != -1:
                    combo_box.setCurrentIndex(index)

    def parse_walls(self, data):
        result = []
        for walls_and_coeff in data:
            result.append(walls_and_coeff['wall_name'])
        return result

    def SavePositionWalls(self):
        col = 4
        if self.list_walls_position:
            self.list_walls_position.clear()

        for row in range(self.CalculateTableWidget.rowCount()):
            row_data = [self.CalculateTableWidget.cellWidget(
                row, col).currentText()]
            self.list_walls_position.append(row_data)
