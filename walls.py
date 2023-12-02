from PyQt6.QtWidgets import QTableWidgetItem, QComboBox, QMessageBox
from PyQt6 import QtCore


class WallsTable:

    def __init__(self):
        self.list_materials = []
        self.list_material_position = []

    def GetMaterials(self):
        self.GetAndUpdateMaterials()
        self.WallLayerComboBox()
        self.UpdateComboBox()

    def AddWallsRow(self):
        self.WallsTableWidget.insertRow(self.WallsTableWidget.rowCount())
        self.WallLayerComboBox()
        self.MakeWallsCellReadOnly()

    def RemoveWallsRow(self):
        self.WallsTableWidget.removeRow(self.WallsTableWidget.rowCount() - 1)

    def MakeWallsCellReadOnly(self):
        flags = QtCore.Qt.ItemFlag.ItemIsEnabled
        for row in range(self.WallsTableWidget.rowCount()):
            for col in range(5, self.WallsTableWidget.columnCount()):
                item = self.WallsTableWidget.item(row, col)
                if item is None:
                    item = QTableWidgetItem()
                    self.WallsTableWidget.setItem(row, col, item)
                item.setFlags(flags)

    def WallLayerComboBox(self):
        column_number = [1, 2, 3, 4, 5]

        for row in range(self.WallsTableWidget.rowCount()):
            for number in column_number:
                combo_box = self.WallsTableWidget.cellWidget(row, number)

                # Проверка, существует ли уже QComboBox в ячейке
                if combo_box is None:
                    combo_box = QComboBox()
                    self.WallsTableWidget.setCellWidget(row, number, combo_box)

                # Получаем список существующих значений в комбобоксе
                existing_items = [combo_box.itemText(
                    i) for i in range(combo_box.count())]

                # Добавляем новые значения, не удаляя старые, и проверяем на дублирование
                for new_item in self.parse_materials(self.list_materials):
                    if new_item not in existing_items:
                        combo_box.addItem(new_item)

    def UpdateComboBox(self):
        column_number = [1, 2, 3, 4, 5]
        self.SavePositionMaterials()

        for row in range(self.WallsTableWidget.rowCount()):
            for col in column_number:
                combo_box = self.WallsTableWidget.cellWidget(row, col)
                combo_box.clear()
                combo_box.addItems(self.parse_materials(self.list_materials))
                if row < len(self.list_material_position) and col - 1 < len(self.list_material_position[row]):
                    current_text = self.list_material_position[row][col - 1]
                    index = combo_box.findText(current_text)
                    if index != -1:
                        combo_box.setCurrentIndex(index)

    def GetAndUpdateMaterials(self):
        table_contents = []
        count_temp = 0
        count_name = 0
        existing_materials = set()

        for row in range(self.MaterialsTableWidget.rowCount()):
            material_name_item = self.MaterialsTableWidget.item(row, 0)
            coefficient_item = self.MaterialsTableWidget.cellWidget(row, 1)

            if material_name_item and coefficient_item:
                material_name = material_name_item.text()

                # Проверка на уникальность материала
                if material_name in existing_materials:
                    message_box = QMessageBox()
                    message_box.critical(
                        None, "Ошибка!", f"Материал с названием '{material_name}' уже существует")
                    message_box.setFixedSize(500, 200)
                    return
                else:
                    existing_materials.add(material_name)

                coefficient_value = coefficient_item.value()
                row_data = {'material_name': material_name,
                            'coefficient_value': coefficient_value}
                table_contents.append(row_data)
                count_name += 1
            else:
                message_box = QMessageBox()
                message_box.critical(
                    None, "Ошибка!", f"У материала № {count_name + 1} не заполнено название")
                message_box.setFixedSize(500, 200)
                count_name = 0
                return

        for materials in table_contents:
            if materials['coefficient_value'] == 0.0:
                message_box = QMessageBox()
                message_box.critical(
                    None, "Ошибка!", f"Коэффициент для материала № {count_temp + 1} не заполнен")
                message_box.setFixedSize(500, 200)
                count_temp += 1
                return

        self.list_materials = table_contents
        self.WallLayerComboBox()  # Обновите комбобоксы после обновления материалов

    def parse_materials(self, data):
        result = []
        for materials_and_temp in data:
            result.append(materials_and_temp['material_name'])
        return result

    def SavePositionMaterials(self):
        number_column = [1, 2, 3, 4, 5]

        if self.list_material_position:
            self.list_material_position.clear()

        for row in range(self.WallsTableWidget.rowCount()):
            row_data = [self.WallsTableWidget.cellWidget(
                row, col).currentText() for col in number_column]
            self.list_material_position.append(row_data)

    def ClearTableWalls(self):
        self.WallsTableWidget.setRowCount(0)
        self.AddWallsRow()
