import sys
import os
import openpyxl

from PyQt6.QtWidgets import QMainWindow, QHeaderView, \
    QApplication, QFileDialog, QMessageBox
from PyQt6 import uic

from materials import MaterialsTable
from walls import WallsTable
from rooms import RoomsTable
from calculate import CalculateTable


ui_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'gui.ui'))


class GUI(QMainWindow, MaterialsTable,
          WallsTable, RoomsTable, CalculateTable):

    def __init__(self):
        super(GUI, self).__init__()
        uic.loadUi(ui_path, self)

        self.setWindowTitle(
            "Расчет тепловых потерь через внутренние ограждающие конструкции")

        # Списки для передачи и хранения материалов
        self.list_materials = []
        self.list_material_position = []

        # Списки для для передачи и обновления помещений
        self.list_rooms = []
        self.list_rooms_position = []

        # Списки для передачи и обновлений стен
        self.list_walls = []
        self.list_walls_position = []

        # Инициализация методов для каждой таблицы
        self.set_autosize_table()
        self.materials()
        self.calculate()
        self.rooms()
        self.walls()

        # Иницализация методов для очистки данных
        self.ClearMaterials.triggered.connect(self.ClearTableMaterials)
        self.ClearWalls.triggered.connect(self.ClearTableWalls)
        self.ClearRooms.triggered.connect(self.ClearTableRooms)
        self.ClearCalculate.triggered.connect(self.ClearTableCalculate)
        self.ClearAll.triggered.connect(self.ClearAllTable)
        self.SaveAll.triggered.connect(self.Save)
        self.ExpMaterialsAction.triggered.connect(self.ExpMaterials)
        self.ExpRoomsAction.triggered.connect(self.ExpRooms)

    def ClearAllTable(self):
        '''Метод очищения всех таблиц'''
        self.ClearTableMaterials()
        self.ClearTableWalls()
        self.ClearTableRooms()
        self.ClearTableCalculate()

    def set_autosize_table(self):
        '''Расстягивание ширины заголовков таблиц под ширину экрана'''
        self.MaterialsTableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

        self.RoomsTableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

        self.WallsTableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

        self.CalculateTableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

    def materials(self):
        '''Методы для таблицы материалов'''
        self.AddRowMaterialsPushButton.clicked.connect(self.AddMaterialsRow)
        self.RemoveRowMaterialsPushButton.clicked.connect(self.RemoveMaterialsRow)  # noqa E501
        self.MaterialsCountSpinBox()

    def rooms(self):
        '''Методы для таблицы помещение'''
        self.AddRowRoomsPushButton.clicked.connect(self.AddRoomsRow)
        self.RemoveRowRoomsPushButton.clicked.connect(self.RemoveRoomsRow)  # noqa E501
        self.RoomsCountSpinBox()

    def calculate(self):
        '''Методы для таблицы расчеты'''
        self.AddRowCalculatePushButton.clicked.connect(self.AddCalculateRow)
        self.RemoveRowCalculatePushButton.clicked.connect(self.RemoveCalculateRow)  # noqa E501
        self.GetRoomsPushButton.clicked.connect(self.GetRoomsAndWalls)
        self.ShowCalculatePushButton.clicked.connect(self.ShowCalculate)

        self.CalculateCountSpinBox()
        self.CalculateRoomsComboBox()
        self.CalculateWallsComboBox()
        self.MakeCalculateCellReadOnly()

    def walls(self):
        '''Методы для таблицы стен'''
        self.AddRowWallsPushButton.clicked.connect(self.AddWallsRow)
        self.RemoveRowWallsPushButton.clicked.connect(self.RemoveWallsRow)
        self.GetMaterialsPushButton.clicked.connect(self.GetMaterials)
        self.CalculateWallsPushButton.clicked.connect(self.CalculateWalls)  # noqa
        self.WallLayerComboBox()
        self.MakeWallsCellReadOnly()

    def Save(self):
        file_dialog = QFileDialog()
        path, _ = file_dialog.getSaveFileName(
            self, "Сохранить файл", "Расчеты", "Excel Files (*.xlsx);;All Files (*)")
        if not path:
            return
        wb = openpyxl.Workbook()
        if 'Sheet' in wb.sheetnames:
            wb.remove(wb['Sheet'])
        self.SaveMaterials(wb)
        self.SaveRooms(wb)
        wb.save(path)
        QMessageBox.information(
            self, "Успешно", "Файл успешно сохранен!")

    def SaveRooms(self, workbook):
        ws_rooms = workbook.create_sheet("Помещения", 0)
        column_headers = ["Название", "Температура"]
        for col_num, header in enumerate(column_headers, 1):
            header_cell = ws_rooms.cell(row=1, column=col_num)
            header_cell.value = header
        for row in range(self.RoomsTableWidget.rowCount()):
            name_rooms_item = self.RoomsTableWidget.item(row, 0)
            temperature_value = self.RoomsTableWidget.cellWidget(
                row, 1).value()
            name_rooms = name_rooms_item.text() if name_rooms_item else "-"
            ws_rooms.cell(row=row + 2, column=1, value=name_rooms)
            ws_rooms.cell(row=row + 2, column=2, value=temperature_value)

    def SaveMaterials(self, workbook):
        ws_materials = workbook.create_sheet("Материалы", 1)

        column_headers = ["Наименование", "λ", "δ,м"]
        for col_num, header in enumerate(column_headers, 1):
            header_cell = ws_materials.cell(row=1, column=col_num)
            header_cell.value = header

        for row in range(self.MaterialsTableWidget.rowCount()):
            name_materials_item = self.MaterialsTableWidget.item(row, 0)
            coeff_value = self.MaterialsTableWidget.cellWidget(row, 1).value()
            thickness_value = self.MaterialsTableWidget.cellWidget(
                row, 2).value()
            name_materials = name_materials_item.text() if name_materials_item else "-"
            ws_materials.cell(row=row + 2, column=1, value=name_materials)
            ws_materials.cell(row=row + 2, column=2, value=coeff_value)
            ws_materials.cell(row=row + 2, column=3, value=thickness_value)

    def SaveWalls(self, workbook):
        pass

    def SaveCaclulate(self, workbook):
        pass

    def ExpMaterials(self):
        file_dialog = QFileDialog()
        path, _ = file_dialog.getSaveFileName(
            self, "Экспорт материалов", "Материалы", "Excel Files (*.xlsx);;All Files (*)")
        if not path:
            return
        wb = openpyxl.Workbook()
        if 'Sheet' in wb.sheetnames:
            wb.remove(wb['Sheet'])
        self.SaveMaterials(wb)
        wb.save(path)
        QMessageBox.information(
            self, "Успешно", "Материалы успешно экспортированны!")

    def ExpRooms(self):
        file_dialog = QFileDialog()
        path, _ = file_dialog.getSaveFileName(
            self, "Экспорт помещений", "Помещения", "Excel Files (*.xlsx);;All Files (*)")
        if not path:
            return
        wb = openpyxl.Workbook()
        if 'Sheet' in wb.sheetnames:
            wb.remove(wb['Sheet'])
        self.SaveRooms(wb)
        wb.save(path)
        QMessageBox.information(
            self, "Успешно", "Помещения успешно экспортированны!")


def main():
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
