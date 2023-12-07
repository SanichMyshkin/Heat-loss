import sys
import os

from PyQt6.QtWidgets import QMainWindow, QHeaderView, QApplication
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


def main():
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
