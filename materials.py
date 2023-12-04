from PyQt6.QtWidgets import QDoubleSpinBox, QTableWidget, QTableWidgetItem


class MaterialsTable:
    MAX_RANGE = 10000.0

    def AddMaterialsRow(self):
        self.MaterialsTableWidget.insertRow(
            self.MaterialsTableWidget.rowCount())
        self.MaterialsCountSpinBox()

    def RemoveMaterialsRow(self):
        self.MaterialsTableWidget.removeRow(
            self.MaterialsTableWidget.rowCount() - 1)

    def MaterialsCountSpinBox(self):
        column_number = [1, 2]
        for col in column_number:
            current_row = self.MaterialsTableWidget.rowCount() - 1
            coeff_thermal_conductivity = QDoubleSpinBox()
            coeff_thermal_conductivity.setMaximum(self.MAX_RANGE)
            self.MaterialsTableWidget.setCellWidget(
                current_row, col, coeff_thermal_conductivity)

    def ClearTableMaterials(self):
        self.MaterialsTableWidget.setRowCount(0)
        self.AddMaterialsRow()
