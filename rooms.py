from PyQt6.QtWidgets import QDoubleSpinBox


class RoomsTable():

    MAX_RANGE = 1000.0

    def AddRoomsRow(self):
        self.RoomsTableWidget.insertRow(self.RoomsTableWidget.rowCount())  # noqa E501
        self.RoomsCountSpinBox()

    def RemoveRoomsRow(self):
        self.RoomsTableWidget.removeRow(self.RoomsTableWidget.rowCount()-1)  # noqa E501

    def RoomsCountSpinBox(self):
        column_number = 1
        current_row = self.RoomsTableWidget.rowCount() - 1
        coeff_thermal_conductivity = QDoubleSpinBox()  # noqa F405
        coeff_thermal_conductivity.setMaximum(self.MAX_RANGE)
        self.RoomsTableWidget.setCellWidget(current_row, column_number, coeff_thermal_conductivity)  # noqa E501
