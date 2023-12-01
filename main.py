import sys
from PyQt6.QtWidgets import QMainWindow, QHeaderView, QApplication
from PyQt6 import uic
from materials import MaterialsTable
from walls import WallsTable
from rooms import RoomsTable
from calculate import CalculateTable
import os

ui_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'gui.ui'))


class GUI(QMainWindow, MaterialsTable,
          WallsTable, RoomsTable, CalculateTable):

    def __init__(self):
        super(GUI, self).__init__()
        uic.loadUi(ui_path, self)
        self.list_materials = []
        self.list_rooms = []
        self.list_material_position = []
        self.set_autosize_table()
        self.materials()
        self.calculate()
        self.rooms()
        self.walls()

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

    def calculate(self):
        '''Методы для таблицы расчеты'''
        self.AddRowCalculatePushButton.clicked.connect(self.AddCalculateRow)
        self.RemoveRowCalculatePushButton.clicked.connect(self.RemoveCalculateRow)  # noqa E501
        self.GetRoomsPushButton.clicked.connect(self.GetRooms)
        self.CalculateCountSpinBox()
        self.CalculateWallComboBox()
        self.CalculateComboBox()
        self.MakeCalculateCellReadOnly()

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

    def walls(self):
        '''Методы для таблицы стен'''
        self.AddRowWallsPushButton.clicked.connect(self.AddWallsRow)
        self.RemoveRowWallsPushButton.clicked.connect(self.RemoveWallsRow)
        self.GetMaterialsPushButton.clicked.connect(self.GetMaterials)
        self.WallLayerComboBox()
        self.MakeWallsCellReadOnly()


def main():
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
