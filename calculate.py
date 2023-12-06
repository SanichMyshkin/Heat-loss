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

        current_row = self.CalculateTableWidget.rowCount() - 1
        wall_combo_box = self.CalculateTableWidget.cellWidget(current_row, 4)
        wall_combo_box.currentIndexChanged.connect(self.Get_wall_coeff)
        room_combo_box1 = self.CalculateTableWidget.cellWidget(current_row, 0)
        room_combo_box1.currentIndexChanged.connect(self.Get_temp)
        room_combo_box2 = self.CalculateTableWidget.cellWidget(current_row, 1)
        room_combo_box2.currentIndexChanged.connect(self.Get_temp)

        self.Get_temp()
        self.Get_wall_coeff()

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
                        None, "Ошибка!", f"Помещение с названием '{room_name}' уже существует")  # noqa E501
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
                    None, "Ошибка!", f"У помещения № {count_name + 1} не заполнено название")  # noqa E501
                message_box.setFixedSize(500, 200)
                count_name = 0
                return

        for materials in table_contents:
            if materials['temperature'] == 0.0:
                message_box = QMessageBox()
                message_box.critical(
                    None, "Ошибка!", f"Температура для помещения № {count_temp + 1} не заполнена")  # noqa E501
                message_box.setFixedSize(500, 200)
                count_temp += 1
                return

        self.list_rooms = table_contents
        self.ClearAndPopulateRoomsComboBox()
        self.CalculateRoomsComboBox()
        self.Get_temp()

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
                combo_box.currentIndexChanged.connect(self.Get_temp)

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
            coefficient_item = self.WallsTableWidget.item(row, 7)

            if not coefficient_item:
                message_box = QMessageBox()
                message_box.critical(
                    None, "Ошибка!", "Коэффициенты теплопередачи для стен не расcчитанны!")  # noqa E501
                message_box.setFixedSize(500, 200)
                return

            if wall_name_item:
                wall_name = wall_name_item.text()

                if wall_name in existing_materials:
                    message_box = QMessageBox()
                    message_box.critical(
                        None, "Ошибка!", f"Стена с названием '{wall_name}' уже существует")  # noqa E501
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
                    None, "Ошибка!", f"У стены № {count_name + 1} не заполнено название")  # noqa E501
                message_box.setFixedSize(500, 200)
                count_name = 0
                return

        self.list_walls = table_contents
        self.CalculateWallsComboBox()
        self.Get_wall_coeff()

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
            if row < len(self.list_walls_position) and len(self.list_walls_position[row]) > 0:  # noqa E501
                current_text = self.list_walls_position[row][0]
                index = combo_box.findText(current_text)
                if index != -1:
                    combo_box.setCurrentIndex(index)
                combo_box.currentIndexChanged.connect(self.Get_wall_coeff)

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

    def Get_temp(self):
        column_number = [0, 1]
        temp_dict = {
            item['rooms_name']: item['temperature'] for item in self.list_rooms
        }

        for row in range(self.CalculateTableWidget.rowCount()):
            for col in column_number:
                name_room = self.CalculateTableWidget.cellWidget(
                    row, col).currentText()
                temperature = temp_dict.get(name_room, 0.0)
                temp_item = QTableWidgetItem()
                temp_item.setData(0, f'{temperature}')
                self.CalculateTableWidget.setItem(row, col + 2, temp_item)
                self.CalculateTableWidget.item(
                    row, col + 2).setText(f'{temperature}')

    def compare_rooms(self, list1, list2):

        set1 = {(item['rooms_name'],
                item['temperature'])
                for item in list1}

        set2 = {(item['rooms_name'],
                item['temperature'])
                for item in list2}

        if set1 == set2:
            return True
        else:
            return False

    def valid_rooms(self):
        current_table = []
        for row in range(self.RoomsTableWidget.rowCount()):
            current_room_name_item = self.RoomsTableWidget.item(row, 0)
            current_temp_item = self.RoomsTableWidget.cellWidget(
                row, 1)

            room_name = current_room_name_item.text()
            temp_value = current_temp_item.value()
            row_data = {'rooms_name': room_name,
                        'temperature': temp_value,
                        }
            current_table.append(row_data)
        return self.compare_rooms(current_table, self.list_rooms)

    def Get_wall_coeff(self):
        col = 4
        wall_dict = {}
        for row in range(self.WallsTableWidget.rowCount()):
            name_wall = self.WallsTableWidget.item(row, 0).text()
            R = self.WallsTableWidget.item(row, 7).text()
            wall_dict[name_wall] = R

        for row in range(self.CalculateTableWidget.rowCount()):
            name_wall = self.CalculateTableWidget.cellWidget(
                row, col).currentText()
            R = wall_dict.get(name_wall, 0.0)
            R_item = QTableWidgetItem()
            R_item.setData(0, f'{R}')
            self.CalculateTableWidget.setItem(row, col + 4, R_item)
            self.CalculateTableWidget.item(
                row, col + 4).setText(f'{R}')

    def valid_walls(self):
        # Получить текущие данные о стенах из таблицы
        current_table = []
        for row in range(self.WallsTableWidget.rowCount()):
            current_wall_name_item = self.WallsTableWidget.item(row, 0)
            current_coefficient_item = self.WallsTableWidget.item(row, 7)

            wall_name = current_wall_name_item.text()
            coefficient_value = current_coefficient_item.text()

            row_data = {'wall_name': wall_name,
                        'coefficient_value': coefficient_value}
            current_table.append(row_data)

        # Сравнить текущие данные о стенах с сохраненными данными
        return self.compare_walls(current_table, self.list_walls)

    def compare_walls(self, list1, list2):
        set1 = {(item['wall_name'], item['coefficient_value'])
                for item in list1}
        set2 = {(item['wall_name'], item['coefficient_value'])
                for item in list2}

        # Если множества совпадают, данные считаются актуальными
        return set1 == set2

    def ShowCalculate(self):
        if self.valid_rooms() is False:
            message_box = QMessageBox()
            message_box.critical(
                    None, "Ошибка!", f"Помещения устарели!\nПожалуйcта, обновите помещения!")  # noqa E501
            message_box.setFixedSize(500, 200)
        if self.valid_walls() is False:
            message_box = QMessageBox()
            message_box.critical(
                    None, "Ошибка!", f"Стены устарели!\nПожалуйcта, обновите стены!")  # noqa E501
            message_box.setFixedSize(500, 200)
