from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QLabel, QMessageBox
)
from api import upload_csv
from charts import PieChartCanvas, BarChartCanvas

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.resize(800, 600)

        self.layout = QVBoxLayout()

        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.handle_upload)

        self.summary_label = QLabel("Upload a CSV to see summary")

        self.layout.addWidget(self.upload_btn)
        self.layout.addWidget(self.summary_label)

        self.setLayout(self.layout)

    def handle_upload(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            result = upload_csv(file_path)
            summary = result["summary"]

            self.summary_label.setText(
                f"""
Total Equipment: {summary['total_equipment']}
Avg Flowrate: {summary['average_flowrate']}
Avg Pressure: {summary['average_pressure']}
Avg Temperature: {summary['average_temperature']}
"""
            )

            pie = PieChartCanvas(summary["equipment_type_distribution"])
            bar = BarChartCanvas(summary["equipment_type_distribution"])

            self.layout.addWidget(pie)
            self.layout.addWidget(bar)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
